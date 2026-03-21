# Calendar Management

## Access

Python API via service account delegation. Full details in `tools/calendar/CLAUDE.md`.

## Calendars

| Calendar | ID | In Briefing |
|---|---|---|
| Tim's primary | `primary` | Yes |
| SG shared | `stolengoat.com_lrke3hfterg2h2h1j0e291du1c@group.calendar.google.com` | Yes |
| SG Content | `stolengoat.com_3avuo77m5jp6t8ctqv6reg1on0@group.calendar.google.com` | No |
| Hook Office | `stolengoat.com_ai27qmjsh0lrv75d1hba45f0o4@group.calendar.google.com` | No |
| FLO | `c_cbefd115ef4fbc52a328da905ef173970c1c5070a5fc77ad146c19d1218c3e44@group.calendar.google.com` | No |
| Product Release | `stolengoat.com_8qhh9i55h2mlo8du3u6mu56r6s@group.calendar.google.com` | No |
| SG Notable Marketing Moments | `c_h09f580plscep2qcgqegbosma8@group.calendar.google.com` | No |
| School Holidays | `c_363a9de61788a7a3172520fee0fa1e74f07d91da175996e32bf1a94935288d68@group.calendar.google.com` | No |
| UK Holidays | `en.uk#holiday@group.v.calendar.google.com` | No |

## Briefing Pattern

For `/morning` and other briefings, query both `primary` and the SG shared calendar:

```python
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone('Europe/London')
now = datetime.now(tz)
start = now.replace(hour=0, minute=0, second=0).isoformat()
end = (now.replace(hour=0, minute=0, second=0) + timedelta(days=1)).isoformat()

events = service.events().list(
    calendarId='primary',
    timeMin=start, timeMax=end,
    singleEvents=True, orderBy='startTime'
).execute().get('items', [])
```

## Rules

- Default to `primary` calendar unless Tim specifies otherwise
- Always show times in Europe/London timezone
- Never delete events without explicit confirmation
- Tim's timezone: `Europe/London`
- Date format for API: RFC3339 (`2026-03-20T00:00:00+00:00`)
