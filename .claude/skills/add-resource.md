---
name: add-resource
description: Add a learning resource to one of the three learning-journey repos (ai-learning-journey, embodied-ai-learning, ic-chip-design-learning). Use when the user says add/collect/save a resource, paper, tool, dataset, course, or blog to a learning-journey repo. Routes to the target repo and defers to that repo's own CONTRIBUTING.md for the exact steps.
---

# Add Resource

Three sibling repos share a structure but **not** the same tooling. This skill
only decides *where* the resource goes; the target repo's `CONTRIBUTING.md` is
the authority for *how* to add it.

## 1. Pick the repo

| Repo | Domain |
|------|--------|
| `ai-learning-journey` | AI / LLM / AI Infra / agent |
| `embodied-ai-learning` | robotics, sim-to-real, VLA |
| `ic-chip-design-learning` | RTL, EDA, chip design |

## 2. Pick the subfolder

- **ai-learning-journey**: `1-Official-Docs` · `2-Papers` · `3-Tutorials` ·
  `4-Tools-Frameworks` · `5-Datasets`
- **embodied-ai-learning**: `1-Papers` · `2-Frameworks-Tools` · `3-Datasets` ·
  `4-Tutorials-Courses` · `5-Projects-OpenSource`
- **ic-chip-design-learning**: `1-Books` · `2-Papers` · `3-EDA-Tools` ·
  `4-OpenSource-Projects` · `5-Courses-Tutorials` · `6-Industry-Standards` ·
  `7-Videos`

Closest match if nothing fits exactly.

## 3. Follow that repo's CONTRIBUTING.md

Read it before writing anything — the three repos differ:

- **ai-learning-journey** and **ic-chip-design-learning** are both
  generator-driven. You write ONE `.md` with full frontmatter
  (`title`/`summary`/`source`/`date`/`tags`) and run `python scripts/build.py`;
  `0-Index.md`, the subfolder table, the README nav, `index.html` and the
  roadmap SVGs are all generated. **Never hand-edit those.**
- **embodied-ai-learning** is still hand-maintained (detail file + subfolder
  README + global index + wiki nav + changelog) — its CONTRIBUTING.md says which.

## 4. Verify before reporting done

Run whatever the repo's CONTRIBUTING.md lists under its pre-commit self-check.
For ai-learning-journey that is:

```bash
python scripts/check_consistency.py   # 0 error(s), 0 warning(s)
python scripts/build.py --check       # "All artifacts up to date."
```
