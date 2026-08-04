#!/usr/bin/env python3
"""Consistency checker for the ai-learning-journey repo.

Source of truth = on-disk resource .md files under 0-Resources/<sub>/.
Validates that every resource is registered in:
  - its subfolder README.md table
  - 0-Resources/0-Index.md
  - the root README.md wiki navigation
and that every registered link resolves to a real file. Also checks
frontmatter basics, the `_Last updated` footer, internal dead links, and
Changelog sanity.

ERROR   -> non-zero exit (CI should fail the build / refuse to publish)
WARNING -> printed, non-fatal
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_ROOT = os.path.join(ROOT, "0-Resources")
SUBDIRS = ["1-Official-Docs", "2-Papers", "3-Tutorials", "4-Tools-Frameworks", "5-Datasets"]

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def exists(rel):
    return os.path.isfile(os.path.join(ROOT, rel))


# ---------- frontmatter ----------
def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def _clean_tag(t):
    t = t.strip().strip("`").strip()
    if t.startswith("#"):
        t = t[1:].strip()
    return t


def parse_tags(s):
    if not s:
        return []
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    if "," in s:
        parts = [p.strip() for p in s.split(",")]
    else:
        parts = s.split()
    return [_clean_tag(p) for p in parts if p.strip()]


# ---------- disk resources ----------
disk = {}  # rel -> {title, tags, date, sub}
for sub in SUBDIRS:
    d = os.path.join(RES_ROOT, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md") or fn == "README.md":
            continue
        rel = f"0-Resources/{sub}/{fn}"
        with open(os.path.join(d, fn), encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        if "title" not in fm and "source" not in fm:
            err(f"{rel}: missing frontmatter 'title' or 'source'")
        tags = parse_tags(fm.get("tags"))
        has_footer = bool(re.search(r"_Last updated:\s*\d{4}-\d{2}-\d{2}_", text))
        if not has_footer:
            warn(f"{rel}: missing '_Last updated: YYYY-MM-DD_' footer")
        if not fm.get("source"):
            warn(f"{rel}: missing 'source' frontmatter")
        disk[rel] = {"title": fm.get("title", ""), "tags": tags, "sub": sub}


# ---------- 0-Index.md (paths are relative to 0-Resources/) ----------
index_entries = {}  # normalized rel -> {tags}
idx_path = os.path.join(RES_ROOT, "0-Index.md")
if os.path.isfile(idx_path):
    with open(idx_path, encoding="utf-8") as f:
        idx_text = f.read()
    # The `_Last updated` footer is the source of the generated date in
    # index.html (generate_index.generated_date reads it). If it is missing,
    # the generator falls back to today() -> CI would produce a diff every run.
    if not re.search(r"_Last updated:\s*\d{4}-\d{2}-\d{2}_", idx_text):
        err("0-Resources/0-Index.md: missing '_Last updated: YYYY-MM-DD_' footer "
            "(required: index.html generated date is derived from it)")
    for line in idx_text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) < 3:
            continue
        m = re.match(r"^\[([^\]]+)\]\(([^)]+)\)$", cells[0])
        if not m:
            continue
        relp = "0-Resources/" + m.group(2).strip()
        tags = [_clean_tag(t) for t in cells[1].split() if t.strip()]
        index_entries[relp] = {"tags": tags}

# ---------- subfolder READMEs ----------
sub_entries = {sub: set() for sub in SUBDIRS}
for sub in SUBDIRS:
    p = os.path.join(RES_ROOT, sub, "README.md")
    if not os.path.isfile(p):
        continue
    with open(p, encoding="utf-8") as f:
        for line in f:
            for m in re.finditer(r"\[[^\]]+\]\(([^)]+\.md)\)", line):
                rp = m.group(1).strip().lstrip("./")
                if not rp.startswith("0-Resources/"):
                    rp = f"0-Resources/{sub}/{rp}"
                if not rp.endswith("README.md"):
                    sub_entries[sub].add(rp)

# ---------- root README nav ----------
nav_links = set()
root_readme = os.path.join(ROOT, "README.md")
if os.path.isfile(root_readme):
    with open(root_readme, encoding="utf-8") as f:
        for line in f:
            for m in re.finditer(r"\]\(([^)]+\.md)\)", line):
                rp = m.group(1).strip()
                if rp.startswith("0-Resources/") and not rp.endswith("README.md") \
                        and rp != "0-Resources/0-Index.md":
                    nav_links.add(rp)

# ---------- cross checks: every disk resource must be registered ----------
for rel, info in disk.items():
    if rel not in index_entries:
        err(f"{rel}: on disk but MISSING from 0-Index.md")
    if rel not in sub_entries.get(info["sub"], set()):
        err(f"{rel}: on disk but MISSING from subfolder README.md")
    if rel not in nav_links:
        err(f"{rel}: on disk but MISSING from root README navigation")

# ---------- every registered entry must exist on disk ----------
registered = set(index_entries) | nav_links | {p for s in sub_entries for p in sub_entries[s]}
for rel in registered:
    if rel not in disk:
        if exists(rel):
            warn(f"{rel}: registered but not parsed as a resource file")
        else:
            err(f"{rel}: registered but FILE DOES NOT EXIST ({rel})")

# ---------- tag drift ----------
# NOTE: 0-Index tags are a curated subset of the frontmatter `tags` field by
# design, so a strict equality compare only produces noise. Skipped on purpose.

# ---------- internal dead links (all .md) ----------
# Skip tooling dirs (.claude/.workbuddy) whose placeholder links such as
# 0-Resources/<sub>/<name>.md contain angle brackets and are not real targets.
LINK_RE = re.compile(r"\]\(((?:0-Resources|1-Notes|2-Code|3-Projects|_misc)/[^)]+\.md)\)")
for dirpath, _, files in os.walk(ROOT):
    if ".git" in dirpath or ".claude" in dirpath or ".workbuddy" in dirpath:
        continue
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(dirpath, fn)
        with open(fp, encoding="utf-8") as f:
            text = f.read()
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if "<" in target or ">" in target:
                continue
            if not exists(target):
                err(f"{os.path.relpath(fp, ROOT)}: dead internal link -> {target}")

# ---------- Changelog sanity ----------
if os.path.isfile(root_readme):
    with open(root_readme, encoding="utf-8") as f:
        lines = f.readlines()
    in_cl = False
    rows = []
    for line in lines:
        s = line.strip()
        if s.startswith("## "):
            if in_cl:
                break
            if "Changelog" in s:
                in_cl = True
            continue
        if in_cl:
            m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|", s)
            if m:
                rows.append((m.group(1), s))
    seen = set()
    for _date, row in rows:
        if row in seen:
            err(f"README Changelog: duplicate row -> {row}")
        seen.add(row)
    # NOTE: the repo convention is "add a new row below for each update"
    # (see README "How to Update"), so the log is append-ordered, not strictly
    # date-descending. We intentionally do NOT warn on ordering here.

# ---------- report ----------
for e in errors:
    print(f"ERROR: {e}")
for w in warnings:
    print(f"WARN:  {w}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
sys.exit(1 if errors else 0)
