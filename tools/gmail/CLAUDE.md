# Gmail Integration

**Status:** PENDING

## Planned Capabilities

- Read and summarise recent emails
- Draft replies with Tim's tone
- Flag urgent messages in morning briefings
- Search emails by sender, subject, or date range

## Setup Steps (When Ready)

1. Enable Gmail API in Google Cloud Console
2. Configure OAuth2 or service account credentials
3. Store credentials in `google-service-account-key.json` (project root)
4. Set status to `active` in `config/accounts.yaml`
5. Add Gmail sections to morning briefing and other workflows

## Authentication

Uses Google Workspace API via service account. Credentials file is in `.gitignore` — never commit it.
