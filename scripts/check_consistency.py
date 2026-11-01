#!/usr/bin/env python3
"""Semantic checks on the resource files themselves.

Artifact sync (0-Index.md / subfolder tables / README nav / index.html) is NOT
checked here — `scripts/build.py --check` owns that, and duplicating the logic
in two places is how two tools drift apart. This script only validates what a
generator cannot infer.

  ERROR   -> non-zero exit (CI fails)
  WARNING -> printed, non-fatal

Checks
  * every resource file has complete frontmatter (title/summary/source/date/tags)
  * filenames follow the lowercase-hyphen convention
  * no deprecated tag alias (see scripts/tags.json)
  * no dead internal links (markdown `](...)` and HTML `<a href>`)
  * README changelog: no duplicate rows, date-descending
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES_ROOT = os.path.join(ROOT, "0-Resources")
SUBDIRS = ["1-Books", "2-Papers", "3-EDA-Tools", "4-OpenSource-Projects",
           "5-Courses-Tutorials", "6-Industry-Standards", "7-Videos"]
REQUIRED = ("title", "summary", "source", "date", "tags")
FNAME_OK = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def exists(rel):
    return os.path.isfile(os.path.join(ROOT, rel))


def parse_frontmatter(text):
    if not text.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            v = v.strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fm[k.strip()] = v
    return fm


def parse_tags(s):
    if not s:
        return []
    s = s.strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [p.strip().strip("`").lstrip("#").strip() for p in s.split(",") if p.strip()]


# ---------- resource files ----------
disk = {}
for sub in SUBDIRS:
    d = os.path.join(RES_ROOT, sub)
    if not os.path.isdir(d):
        continue
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md") or fn == "README.md":
            continue
        rel = f"0-Resources/{sub}/{fn}"
        if not FNAME_OK.match(fn):
            warn(f"{rel}: filename not lowercase-hyphenated (e.g. my-resource.md)")
        with open(os.path.join(d, fn), encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        missing = [k for k in REQUIRED if not fm.get(k)]
        if missing:
            err(f"{rel}: frontmatter missing {', '.join(missing)} "
                f"(all of title/summary/source/date/tags are required — they drive "
                f"0-Index, the subfolder table, the README nav and index.html)")
        if fm.get("date") and not re.match(r"^\d{4}-\d{2}-\d{2}$", fm["date"]):
            err(f"{rel}: 'date' not YYYY-MM-DD: {fm['date']}")
        # No `_Last updated` footer check: `date` in frontmatter is the only date
        # that drives anything. The footer rule was never followed here (0/17
        # files had one), so a warning on every file would just be noise.
        disk[rel] = {"tags": parse_tags(fm.get("tags"))}

# ---------- tag vocabulary ----------
registry = os.path.join(ROOT, "scripts", "tags.json")
if os.path.isfile(registry):
    with open(registry, encoding="utf-8") as f:
        ALIASES = json.load(f).get("aliases", {})
    for rel, info in sorted(disk.items()):
        for t in info["tags"]:
            if t in ALIASES:
                err(f"{rel}: tag '{t}' is an alias — use '{ALIASES[t]}' "
                    f"(run scripts/normalize_tags.py)")

# ---------- dead internal links ----------
# Tooling dirs are skipped: their placeholder links (0-Resources/<sub>/<name>.md)
# contain angle brackets and are not real targets.
LINK_RE = re.compile(r"\]\(((?:0-Resources|1-Notes|2-Code|3-Projects|_misc)/[^)]+\.md)\)")
HREF_RE = re.compile(r'href="((?:0-Resources|1-Notes|2-Code|3-Projects|_misc)/[^"]+\.md)"')
IMG_RE = re.compile(r'(?:src|srcset)="(assets/[^"]+)"')
for dirpath, _, files in os.walk(ROOT):
    if ".git" in dirpath or ".claude" in dirpath or ".workbuddy" in dirpath:
        continue
    for fn in files:
        if not fn.endswith(".md"):
            continue
        fp = os.path.join(dirpath, fn)
        with open(fp, encoding="utf-8") as f:
            text = f.read()
        rel_fp = os.path.relpath(fp, ROOT)
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if "<" in target or ">" in target:
                continue
            if not exists(target):
                err(f"{rel_fp}: dead internal link -> {target}")
        for m in HREF_RE.finditer(text):
            if not exists(m.group(1)):
                err(f"{rel_fp}: dead internal link -> {m.group(1)} (html href)")
        for m in IMG_RE.finditer(text):
            if not exists(m.group(1)):
                err(f"{rel_fp}: missing image -> {m.group(1)}")

# ---------- changelog ----------
root_readme = os.path.join(ROOT, "README.md")
if os.path.isfile(root_readme):
    with open(root_readme, encoding="utf-8") as f:
        lines = f.readlines()
    in_cl, rows = False, []
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
    # Convention: newest row on top. Append-at-bottom ordering silently drifted
    # out of order once, so it is enforced now.
    for i in range(len(rows) - 1):
        if rows[i][0] < rows[i + 1][0]:
            err(f"README Changelog: not date-descending — {rows[i][0]} appears "
                f"above {rows[i + 1][0]} (insert newest rows at the top)")

# ---------- report ----------
for e in errors:
    print(f"ERROR: {e}")
for w in warnings:
    print(f"WARN:  {w}")
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
sys.exit(1 if errors else 0)
