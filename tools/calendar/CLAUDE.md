# Google Calendar Integration

**Status:** ACTIVE

## Connection Details

- **Email:** tim.bland@stolengoat.com
- **Auth:** Service account with domain-wide delegation
- **Service account:** pablo-766@pablo-490815.iam.gserviceaccount.com
- **Credentials:** `google-service-account-key.json` (project root, in .gitignore)

## Scopes

- `calendar.readonly` — read calendars and events
- `calendar.events` — create, update, and delete events

## Available Calendars

| Calendar | ID | Used in briefing |
|---|---|---|
| tim.bland@stolengoat.com | `primary` | Yes |
| SG shared calendar | `stolengoat.com_lrke3hfterg2h2h1j0e291du1c@group.calendar.google.com` | Yes |
| SG Content Calendar | `stolengoat.com_3avuo77m5jp6t8ctqv6reg1on0@group.calendar.google.com` | No |
| Hook Office Calendar | `stolengoat.com_ai27qmjsh0lrv75d1hba45f0o4@group.calendar.google.com` | No |
| FLO Calendar | `c_cbefd115ef4fbc52a328da905ef173970c1c5070a5fc77ad146c19d1218c3e44@group.calendar.google.com` | No |
| Product Release Calendar | `stolengoat.com_8qhh9i55h2mlo8du3u6mu56r6s@group.calendar.google.com` | No |
| SG Notable Marketing Moments | `c_h09f580plscep2qcgqegbosma8@group.calendar.google.com` | No |
| School Holidays | `c_363a9de61788a7a3172520fee0fa1e74f07d91da175996e32bf1a94935288d68@group.calendar.google.com` | No |
| Holidays in United Kingdom | `en.uk#holiday@group.v.calendar.google.com` | No |

## How to Use

All Calendar access is via Python with the Google API client. Run scripts with `python3 -c "..."` from Bash.

### Authentication Pattern

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = 'C:/ClaudeProjects/pablo/google-service-account-key.json'
USER = 'tim.bland@stolengoat.com'
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
creds = creds.with_subject(USER)
service = build('calendar', 'v3', credentials=creds)
```

## Capabilities

- **List calendars:** `service.calendarList().list()` — all visible calendars
- **Today's agenda:** `service.events().list(calendarId='primary', timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime')` — events for a date range
- **Get event:** `service.events().get(calendarId='primary', eventId=event_id)` — full event details
- **Create event:** `service.events().insert(calendarId='primary', body=event)` — add an event
- **Update event:** `service.events().update(calendarId='primary', eventId=event_id, body=event)` — modify an event

### Date Format

Use RFC3339 for timeMin/timeMax: `2026-03-20T00:00:00Z` or with timezone `2026-03-20T00:00:00+00:00`.

Tim's timezone is `Europe/London`.

## Rules

- Default to `primary` calendar unless Tim specifies otherwise
- Always show times in Europe/London timezone
- Never delete events without explicit confirmation
- Never display full .env or credentials file contents
