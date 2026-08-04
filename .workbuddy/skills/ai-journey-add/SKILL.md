---
name: ai-journey-add
description: Add a new resource, note, or code entry to the ai-learning-journey knowledge-base repo following its established multi-place update pattern, then regenerate index.html and push. Trigger when the user says "add a resource / note / paper / tool / dataset / tutorial to ai-learning-journey", "upload this to the repo", or hands over a markdown file or link to file under 0-Resources, 1-Notes, or 2-Code.
agent_created: true
---

# AI Learning Journey — Add Entry

Add a learning resource, personal note, or code example to the
**ai-learning-journey** repo and publish it in one pass: create the detail file,
update the subfolder index, update the root wiki nav, update the changelog,
regenerate `index.html`, then commit and push.

## Overview

The repo (`70asunflower/ai-learning-journey`) is a personal AI-learning knowledge
base rendered as a GitHub Pages single-file reader (`index.html`). Content lives
in numbered folders; a Python generator (`scripts/generate_index.py`) rebuilds
`index.html` from the `📚 Resources` block of `README.md`.

Two entry types behave differently and must not be confused:

- **Resource** (`0-Resources/`) — has an external `source:` URL. **IS web-indexed**
  (searchable + tag-filterable in `index.html`). Requires the 4-place update.
- **Note** (`1-Notes/`) — original writing, **no** `source:` URL. **NOT web-indexed**
  (only reachable via README nav + folder README; GitHub Pages still serves the
  raw `.md`). Requires the 3-place update.
- **Code** (`2-Code/`) — runnable example in its own subfolder. Update
  `2-Code/README.md` only; not web-indexed.

## Critical Operational Notes (read before acting)

1. **`gh` CLI is logged in and VALID in the WorkBuddy sandbox** (verified 2026-07-23
   and used for every successful push since): `gh auth status` reports valid with
   `repo` scope. Use it as the git credential helper for push/pull:
   `git -c credential.helper="!gh auth git-credential" push origin master`.
   Do **NOT** use the Windows GCM token approach below — in the sandbox, reading
   GCM credentials is blocked, so it fails; `gh` is the reliable path.
2. **Push via the `gh` credential helper** (non-interactive, token never persisted
   to `.git/config`):
   ```bash
   git -c credential.helper="!gh auth git-credential" push origin master
   ```
   If push fails with `schannel: failed to receive handshake` (intermittent TLS
   flakiness), retry with the openssl backend:
   `git -c http.sslBackend=openssl -c credential.helper="!gh auth git-credential" push origin master`
   (large payloads may need a retry; the 2nd attempt usually succeeds).
   Always verify `git remote -v` shows a clean `https://github.com/...` (no token).
3. **Generator is idempotent and only reads the Resources block.** After any change,
   re-run `python scripts/generate_index.py`. For a Resource add, `index.html`
   changes; for a Note/Code add, `index.html` is unchanged. Either outcome is
   correct — never force a spurious diff.
4. **Default repo path** (resolve at runtime; the user may have it elsewhere):
   `D:\Project\workspace\my_github\ai-learning-journey`. Branch is `master`.
5. **CI** (`.github/workflows/build-index.yml`) regenerates `index.html` on push,
   so committing the regenerated file keeps local and remote consistent.

## Decision Tree

Given the item to add:

- Has an external original URL (docs site, paper, blog, tool homepage, dataset)?
  → **Resource** → pick subfolder → follow Workflow A.
- Is it the user's own writing/summary with no external source?
  → **Note** → pick subfolder → follow Workflow B.
- Is it runnable code (script + requirements + README)?
  → **Code** → `2-Code/<name>/` → update `2-Code/README.md` only.

### Subfolder map (verified 2026-07-19)

`0-Resources/`: `1-Official-Docs` · `2-Papers` · `3-Tutorials` ·
`4-Tools-Frameworks` · `5-Datasets`

`1-Notes/`: `1-Foundations` · `2-Models` (incl. `Qwen-Series`) ·
`3-Training` · `4-Deployment`

If no exact subfolder fits, use the closest match.

