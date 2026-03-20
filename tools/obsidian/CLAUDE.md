# Obsidian Vault Integration

## Vault Path

```
C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian
```

Use this path directly — never search for the vault.

## Available Skills

| Skill | What it does |
|---|---|
| `/note` | Create a quick note in `inbox/` with frontmatter |
| `/bookmark` | Save a URL with summary, tags, and links to `bookmarks/` |
| `/organise` | Scan vault, fix frontmatter, suggest moves, add missing links |
| `/devlog` | Write a daily dev log entry to `journal/` |
| `/generate-ideas` | Research and save business ideas to `business-scout/` |
| `/morning` | Daily briefing drawing on vault data |

## Frontmatter Standard

Every markdown file must have YAML frontmatter:

```yaml
---
title: "Note Title"
date: DD-MM-YYYY
tags:
  - tag-one
  - tag-two
type: note | journal | bookmark | project | reference | idea
---
```

- `date` format is always `DD-MM-YYYY`
- `type` must be one of the listed values
- `tags` is always a list, never inline

## Folder Structure

| Folder | Purpose |
|---|---|
| `inbox/` | Unsorted notes awaiting filing |
| `journal/` | Daily dev logs and journal entries |
| `bookmarks/` | Saved URLs with summaries |
| `projects/` | Project notes and tracking |
| `Ideas/` | Raw ideas and concepts |
| `business-scout/` | Researched business ideas |
| `references/` | Reference material and research |
| `templates/` | Note templates (do not edit directly) |
| `agents/` | Agent-related content |
| `agents/logging/` | All agent activity logs (briefings, actions) |
| `skills/` | Skill definitions for vault-specific workflows |
| `daily-notes/` | Legacy daily notes folder |

## Tag Vocabulary

Reuse existing tags before creating new ones. Common tags in this vault:

- **Type:** devlog, daily, bookmark, project, note, reference, instructions, business-idea
- **Topic:** ai, claude-code, automation, design, tool, research
- **Domain:** guitar-gear, art-supplies, marketing, instagram
- **Meta:** gift-ideas-for-emily, creative-gifts

When in doubt, `Grep` the vault for existing tags before inventing a new one.

## Rules

1. **Wiki-links** — use `[[note-name]]` syntax to link between notes
2. **Never delete** — archive or move, never remove files from the vault
3. **EN-UK spelling** — organise, colour, behaviour, etc.
4. **Log everything** — write agent activity to `agents/logging/`
5. **Reuse tags** — check existing tags before creating new ones
6. **Frontmatter always** — every file gets the standard frontmatter block
7. **Link liberally** — connect related notes with wiki-links wherever possible
