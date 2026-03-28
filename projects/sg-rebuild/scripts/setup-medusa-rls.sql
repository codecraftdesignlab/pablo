-- =============================================================
-- Setup Row Level Security on all Medusa tables in Supabase
-- =============================================================
-- Purpose: Lock down public schema tables so that:
--   1. Only the service_role can perform all operations
--   2. Authenticated users get read-only access
--   3. The anon role has no access at all
--
-- Excludes legacy SG tables that already have RLS configured.
-- Skips any table that already has RLS enabled.
-- =============================================================

DO $$
DECLARE
    tbl RECORD;
    policy_exists BOOLEAN;
    excluded_tables TEXT[] := ARRAY[
        'operational_skus',
        'articles',
        'orders',
        'sku_logs',
        'sku_stats',
        'commodity_codes',
        'fault_codes',
        'special_customers',
        'goat_text_generator',
        'analytics_orders',
        'analytics_customers'
    ];
BEGIN
    FOR tbl IN
        SELECT t.tablename
        FROM pg_tables t
        WHERE t.schemaname = 'public'
          AND t.tablename != ALL(excluded_tables)
          AND t.rowsecurity = false
        ORDER BY t.tablename
    LOOP
        -- Enable RLS
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', tbl.tablename);

        -- Revoke all permissions from anon role
        EXECUTE format('REVOKE ALL ON public.%I FROM anon', tbl.tablename);

        -- Policy: service_role gets full access
        SELECT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname = 'public'
              AND tablename = tbl.tablename
              AND policyname = 'Service role full access'
        ) INTO policy_exists;

        IF NOT policy_exists THEN
            EXECUTE format(
                'CREATE POLICY "Service role full access" ON public.%I FOR ALL USING (auth.role() = ''service_role'') WITH CHECK (auth.role() = ''service_role'')',
                tbl.tablename
            );
        END IF;

        -- Policy: authenticated users get read-only access
        SELECT EXISTS (
            SELECT 1 FROM pg_policies
            WHERE schemaname = 'public'
              AND tablename = tbl.tablename
              AND policyname = 'Authenticated read access'
        ) INTO policy_exists;

        IF NOT policy_exists THEN
            EXECUTE format(
                'CREATE POLICY "Authenticated read access" ON public.%I FOR SELECT USING (auth.role() = ''authenticated'')',
                tbl.tablename
            );
        END IF;

        RAISE NOTICE 'RLS enabled on: %', tbl.tablename;
    END LOOP;
END $$;