## Workflow A — Add a Resource (4 places + regen + push)

### 1. Create the detail file
Path: `0-Resources/<subfolder>/<name>.md`
Name: lowercase, hyphen-separated (e.g. `vllm-docs-zh.md`).
Frontmatter (Resource schema):
```markdown
---
source: <original URL>
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
---
```
Body: title + one-line summary, then `## Overview` / `## Key Points` /
`## Use Cases` as relevant. End with: `_Last updated: YYYY-MM-DD_`

### 2. Update subfolder README table
File: `0-Resources/<subfolder>/README.md`
Append a row matching that table's column format. Use
`[详情](<name>.md) · [官方](<URL>)` when a detail file exists.

### 3. Update the global index
File: `0-Resources/0-Index.md`
Add a row under the matching category section:
`| [<Display Name>](<subfolder>/<name>.md) | #tag1 #tag2 #tag3 | YYYY-MM-DD |`
Paths are relative to `0-Resources/`. Add the section if missing.
**Then bump the `_Last updated: YYYY-MM-DD_` footer at the bottom of the file**
(it is the source of the `generated` date in `index.html`; `check_consistency.py`
errors if it is missing, so always keep it current).

### 4. Update root wiki nav + changelog
File: `README.md` (repo root).
- Wiki nav: add a bullet inside the matching `<details>` block under
  `📚 Resources`:
  `- [<Display Name>](0-Resources/<subfolder>/<name>.md) — one-line description`
- Changelog: add a new row **at the top** of the table (below the header):
  `| YYYY-MM-DD | Added <name> — one-line description |`

### 5. Regenerate, commit, push
Run `python scripts/generate_index.py`; `index.html` SHOULD change. Stage all
changed files (detail file, subfolder README, `0-Index.md`, root `README.md`,
`index.html`), commit, push via the `gh` credential helper (see Operational
Note 2).

## Workflow B — Add a Note (3 places + regen + push)

### 1. Create the detail file
Path: `1-Notes/<subfolder>/<name>.md`
Name: lowercase, hyphen-separated slug; keep the Chinese title in the H1.
Frontmatter (Note schema — **differs from the repo README's "same as resource"
suggestion; use this real schema from `1-Notes/0-Template.md`**):
```markdown
---
topic: <short topic>
date: YYYY-MM-DD
tags: [tag1, tag2]
status: draft   # or: review / complete
---
```
Body: the user's understanding, code experiments, gotchas. End with
`_Last updated: YYYY-MM-DD_`

### 2. Update folder README index
File: `1-Notes/<subfolder>/README.md`
Add a row/link to the new note.

### 3. Update root wiki nav + changelog
File: `README.md` (repo root).
- Wiki nav: add a bullet inside the matching `<details>` block under
  `📝 Personal Notes`:
  `- [<Display Name>](1-Notes/<subfolder>/<name>.md) — one-line description`
- Changelog: new row at the top of the table.

### 4. Regenerate, commit, push
Run `python scripts/generate_index.py`; `index.html` should be **unchanged**
(notes are not web-indexed). Stage the detail file, folder README, and root
`README.md`; commit; push via the `gh` credential helper (see Operational
Note 2). Do **not** invent an `index.html` diff.

## Verification Checklist

- [ ] Detail file present with correct frontmatter + `_Last updated:` line.
- [ ] Subfolder README updated.
- [ ] Root `README.md` nav + changelog updated.
- [ ] For Resources: `0-Resources/0-Index.md` updated (row AND `_Last updated` footer) AND `index.html` regenerated.
- [ ] For Notes: `index.html` confirmed unchanged (no spurious diff).
- [ ] `git remote -v` clean (no embedded token) before/after push.
- [ ] Push succeeded to `origin/master`.

## References

- `references/repo-structure.md` — verified folder tree, README block line map,
  `0-Index.md` row format, and frontmatter examples for both schemas.
- `scripts/publish.sh <repo-path> "<commit-message>"` — regenerates `index.html`,
  stages, commits, and pushes via the `gh` credential helper in one call.
