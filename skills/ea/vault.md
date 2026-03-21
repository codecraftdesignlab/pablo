# Obsidian Vault Access

## Path

```
C:\Users\timbl\stolen goat Dropbox\tim bland\Obsidian
```

Full integration guide: `tools/obsidian/CLAUDE.md`

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
| `agents/logging/` | All agent activity logs |
| `daily-notes/` | Legacy daily notes folder |

## Frontmatter Standard

```yaml
---
title: "Note Title"
date: DD-MM-YYYY
tags:
  - tag-one
type: note | journal | bookmark | project | reference | idea
---
```

## Tag Vocabulary

Reuse existing tags. Common ones:
- **Type:** devlog, daily, bookmark, project, note, reference, instructions, business-idea
- **Topic:** ai, claude-code, automation, design, tool, research
- **Domain:** guitar-gear, art-supplies, marketing, instagram
- **Meta:** gift-ideas-for-emily, creative-gifts

When in doubt, Grep the vault for existing tags before inventing new ones.

## Rules

1. **Wiki-links** — use `[[note-name]]` syntax
2. **Never delete** — archive or move only
3. **EN-UK spelling** — organise, colour, behaviour
4. **Log everything** — agent activity to `agents/logging/`
5. **Reuse tags** — check before creating
6. **Frontmatter always** — every file gets the standard block
7. **Link liberally** — connect related notes with wiki-links
