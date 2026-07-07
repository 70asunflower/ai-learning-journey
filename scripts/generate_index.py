#!/usr/bin/env python3
"""Generate a single-file index.html from README.md wiki navigation + 0-Index.md tags.

Usage:
    python scripts/generate_index.py

The script parses the "📚 Resources" block of README.md (every <details> category and
its markdown links) and enriches each item with tags scraped from 0-Resources/0-Index.md.
Output: index.html at repo root (self-contained: embedded CSS + JS, no dependencies).

After adding a resource, just re-run this script — no need to edit index.html by hand.
"""
import re
import json
import datetime
import pathlib

REPO = "70asunflower/ai-learning-journey"
BRANCH = "master"  # default branch of this repo
ROOT = pathlib.Path(__file__).resolve().parent.parent

SIBLINGS = [
    {"name": "Embodied AI", "url": "https://70asunflower.github.io/embodied-ai-learning/"},
    {"name": "IC Chip Design", "url": "https://70asunflower.github.io/ic-chip-design-learning/"},
]

readme = (ROOT / "README.md").read_text(encoding="utf-8")
index_md = (ROOT / "0-Resources" / "0-Index.md").read_text(encoding="utf-8")

BLOB = f"https://github.com/{REPO}/blob/{BRANCH}/"


def normalize(p: str) -> str:
    p = p.strip()
    if p.startswith("0-Resources/"):
        p = p[len("0-Resources/"):]
    return p


def prettify(cat: str) -> str:
    cat = re.sub(r"^\d+-", "", cat)
    return cat.replace("-", " ").strip()


# ---- 1. tags from 0-Index.md (table: | [Name](path) | #tags | date |) ----
tags_by_path: dict[str, list[str]] = {}
for line in index_md.splitlines():
    if not (line.strip().startswith("|") and "](" in line):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 2:
        continue
    lm = re.search(r"\]\(([^)]+)\)", cells[0])
    if not lm:
        continue
    path = normalize(lm.group(1))
    tags = re.findall(r"#([\w\-]+)", cells[1])
    tags_by_path[path] = tags


# ---- 2. resources from README.md (inside 📚 Resources block) ----
categories: list[dict] = []
cat_map: dict[str, list[dict]] = {}
stack: list[str | None] = []

for line in readme.splitlines():
    s = line.strip()
    if s.startswith("<details"):
        stack.append(None)
        continue
    m = re.match(r"<summary>(.*?)</summary>", s)
    if m:
        stack[-1] = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        continue
    if s == "</details>":
        if stack:
            stack.pop()
        continue
    if not stack or "Resources" not in (stack[0] or ""):
        continue
    cat = next((x for x in reversed(stack) if x and re.match(r"^\d+-", x)), None)
    if not cat:
        continue
    lm = re.search(r"\[([^\]]+)\]\(([^)]+)\)", line)
    if not lm:
        continue
    title = lm.group(1).strip()
    url = lm.group(2).strip()
    desc = re.sub(r"^[\s—\-–]+", "", line[lm.end():].strip())
    full = url if url.startswith(("http://", "https://")) else BLOB + url
    tags = tags_by_path.get(normalize(url), [])
    is_index = title.startswith(("📄", "📋", "📁"))
    name = prettify(cat)
    if name not in cat_map:
        items: list[dict] = []
        cat_map[name] = items
        categories.append({"name": name, "items": items})
    cat_map[name].append(
        {"title": title, "url": full, "desc": desc, "tags": tags, "index": is_index}
    )

data = {
    "repo": REPO,
    "branch": BRANCH,
    "generated": datetime.date.today().isoformat(),
    "categories": categories,
}

