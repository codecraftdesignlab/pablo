# Gmail Integration

**Status:** ACTIVE

## Connection Details

- **Email:** tim.bland@stolengoat.com
- **Auth:** Service account with domain-wide delegation
- **Service account:** pablo-766@pablo-490815.iam.gserviceaccount.com
- **Credentials:** `google-service-account-key.json` (project root, in .gitignore)

## Scopes

- `gmail.readonly` — read emails and labels
- `gmail.compose` — create drafts
- `gmail.modify` — modify labels, mark read/unread

## How to Use

All Gmail access is via Python with the Google API client. Run scripts with `python3 -c "..."` from Bash.

### Authentication Pattern

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = 'C:/ClaudeProjects/pablo/google-service-account-key.json'
USER = 'tim.bland@stolengoat.com'
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
creds = creds.with_subject(USER)
service = build('gmail', 'v1', credentials=creds)
```

## Capabilities

- **Read inbox:** `service.users().messages().list(userId='me', q='is:unread')` — list and read messages
- **Search:** `service.users().messages().list(userId='me', q='from:someone@example.com subject:thing')` — Gmail search syntax
- **Get message:** `service.users().messages().get(userId='me', id=msg_id, format='full')` — full message with headers and body
- **Draft replies:** `service.users().drafts().create(userId='me', body=draft)` — create draft emails
- **Labels:** `service.users().labels().list(userId='me')` — list all labels
- **Modify:** `service.users().messages().modify(userId='me', id=msg_id, body={'addLabelIds': [], 'removeLabelIds': []})` — add/remove labels

## Rules

- Never send emails directly — always create **drafts** for Tim to review
- Never display full .env or credentials file contents
- Decode message bodies from base64 (`base64.urlsafe_b64decode`)
- Use `format='metadata'` with `metadataHeaders=['From','To','Subject','Date']` for listing (faster than full)
