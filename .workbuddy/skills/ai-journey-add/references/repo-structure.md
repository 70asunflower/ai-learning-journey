# ai-learning-journey — Repository Structure Reference

Verified 2026-07-19 from the live clone at
`D:\Project\workspace\my_github\ai-learning-journey` (branch `master`).

## Top-level layout

```
ai-learning-journey/
├── README.md                 # wiki nav (Resources/Notes/Code/Misc) + Changelog + update guide
├── index.html                # auto-generated single-file reader (from Resources block only)
├── 0-Resources/
│   ├── 0-Index.md            # global tag/date index of ALL resources
│   ├── 1-Official-Docs/
│   ├── 2-Papers/
│   ├── 3-Tutorials/
│   ├── 4-Tools-Frameworks/
│   └── 5-Datasets/
├── 1-Notes/
│   ├── 0-Template.md         # note frontmatter template (topic/date/tags/status)
│   ├── 1-Foundations/
│   ├── 2-Models/
│   │   └── Qwen-Series/
│   ├── 3-Training/
│   └── 4-Deployment/
├── 2-Code/                   # runnable examples (each in its own subfolder)
├── 3-Projects/
├── _misc/
└── scripts/
    ├── generate_index.py     # rebuilds index.html from README Resources block
    └── README.md             # generator usage
```

## README.md block line map (use for nav/changelog edits)

| Line | Element |
|------|---------|
| 8    | `## 🗂️ Wiki Navigation` |
| 11   | `<summary><b>📚 Resources</b></summary>` |
| 14   | `<details> 1-Official-Docs` |
| 22   | `<details> 2-Papers` |
| 29   | `<details> 3-Tutorials` |
| 53   | `<details> 4-Tools & Frameworks` |
| 69   | `<details> 5-Datasets` |
| 80   | `<summary><b>📝 Personal Notes</b></summary>` |
| 83   | `<details> 1-Foundations` |
| 91   | `<details> 2-Models` |
| 98   | `<details> 3-Training` |
| 105  | `<details> 4-Deployment` |
| 116  | `<summary><b>💻 Code & Projects</b></summary>` |
| 208  | `## Changelog` (table starts a few lines below) |

Wiki-nav bullets live **inside** each `<details>` block (between the `<summary>`
line and the next `</details>`). Add new bullets there.

## Frontmatter schemas

### Resource (`0-Resources/**`) — web-indexed
```yaml
---
source: <original URL>
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---
```
End file with: `_Last updated: YYYY-MM-DD_`

### Note (`1-Notes/**`) — NOT web-indexed
Use the REAL schema from `1-Notes/0-Template.md`.
(Note: `README.md` "How to Update → Adding a New Note" incorrectly says "same
frontmatter as resources" — that guidance is wrong; use this instead.)
```yaml
---
topic: <short topic>
date: YYYY-MM-DD
tags: [tag1, tag2]
status: draft        # draft | review | complete
---
```
End file with: `_Last updated: YYYY-MM-DD_`

## 0-Index.md row format

Paths are **relative to `0-Resources/`**. Columns: `Resource | Tags | Date`.
```markdown
| [<Display Name>](<subfolder>/<name>.md) | #tag1 #tag2 #tag3 | YYYY-MM-DD |
```
Sections are `## Official Docs`, `## Papers`, `## Tutorials`, etc. If a section
is empty (`_Empty — add your first ..._`), replace that placeholder line with the
new row.

## Changelog row format (README.md, top of table)
```markdown
| YYYY-MM-DD | Added <name> — one-line description |
```

## Generator behavior
- Command: `python scripts/generate_index.py`
- Reads **only** the `📚 Resources` `<details>` block of `README.md`.
- `index.html` changes when a Resource is added; **unchanged** when only a
  Note/Code entry is added. Both are correct outcomes (idempotent).
- CI (`.github/workflows/build-index.yml`) re-runs it on push.