HTML = r"""<!DOCTYPE html>
<html lang="zh" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Learning Journey · Resource Index</title>
<style>
:root{
  --bg:#0f1117; --panel:rgba(23,26,35,.82); --card:#1b2030; --card-hover:#222a3d;
  --text:#e7eaf1; --muted:#94a0b4; --accent:#6ea8fe; --accent2:#7ee0c0;
  --border:#2a3142; --chip:#222a3a; --chip-active:#6ea8fe; --shadow:0 6px 24px rgba(0,0,0,.35);
}
[data-theme="light"]{
  --bg:#f5f7fc; --panel:rgba(255,255,255,.85); --card:#ffffff; --card-hover:#f0f4ff;
  --text:#1a2233; --muted:#5b6678; --accent:#2f6fed; --accent2:#1aa179;
  --border:#e4e9f2; --chip:#eef2fa; --chip-active:#2f6fed; --shadow:0 6px 24px rgba(40,60,120,.12);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Microsoft YaHei",sans-serif;
  line-height:1.6;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
header{position:sticky;top:0;z-index:20;backdrop-filter:blur(12px);
  background:var(--panel);border-bottom:1px solid var(--border)}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
.h-top{display:flex;align-items:center;gap:14px;padding:16px 0 12px;flex-wrap:wrap}
.h-top h1{font-size:20px;margin:0;font-weight:700;letter-spacing:.3px}
.h-top h1 .em{background:linear-gradient(90deg,var(--accent),var(--accent2));
  -webkit-background-clip:text;background-clip:text;color:transparent}
.live{font-size:12px;color:var(--muted);border:1px solid var(--border);
  padding:3px 9px;border-radius:999px;transition:.2s}
.live:hover{color:var(--accent);border-color:var(--accent)}
.sibnav{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:0 0 10px}
.sib-label{font-size:12px;color:var(--muted)}
.sib{font-size:12.5px;color:var(--accent);border:1px solid var(--border);padding:3px 10px;border-radius:999px;transition:.15s}
.sib:hover{border-color:var(--accent);background:rgba(110,168,254,.1)}
.spacer{flex:1}
#themeBtn{cursor:pointer;border:1px solid var(--border);background:transparent;color:var(--text);
  border-radius:10px;padding:7px 12px;font-size:14px;transition:.2s}
#themeBtn:hover{border-color:var(--accent);color:var(--accent)}
#search{width:100%;padding:11px 14px;border-radius:12px;border:1px solid var(--border);
  background:var(--card);color:var(--text);font-size:15px;outline:none;transition:.2s}
#search:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(110,168,254,.18)}
#tagbar{display:flex;flex-wrap:wrap;gap:8px;padding:12px 0 16px;
  max-height:120px;overflow-y:auto;padding-right:6px;
  transition:max-height .3s ease}
#tagbar.collapsed{max-height:0;overflow:hidden;padding:0}
.chip{cursor:pointer;font-size:12.5px;padding:5px 11px;border-radius:999px;
  background:var(--chip);color:var(--muted);border:1px solid transparent;transition:.15s;user-select:none}
.chip:hover{color:var(--text)}
.chip.active{background:var(--chip-active);color:#0b0e16;border-color:var(--chip-active);font-weight:600}
main{padding:8px 0 60px}
.sec{margin:26px 0 8px}
.sec h2{font-size:15px;text-transform:uppercase;letter-spacing:1.2px;color:var(--muted);
  margin:0 0 14px;display:flex;align-items:center;gap:9px}
.sec h2 .cnt{font-size:12px;background:var(--chip);color:var(--muted);padding:1px 9px;border-radius:999px;letter-spacing:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px}
.card{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:16px 17px;
  transition:.18s;display:flex;flex-direction:column;gap:8px;min-height:96px}
.card:hover{background:var(--card-hover);transform:translateY(-3px);box-shadow:var(--shadow);border-color:var(--accent)}
.card .t{font-weight:650;font-size:15.5px;display:flex;align-items:center;gap:7px}
.card .t .arrow{color:var(--accent);opacity:0;transition:.18s;font-size:13px}
.card:hover .t .arrow{opacity:1}
.card .d{font-size:13px;color:var(--muted);flex:1}
.card .tags{display:flex;flex-wrap:wrap;gap:6px}
.card .tag{font-size:11px;color:var(--accent2);background:rgba(126,224,192,.10);
  border:1px solid rgba(126,224,192,.25);padding:1px 8px;border-radius:999px}
.card .idx{font-size:10.5px;font-weight:700;letter-spacing:.5px;color:var(--accent);
  background:rgba(110,168,254,.12);border:1px solid rgba(110,168,254,.3);padding:1px 7px;border-radius:6px}
.empty{text-align:center;color:var(--muted);padding:50px 0;font-size:15px}
footer{border-top:1px solid var(--border);color:var(--muted);font-size:12.5px;text-align:center;padding:22px 0 40px}
footer code{background:var(--chip);padding:2px 7px;border-radius:6px;color:var(--text)}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="h-top">
      <h1><span class="em">AI Learning Journey</span> · Resource Index</h1>
      <a class="live" href="__LIVE__" target="_blank" rel="noopener">🌐 仓库 README</a>
      <span class="spacer"></span>
      <button id="themeBtn" title="切换主题">🌙</button>
    </div>
    <div class="sibnav"><span class="sib-label">姊妹仓库：</span>__SIBLINGS__</div>
    <input id="search" type="text" placeholder="搜索资源 / 描述 / 标签…" autocomplete="off">
    <div id="tagbar"></div>
  </div>
</header>
<main class="wrap">
  <div id="app"></div>
  <div class="empty" id="empty" style="display:none">没有匹配的资源 🤔</div>
</main>
<footer class="wrap">
  由 <code>scripts/generate_index.py</code> 从 README.md 自动生成 · 最后更新 __DATE__<br>
  添加资源后改 README，重跑脚本即可同步本页。
</footer>
<script>
const DATA = __DATA__;
const LIVE = "__LIVE__";
const state = { q: "", tags: new Set() };

const allTags = new Set();
DATA.categories.forEach(c => c.items.forEach(it => it.tags.forEach(t => allTags.add(t))));
const sortedTags = [...allTags].sort();

const app = document.getElementById("app");
const tagbar = document.getElementById("tagbar");
const empty = document.getElementById("empty");
const search = document.getElementById("search");

function tagChips(tags) {
  if (!tags.length) return "";
  return '<div class="tags">' + tags.map(t =>
    `<span class="tag">#${t}</span>`).join("") + "</div>";
}

function cardHTML(it) {
  const idx = it.index ? '<span class="idx">INDEX</span>' : "";
  const desc = it.desc ? `<div class="d">${it.desc}</div>` : "";
  return `<a class="card" href="${it.url}" target="_blank" rel="noopener">
    <div class="t">${idx}${it.title}<span class="arrow">↗</span></div>
    ${desc}${tagChips(it.tags)}</a>`;
}

function visible(it) {
  const q = state.q;
  const txt = (it.title + " " + it.desc + " " + it.tags.join(" ")).toLowerCase();
  const okQ = !q || txt.includes(q);
  const okT = state.tags.size === 0 || it.tags.some(t => state.tags.has(t));
  return okQ && okT;
}

function renderTags() {
  if (sortedTags.length === 0) { tagbar.style.display = "none"; return; }
  tagbar.innerHTML = sortedTags.map(t => {
    const active = state.tags.has(t) ? " active" : "";
    return `<span class="chip${active}" data-t="${t}">#${t}</span>`;
  }).join("");
  tagbar.querySelectorAll(".chip").forEach(el => {
    el.onclick = () => {
      const t = el.dataset.t;
      if (state.tags.has(t)) state.tags.delete(t); else state.tags.add(t);
      renderTags(); render();
    };
  });
}

function render() {
  let html = "";
  let total = 0;
  DATA.categories.forEach(c => {
    const items = c.items.filter(visible);
    if (!items.length) return;
    total += items.length;
    html += `<section class="sec"><h2>${c.name}<span class="cnt">${items.length}</span></h2>
      <div class="grid">${items.map(cardHTML).join("")}</div></section>`;
  });
  app.innerHTML = html;
  empty.style.display = total ? "none" : "block";
  /* collapse tagbar when searching to give results room */
  if (state.q) { tagbar.classList.add("collapsed"); }
  else { tagbar.classList.remove("collapsed"); }
  /* show result count in search placeholder */
  search.placeholder = state.q
    ? `搜索: "${state.q}" — 找到 ${total} 条结果`
    : "搜索资源 / 描述 / 标签…";
}

search.addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });

// theme
const themeBtn = document.getElementById("themeBtn");
function applyTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  themeBtn.textContent = t === "dark" ? "🌙" : "☀️";
  try { localStorage.setItem("alj-theme", t); } catch (e) {}
}
themeBtn.onclick = () => {
  const cur = document.documentElement.getAttribute("data-theme");
  applyTheme(cur === "dark" ? "light" : "dark");
};
(function () {
  let t = "dark";
  try { t = localStorage.getItem("alj-theme") || "dark"; } catch (e) {}
  applyTheme(t);
})();

renderTags();
render();
</script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", json.dumps(data, ensure_ascii=False))
        .replace("__DATE__", data["generated"])
        .replace("__LIVE__", BLOB + "README.md")
        .replace("__SIBLINGS__", "".join(
            f'<a class="sib" href="{s["url"]}" target="_blank" rel="noopener">{s["name"]}</a>'
            for s in SIBLINGS)))

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
n_items = sum(len(c["items"]) for c in categories)
n_tags = len({t for c in categories for it in c["items"] for t in it["tags"]})
print(f"Wrote {out} — {len(categories)} categories, {n_items} items, {n_tags} tags")
