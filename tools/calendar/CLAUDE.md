# Google Calendar Integration

**Status:** PENDING

## Planned Capabilities

- Fetch today's agenda for morning briefings
- Check availability for scheduling
- Create and update calendar events
- Send meeting reminders and prep notes

## Setup Steps (When Ready)

1. Enable Google Calendar API in Google Cloud Console
2. Configure OAuth2 or service account credentials
3. Store credentials in `google-service-account-key.json` (project root)
4. Set status to `active` in `config/accounts.yaml`
5. Add calendar sections to morning briefing and other workflows

## Authentication

Uses Google Workspace API via service account. Credentials file is in `.gitignore` — never commit it.
