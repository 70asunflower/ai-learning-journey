---
name: add-resource
description: Add a new learning resource to ai-learning-journey, embodied-ai-learning, or ic-chip-design-learning repos following the 3-place update pattern (detail file + subfolder README + global index + wiki nav + changelog)
---

# Add Resource Skill

Adds a new resource to any learning journey repo (**ai-learning-journey**, **embodied-ai-learning**, **ic-chip-design-learning**) using the **3-place update pattern** (plus wiki nav and changelog).

## Steps

### 0. Determine target repo and subfolder

Given a resource and its domain, pick:
- **ai-learning-journey/** — AI/LLM/general
- **embodied-ai-learning/** — robotics, sim-to-real, VLA
- **ic-chip-design-learning/** — RTL, EDA, chip design

Then pick the matching subfolder under `0-Resources/<subfolder>/`:
- **ai-learning-journey**: `1-Official-Docs`, `2-Papers`, `3-Tutorials`, `4-Tools-Frameworks`, `5-Datasets`
- **embodied-ai-learning**: `1-Papers`, `2-Frameworks-Tools`, `3-Datasets`, `4-Tutorials-Courses`, `5-Projects-OpenSource`
- **ic-chip-design-learning**: `1-Books`, `2-Papers`, `3-EDA-Tools`, `4-OpenSource-Projects`, `5-Courses-Tutorials`, `6-Industry-Standards`

If no suitable subfolder exists, use the closest match.

### 1. Create the detail file

Filename: `<name>.md` in `0-Resources/<subfolder>/`.

Naming: lowercase, hyphen-separated.

Start with frontmatter:
```markdown
---
source: <original URL>
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---
```

Then add content:
- Title and one-line summary
- `## Overview` — what it is, key capabilities
- `## Use Cases` / `## Key Points` — bullets
- End with: `_Last updated: YYYY-MM-DD_`

### 2. Update the subfolder README table

File: `0-Resources/<subfolder>/README.md`

Add a row to the existing table. Match the table's column format (e.g. `| Name | Purpose | Link |`). Use the `[详情](<name>.md) · [官方](<URL>)` pattern when a detail file exists.

### 3. Update the global index

File: `0-Resources/0-Index.md`

Add a row under the correct category section:
```
| [<Display Name>](<subfolder>/<name>.md) | `#tag1 #tag2 #tag3` | YYYY-MM-DD |
```

Paths are **relative to `0-Resources/`**. If the target section doesn't exist, add it.

### 4. Update wiki navigation

File: `README.md` at repo root.

Add a bullet inside the matching `<details>` block:
```
- [<Display Name>](0-Resources/<subfolder>/<name>.md) — one-line description
```

### 5. Update changelog

File: `README.md` at repo root.

Add a new row at the **top** of the Changelog table (below the header):
```
| YYYY-MM-DD | Added <name> — one-line description |
```

### 6. Commit and push

Stage all changed files, commit with descriptive message, push to remote.
