# Inbox Management

## Automated Tidy

The inbox tidy script runs every 30 minutes via Windows Task Scheduler.

- **Script:** `scripts/tidy-inbox.py`
- **Launcher:** `scripts/tidy-inbox.vbs` (silent execution)
- **Mode:** Runs with `--dry-run` flag removed for live operation

## Rules

### Never Touch (keep unread)
- `*@stolengoat.com` (from or in CC/To, excluding Tim's own address)
- `d.mealingbland@gmail.com`
- `gtitim@gmail.com`
- `codecraftdesignlab@gmail.com`
- Emails that look personal (no unsubscribe header, single sender, not bulk)

### Mark as Read
- Promotions category
- Social category (LinkedIn, etc.)
- Known automated senders (see `AUTO_SENDERS` in script)
- Newsletters with unsubscribe headers

### Trash
- Known spam patterns (see `TRASH_SENDERS` in script)

## Updating Whitelist

Edit `scripts/tidy-inbox.py` directly:
- **Domains:** Add to `WHITELIST_DOMAINS` list
- **Emails:** Add to `WHITELIST_EMAILS` list
- **Auto senders:** Add substring patterns to `AUTO_SENDERS`
- **Spam:** Add substring patterns to `TRASH_SENDERS`

## Manual Gmail Access

Use the Python API pattern from `tools/gmail/CLAUDE.md`:
- Authentication via service account delegation
- Always create **drafts**, never send directly
- Use `format='metadata'` for listing (faster)
- Decode bodies from base64
