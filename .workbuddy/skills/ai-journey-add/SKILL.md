---
name: ai-journey-add
description: Add a resource, note, or code entry to the ai-learning-journey repo and publish it. Trigger when the user says "add a resource / note / paper / tool / dataset / tutorial to ai-learning-journey", "upload this to the repo", or hands over a markdown file or link to file under 0-Resources, 1-Notes, or 2-Code. Rules live in the repo's CONTRIBUTING.md; this skill only carries the operational bits an agent needs (paths, push credentials, verification).
agent_created: true
---

# AI Learning Journey — Add Entry

**The rules are in the repo's `CONTRIBUTING.md`. Read it, don't reinvent it.**
This file only carries what CONTRIBUTING.md can't: the sandbox's push setup and
the exact verification loop.

Default repo path: `D:\Project\workspace\my_github\ai-learning-journey`, branch `master`.

## The one thing to get right

Since the build refactor, **a resource is one file**:

`0-Resources/<subfolder>/<name>.md` with five required frontmatter fields —

```markdown
---
title: 显示名称
summary: 一句话说明（同时用于网页卡片和子目录表格）
source: 原始链接
date: YYYY-MM-DD
tags: [tag1, tag2]
---
```

then `python scripts/build.py`. That regenerates `0-Resources/0-Index.md`,
the subfolder `README.md` table, the root README nav block and `index.html`.
**Hand-editing any of those four is wasted work — the next build overwrites it.**

Notes (`1-Notes/`) are NOT generated: they need the folder README + the
`📝 Personal Notes` nav block edited by hand, and `index.html` must stay
unchanged. See CONTRIBUTING.md.

## Operational notes (verified, keep these)

1. **`gh` CLI is logged in and valid in this sandbox.** Use it as the credential
   helper — do NOT try to read Windows GCM credentials, that is blocked here.
   ```bash
   git -c credential.helper="!gh auth git-credential" push origin master
   ```
2. If push fails with `schannel: failed to receive handshake` (intermittent TLS
   flakiness), retry with the openssl backend:
   ```bash
   git -c http.sslBackend=openssl -c credential.helper="!gh auth git-credential" push origin master
   ```
   A second attempt usually succeeds.
3. **Commit attribution**: `git -c user.name="<current model name>" commit ...`.
   Never write the model name into repo config — the next agent would inherit it.
   The user's own `user.email` stays untouched.
4. **CI** (`.github/workflows/build-index.yml`) re-runs `check_consistency.py`
   and `build.py` on push and auto-commits any drift with `[skip ci]`. A clean
   local build therefore produces **no** bot commit — that is the success signal,
   not a failure.

## Verification (must all pass before reporting done)

```bash
python scripts/check_consistency.py        # expect: 0 error(s), 0 warning(s).
python scripts/normalize_tags.py --check   # expect: Tags already canonical.
python scripts/build.py --check            # expect: All artifacts up to date.
```

If `build.py --check` reports stale files, you forgot to run `build.py` — or you
hand-edited a generated block.

## Tags

`scripts/tags.json` maps deprecated spellings to canonical ones. Before inventing
a tag, check whether an existing canonical tag already covers it; if it is a
synonym, add the pair to `aliases` and use the canonical form.
`python scripts/normalize_tags.py --report` prints frequency + singleton tags
(singletons are candidates for merging, not automatically wrong).

## References

- `references/repo-structure.md` — folder tree, frontmatter examples for both
  schemas, generator behaviour.
- `scripts/publish.sh <repo-path> "<commit-message>"` — build, stage, commit and
  push via the `gh` credential helper in one call.
