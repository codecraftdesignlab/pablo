# Mailchimp Integration

**Status:** ACTIVE

## Connection Details

- **API Key:** stored in `.env` as `MAILCHIMP_API_KEY`
- **Data Centre:** `us1` (derived from API key suffix)
- **Base URL:** `https://us1.api.mailchimp.com/3.0`
- **Auth:** HTTP Basic (`anystring`, `API_KEY`)

## Audiences

| Audience | List ID | Members | Purpose |
|---|---|---|---|
| SG Mailing List | `6b5b431c5b` | ~46,800 | Stolen Goat newsletter subscribers |
| VeloVixen | `d3fdef7bd4` | ~2,000 | VeloVixen subscribers |

## How to Use

```python
import sys
sys.path.insert(0, 'C:/ClaudeProjects/pablo')
from tools.mailchimp.mailchimp import (
	get_all_members, get_member, update_member,
	set_tags, subscriber_hash, submit_batch,
	get_merge_fields, create_merge_field,
)

# Get all subscribed members
members = get_all_members()
print(f"{len(members)} subscribers")

# Get a single member
member = get_member("someone@example.com")
print(member['tags'], member['merge_fields'])

# Add tags
set_tags("someone@example.com", [
	{"name": "vip", "status": "active"},
	{"name": "dormant", "status": "inactive"},  # removes this tag
])

# Update merge fields
update_member("someone@example.com", {
	"merge_fields": {"LAST_ORDER": "2026-03-01", "ORDER_COUNT": "5"}
})
```

## Subscriber Hash

Mailchimp identifies members by MD5 hash of lowercase email:
```python
import hashlib
h = hashlib.md5("someone@example.com".lower().encode()).hexdigest()
```

## Batch API

For bulk operations (>100 subscribers), use the batch API:
- Max 500 operations per batch
- Each operation is a full API call (method, path, body as JSON string)
- Poll `get_batch_status(batch_id)` until `status == "finished"`

## Merge Fields (SG Mailing List)

| Tag | Type | Name | Source |
|---|---|---|---|
| FNAME | text | First Name | Existing |
| LNAME | text | Last Name | Existing |
| COLLECTION | text | Collection | Existing |
| LAST_ORDER | text | Last Order Date | Segmentation script |
| ORDER_COUNT | text | Order Count | Segmentation script |
| TOTAL_SPEND | text | Total Spend | Segmentation script |
| LIFECYCLE | text | Lifecycle Stage | Segmentation script |
| INTERESTS | text | Interests | Segmentation script |

## Rate Limits

- 10 concurrent connections max
- ~10 requests/second
- Batch API recommended for bulk updates

## Rules

1. **Never delete subscribers** — only add/remove tags or update merge fields
2. **Use batch API for bulk operations** — individual calls for >100 subscribers will hit rate limits
3. **Do not expose the API key** — it's in `.env`, never log or display it
