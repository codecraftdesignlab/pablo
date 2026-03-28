-- ============================================================
-- Veeqo Auto-Sync Trigger for Supabase
-- ============================================================
-- Fires on product_variant INSERT, pushes new variants to
-- Veeqo via pg_net HTTP POST.
--
-- Prerequisites:
--   - pg_net extension (CREATE EXTENSION IF NOT EXISTS pg_net;)
--   - supabase_vault with secret 'veeqo_api_key'
--
-- Run: psql $DATABASE_URL -f setup-veeqo-trigger.sql
-- ============================================================

-- 0. Ensure pg_net is enabled
CREATE EXTENSION IF NOT EXISTS pg_net;

-- 1. Sync log table
CREATE TABLE IF NOT EXISTS public.veeqo_sync_log (
    id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    variant_id      text NOT NULL,
    sku             text NOT NULL,
    product_title   text,
    variant_title   text,
    price_gbp       numeric,
    http_request_id bigint,          -- pg_net request id
    status          text NOT NULL DEFAULT 'pending',  -- pending | synced | failed
    error_message   text,
    created_at      timestamptz NOT NULL DEFAULT now(),
    updated_at      timestamptz NOT NULL DEFAULT now(),

    -- Dedup: one log row per variant
    CONSTRAINT uq_veeqo_sync_variant UNIQUE (variant_id)
);

-- Index for reconciliation queries
CREATE INDEX IF NOT EXISTS idx_veeqo_sync_status ON public.veeqo_sync_log (status);

-- RLS: only service role can read/write
ALTER TABLE public.veeqo_sync_log ENABLE ROW LEVEL SECURITY;

-- Drop existing policies to make script idempotent
DROP POLICY IF EXISTS "Service role full access" ON public.veeqo_sync_log;

CREATE POLICY "Service role full access"
    ON public.veeqo_sync_log
    FOR ALL
    USING (auth.role() = 'service_role')
    WITH CHECK (auth.role() = 'service_role');


-- 2. Trigger function
CREATE OR REPLACE FUNCTION public.fn_veeqo_sync_variant()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_product_title  text;
    v_product_status text;
    v_price_gbp      numeric;
    v_api_key        text;
    v_payload        jsonb;
    v_request_id     bigint;
    v_weight_val     integer;
BEGIN
    -- Guard: skip if SKU is NULL or empty
    IF NEW.sku IS NULL OR trim(NEW.sku) = '' THEN
        RETURN NEW;
    END IF;

    -- Guard: skip if parent product is not published (or missing)
    SELECT p.title, p.status
      INTO v_product_title, v_product_status
      FROM public.product p
     WHERE p.id = NEW.product_id
       AND p.deleted_at IS NULL;

    IF v_product_status IS NULL OR v_product_status != 'published' THEN
        RETURN NEW;
    END IF;

    -- Dedup: insert into sync log, skip if variant already logged
    INSERT INTO public.veeqo_sync_log (variant_id, sku, product_title, variant_title)
    VALUES (NEW.id, NEW.sku, v_product_title, NEW.title)
    ON CONFLICT (variant_id) DO NOTHING;

    -- If row already existed, skip the HTTP call
    IF NOT FOUND THEN
        RETURN NEW;
    END IF;

    -- Fetch GBP price via: variant -> product_variant_price_set -> price
    SELECT p.amount
      INTO v_price_gbp
      FROM public.product_variant_price_set pvps
      JOIN public.price p ON p.price_set_id = pvps.price_set_id
     WHERE pvps.variant_id = NEW.id
       AND p.currency_code = 'gbp'
       AND p.deleted_at IS NULL
     ORDER BY p.created_at DESC
     LIMIT 1;

    -- Update log with price
    UPDATE public.veeqo_sync_log
       SET price_gbp = v_price_gbp
     WHERE variant_id = NEW.id;

    -- Get API key from Supabase Vault
    SELECT decrypted_secret
      INTO v_api_key
      FROM vault.decrypted_secrets
     WHERE name = 'veeqo_api_key'
     LIMIT 1;

    IF v_api_key IS NULL THEN
        UPDATE public.veeqo_sync_log
           SET status = 'failed',
               error_message = 'Vault secret veeqo_api_key not found',
               updated_at = now()
         WHERE variant_id = NEW.id;
        RETURN NEW;
    END IF;

    -- Weight: product_variant.weight is integer (grams), default 0
    v_weight_val := COALESCE(NEW.weight, 0);

    -- Build Veeqo payload
    v_payload := jsonb_build_object(
        'product', jsonb_build_object(
            'title', v_product_title,
            'variants', jsonb_build_array(
                jsonb_build_object(
                    'title',    COALESCE(NEW.title, NEW.sku),
                    'sku_code', NEW.sku,
                    'price',    COALESCE(v_price_gbp, 0)::text,
                    'tax_rate', 20.0,
                    'weight',   jsonb_build_object(
                        'value', v_weight_val,
                        'unit',  'g'
                    )
                )
            )
        )
    );

    -- Fire async HTTP POST via pg_net
    SELECT net.http_post(
        url     := 'https://api.veeqo.com/products',
        body    := v_payload,
        headers := jsonb_build_object(
            'Content-Type', 'application/json',
            'x-api-key',    v_api_key,
            'User-Agent',   'Pablo/1.0 (Supabase trigger)'
        )
    ) INTO v_request_id;

    -- Store the request ID so reconciliation can check the response
    UPDATE public.veeqo_sync_log
       SET http_request_id = v_request_id,
           updated_at = now()
     WHERE variant_id = NEW.id;

    RETURN NEW;
END;
$$;


-- 3. Trigger on product_variant AFTER INSERT
DROP TRIGGER IF EXISTS trg_veeqo_sync_variant ON public.product_variant;

CREATE TRIGGER trg_veeqo_sync_variant
    AFTER INSERT ON public.product_variant
    FOR EACH ROW
    EXECUTE FUNCTION public.fn_veeqo_sync_variant();


-- Done
-- Verify: SELECT * FROM public.veeqo_sync_log ORDER BY created_at DESC LIMIT 10;
