# ai-learning-journey — Repository Structure Reference

Updated 2026-11-01. The repo is now **generator-driven**: resource frontmatter is
the only hand-maintained data, everything else is built.

## Top-level layout

```
ai-learning-journey/
├── README.md                 # front door + nav (Resources nav is GENERATED) + changelog
├── CONTRIBUTING.md           # authoritative how-to-add rules
├── index.html                # GENERATED single-file reader
├── assets/preview.png        # README screenshot of index.html
├── 0-Resources/
│   ├── 0-Index.md            # GENERATED tag/date index of all resources
│   ├── 1-Official-Docs/
│   ├── 2-Papers/
│   ├── 3-Tutorials/
│   ├── 4-Tools-Frameworks/
│   └── 5-Datasets/
├── 1-Notes/                  # hand-maintained, NOT web-indexed
│   ├── 0-Template.md
│   ├── 1-Foundations/  2-Models/  3-Training/  4-Deployment/
├── 2-Code/  3-Projects/  _misc/
└── scripts/
    ├── build.py              # generates everything below
    ├── check_consistency.py  # semantic checks
    ├── normalize_tags.py     # tag alias rewrite
    ├── tags.json             # alias -> canonical registry
    └── README.md
```

## Generated vs hand-written

| Path | Owner |
|------|-------|
| `0-Resources/0-Index.md` | **generated** (whole file) |
| `0-Resources/<sub>/README.md` | **generated** between `<!-- BUILD:TABLE:START/END -->` |
| `README.md` Resources nav | **generated** between `<!-- BUILD:NAV:START/END -->` |
| `index.html` | **generated** (whole file) |
| everything else | hand-written |

Never hand-edit a generated block — `build.py` overwrites it.

## Frontmatter schemas

### Resource (`0-Resources/**`) — all five fields required
```yaml
---
title: 显示名称
summary: 一句话说明（网页卡片 + 子目录表格共用）
source: <original URL>
date: YYYY-MM-DD
tags: [tag1, tag2]
---
```
End file with: `_Last updated: YYYY-MM-DD_`

`check_consistency.py` errors if any of the five is missing — they drive
0-Index, the subfolder table, the README nav and index.html.

### Note (`1-Notes/**`) — NOT web-indexed
Use the schema from `1-Notes/0-Template.md` (`topic`/`status`, not `source`).
```yaml
---
topic: <short topic>
date: YYYY-MM-DD
tags: [tag1, tag2]
status: reading      # reading | writing | done
---
```
End file with: `_Last updated: YYYY-MM-DD_`

## What the generated output looks like

`0-Index.md` rows (paths relative to `0-Resources/`, tag cell backticked):
```markdown
| [<title>](<subfolder>/<name>.md) | `#tag1 #tag2` | YYYY-MM-DD |
```

Subfolder table:
```markdown
| Resource | Description | Date |
| :--- | :--- | :--- |
| [<title>](<name>.md) | <summary> | YYYY-MM-DD |
```

README nav bullet:
```markdown
- [<title>](0-Resources/<subfolder>/<name>.md) — <summary>
```
plus one `- [📄 <Label> Index](...)` per category and a `📋 Full Resource Index`
line. The Resources nav lives inside `<details open><summary><b>📚 Resources</b></summary>`.

`index.html` `generated` date = max resource `date` (no footer to bump anywhere).

## Changelog row format (README.md, top of table)
```markdown
| YYYY-MM-DD | Added <name> — one-line description |
```
Date-descending, enforced by `check_consistency.py`.

## Scripts

```bash
python scripts/build.py             # regenerate all four artifacts
python scripts/build.py --check     # exit 1 if any artifact is stale
python scripts/check_consistency.py # semantic checks (not artifact sync)
python scripts/normalize_tags.py --check|--report
```

Division of labour: `check_consistency.py` validates the *sources*,
`build.py --check` validates the *outputs*. Neither duplicates the other.
