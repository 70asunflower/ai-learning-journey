#!/usr/bin/env python3
"""Generate a single-file index.html from README.md wiki navigation + 0-Index.md tags.

Usage:
    python scripts/generate_index.py

The script parses the "📚 Resources" block of README.md (every <details> category and
its markdown links) and enriches each item with tags scraped from 0-Resources/0-Index.md.

Output: index.html at repo root (self-contained: embedded CSS + JS).
  * Clicking a resource opens an in-page reader (fetches the .md and renders it with marked.js)
  * Minimalist theme, search box, optional tag filter, light/dark toggle, sister-repo nav.

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

TITLE = "AI Learning Journey"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
index_md = (ROOT / "0-Resources" / "0-Index.md").read_text(encoding="utf-8")
# Inline marked.js so the page works fully offline / behind GFW (no CDN dependency).
marked_js = (ROOT / "scripts" / "marked.min.js").read_text(encoding="utf-8")

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

    # classify link: internal (repo .md) vs external
    if url.startswith(("http://", "https://")):
        if url.startswith(BLOB):
            path = url[len(BLOB):]
            external = False
        else:
            path = url
            external = True
        github = url
    else:
        path = url
        external = False
        github = BLOB + url

    tags = tags_by_path.get(normalize(url), [])
    is_index = title.startswith(("📄", "📋", "📁"))
    name = prettify(cat)
    if name not in cat_map:
        items: list[dict] = []
        cat_map[name] = items
        categories.append({"name": name, "items": items})
    cat_map[name].append(
        {"title": title, "path": path, "github": github, "external": external,
         "desc": desc, "tags": tags, "index": is_index}
    )

data = {
    "repo": REPO,
    "branch": BRANCH,
    "generated": datetime.date.today().isoformat(),
    "categories": categories,
}

HTML = r"""<!DOCTYPE html>
<html lang="zh" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ · Resource Index</title>
<script>__MARKED__</script>
<style>
:root{
  --bg:#fcfcfb; --panel:#ffffff; --card:#ffffff; --card-hover:#f7f7f5;
  --text:#1c1c1c; --muted:#9a9a9a; --accent:#2f6df6; --border:#ececec;
  --code:#f4f4f2; --shadow:0 1px 2px rgba(0,0,0,.03);
}
[data-theme="dark"]{
  --bg:#101011; --panel:#171718; --card:#1b1b1d; --card-hover:#232325;
  --text:#e9e9e7; --muted:#8c8c8c; --accent:#6f9bf2; --border:#2a2a2d;
  --code:#212124; --shadow:none;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:15px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
header{border-bottom:1px solid var(--border);background:var(--panel)}
.wrap{max-width:900px;margin:0 auto;padding:0 24px}
.h-top{display:flex;align-items:center;gap:14px;padding:22px 0 16px;flex-wrap:wrap}
.h-top h1{font-size:19px;margin:0;font-weight:600;letter-spacing:.2px}
.live{font-size:12px;color:var(--muted);border:1px solid var(--border);
  padding:3px 10px;border-radius:6px;transition:.2s}
.live:hover{color:var(--accent);border-color:var(--accent)}
.sibnav{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:0 0 14px}
.sib-label{font-size:12px;color:var(--muted)}
.sib{font-size:12.5px;color:var(--accent);border:1px solid var(--border);padding:3px 11px;border-radius:6px;transition:.15s}
.sib:hover{border-color:var(--accent)}
.spacer{flex:1}
#themeBtn{cursor:pointer;border:1px solid var(--border);background:transparent;color:var(--text);
  border-radius:6px;padding:6px 11px;font-size:14px;transition:.2s}
#themeBtn:hover{border-color:var(--accent);color:var(--accent)}
#search{width:100%;padding:10px 13px;border-radius:8px;border:1px solid var(--border);
  background:var(--card);color:var(--text);font-size:14.5px;outline:none;transition:.2s}
#search:focus{border-color:var(--accent)}
#tagbar{display:flex;flex-wrap:wrap;gap:7px;padding:12px 0 16px;
  max-height:118px;overflow-y:auto;transition:max-height .3s ease}
#tagbar.collapsed{max-height:0;overflow:hidden;padding:0}
.chip{cursor:pointer;font-size:12px;padding:4px 10px;border-radius:6px;
  background:transparent;color:var(--muted);border:1px solid var(--border);transition:.15s;user-select:none}
.chip:hover{color:var(--text)}
.chip.active{background:var(--accent);color:#fff;border-color:var(--accent)}
main{padding:6px 0 60px}
.sec{margin:30px 0 10px}
.sec h2{font-size:12.5px;text-transform:uppercase;letter-spacing:1.4px;color:var(--muted);
  margin:0 0 16px;display:flex;align-items:center;gap:9px;font-weight:600}
.sec h2 .cnt{font-size:11px;background:var(--card);color:var(--muted);padding:1px 8px;border-radius:6px;border:1px solid var(--border);letter-spacing:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:15px 16px;
  transition:.15s;display:flex;flex-direction:column;gap:8px;min-height:92px}
.card:hover{border-color:var(--accent);background:var(--card-hover)}
.card .t{font-weight:600;font-size:15px;display:flex;align-items:center;gap:7px}
.card .t .arrow{color:var(--accent);opacity:0;transition:.15s;font-size:12px;margin-left:auto}
.card:hover .t .arrow{opacity:1}
.card .d{font-size:13px;color:var(--muted);flex:1}
.card .tags{display:flex;flex-wrap:wrap;gap:6px}
.card .tag{font-size:11px;color:var(--accent);background:transparent;border:1px solid var(--border);padding:1px 8px;border-radius:6px}
.card .idx{font-size:10px;font-weight:700;letter-spacing:.5px;color:var(--accent);
  border:1px solid var(--accent);padding:1px 7px;border-radius:5px}
.empty{text-align:center;color:var(--muted);padding:50px 0;font-size:15px}
footer{border-top:1px solid var(--border);color:var(--muted);font-size:12px;text-align:center;padding:24px 0 44px}
footer code{background:var(--card);padding:2px 7px;border-radius:5px;color:var(--text);border:1px solid var(--border)}

/* ---- reader overlay ---- */
.reader{position:fixed;inset:0;background:var(--bg);z-index:50;display:none;flex-direction:column}
.reader.open{display:flex}
.reader-bar{position:sticky;top:0;background:var(--panel);border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:12px;padding:11px 24px;flex-wrap:wrap}
.reader-bar .ttl{font-weight:600;font-size:14px;max-width:60%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.reader-bar .gh{font-size:12px;color:var(--accent);margin-left:auto}
.reader-bar .x{cursor:pointer;border:1px solid var(--border);background:transparent;color:var(--text);
  border-radius:7px;width:34px;height:34px;font-size:17px;line-height:1;transition:.15s}
.reader-bar .x:hover{border-color:var(--accent);color:var(--accent)}
.content{max-width:760px;width:100%;margin:0 auto;padding:30px 24px 90px;line-height:1.78;overflow-y:auto;flex:1}
.content .loading,.content .fallback{color:var(--muted);padding:40px 0;text-align:center}
.content .fallback a{color:var(--accent)}
.content h1,.content h2,.content h3{line-height:1.35;margin:1.6em 0 .6em;font-weight:650}
.content h1{font-size:24px;border-bottom:1px solid var(--border);padding-bottom:.3em}
.content h2{font-size:20px}
.content h3{font-size:16.5px}
.content p{margin:.7em 0}
.content a{color:var(--accent);text-decoration:none;border-bottom:1px solid transparent}
.content a:hover{border-bottom-color:var(--accent)}
.content code{background:var(--code);padding:2px 6px;border-radius:5px;font-size:.88em;font-family:"SFMono-Regular",Consolas,Menlo,monospace}
.content pre{background:var(--code);padding:14px 16px;border-radius:10px;overflow-x:auto;line-height:1.5}
.content pre code{background:transparent;padding:0}
.content blockquote{margin:.9em 0;padding:.4em 1em;border-left:3px solid var(--border);color:var(--muted)}
.content img{max-width:100%;border-radius:8px;margin:.5em 0}
.content table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14px}
.content th,.content td{border:1px solid var(--border);padding:7px 10px;text-align:left}
.content ul,.content ol{padding-left:1.4em}
</style>
</head>
<body>
<header>
  <div class="wrap">
    <div class="h-top">
      <h1>__TITLE__ · Resource Index</h1>
      <a class="live" href="__LIVE__" target="_blank" rel="noopener">仓库 README</a>
      <span class="spacer"></span>
      <button id="themeBtn" title="切换主题">◐</button>
    </div>
    <div class="sibnav"><span class="sib-label">姊妹仓库</span>__SIBLINGS__</div>
    <input id="search" type="text" placeholder="搜索资源 / 描述 / 标签…" autocomplete="off">
    <div id="tagbar"></div>
  </div>
</header>
<main class="wrap">
  <div id="app"></div>
  <div class="empty" id="empty" style="display:none">没有匹配的资源</div>
</main>
<footer class="wrap">
  由 <code>scripts/generate_index.py</code> 从 README.md 自动生成 · 最后更新 __DATE__<br>
  点击任意资源即可在本页阅读内容 · 添加资源后改 README，重跑脚本即同步
</footer>

<div class="reader" id="reader">
  <div class="reader-bar">
    <button class="x" id="readerX" title="关闭">×</button>
    <span class="ttl" id="readerTitle"></span>
    <a class="gh" id="readerGh" href="#" target="_blank" rel="noopener">在 GitHub 查看 ↗</a>
  </div>
  <div class="content" id="readerContent"></div>
</div>

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
const reader = document.getElementById("reader");
const readerContent = document.getElementById("readerContent");
const readerTitle = document.getElementById("readerTitle");
const readerGh = document.getElementById("readerGh");
const readerX = document.getElementById("readerX");
let currentGithub = LIVE;

function tagChips(tags) {
  if (!tags.length) return "";
  return '<div class="tags">' + tags.map(t =>
    `<span class="tag">#${t}</span>`).join("") + "</div>";
}

function cardHTML(it) {
  const idx = it.index ? '<span class="idx">INDEX</span>' : "";
  const desc = it.desc ? `<div class="d">${it.desc}</div>` : "";
  const ext = it.external ? ' target="_blank" rel="noopener"' : '';
  return `<a class="card" href="${it.github}" data-path="${it.path}" data-title="${it.title}" data-gh="${it.github}" data-ext="${it.external ? 1 : 0}"${ext}>
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
  if (state.q) { tagbar.classList.add("collapsed"); }
  else { tagbar.classList.remove("collapsed"); }
  search.placeholder = state.q
    ? `搜索: "${state.q}" — 找到 ${total} 条`
    : "搜索资源 / 描述 / 标签…";
}

app.addEventListener("click", e => {
  const card = e.target.closest(".card");
  if (!card) return;
  if (card.dataset.ext === "1") return; /* external link: let browser open */
  e.preventDefault();
  currentGithub = card.dataset.gh;
  openReader(card.dataset.path, card.dataset.title);
});

/* ---------- in-page reader ---------- */
function baseDirOf(p) { const i = p.lastIndexOf("/"); return i < 0 ? "" : p.slice(0, i + 1); }
function resolve(rel, base) {
  if (/^(https?:|#|\/)/.test(rel)) return rel;
  return base + rel;
}
function renderMD(md, base) {
  let html;
  if (window.marked) html = marked.parse(md);
  else html = "<pre>" + md.replace(/</g, "&lt;") + "</pre>";
  const div = document.createElement("div");
  div.innerHTML = html;
  div.querySelectorAll("img").forEach(im => { im.src = resolve(im.getAttribute("src") || "", base); });
  div.querySelectorAll("a").forEach(a => {
    const h = a.getAttribute("href") || "";
    if (h.endsWith(".md") && !/^https?:/.test(h)) {
      const p = resolve(h, base);
      a.setAttribute("href", "#");
      a.addEventListener("click", ev => { ev.preventDefault(); openReader(p, a.textContent); });
    } else if (!/^(https?:|#)/.test(h)) {
      a.setAttribute("href", resolve(h, base));
      a.target = "_blank"; a.rel = "noopener";
    } else if (/^https?:/.test(h)) {
      a.target = "_blank"; a.rel = "noopener";
    }
  });
  return div.innerHTML;
}
function openReader(path, title) {
  location.hash = "view/" + encodeURIComponent(path) + "|" + encodeURIComponent(title || "");
}
async function showReader(path, title) {
  reader.classList.add("open");
  document.body.style.overflow = "hidden";
  readerTitle.textContent = title || path;
  readerGh.href = currentGithub;
  readerContent.innerHTML = '<div class="loading">加载中…</div>';
  try {
    const res = await fetch(path);
    if (!res.ok) throw new Error("HTTP " + res.status);
    const md = await res.text();
    readerContent.innerHTML = renderMD(md, baseDirOf(path));
    readerContent.scrollTop = 0;
  } catch (e) {
    readerContent.innerHTML = '<div class="fallback">无法在本页加载内容（可能为本地打开或网络限制）。<br>' +
      '<a href="' + currentGithub + '" target="_blank" rel="noopener">在 GitHub 查看原文 ↗</a></div>';
  }
}
function closeReader() {
  if (location.hash) location.hash = "";
  else { reader.classList.remove("open"); document.body.style.overflow = ""; }
}
readerX.addEventListener("click", closeReader);
window.addEventListener("hashchange", () => {
  const h = location.hash;
  if (h.startsWith("#view/")) {
    const body = decodeURIComponent(h.slice(6));
    const sep = body.indexOf("|");
    const path = sep < 0 ? body : body.slice(0, sep);
    const title = sep < 0 ? "" : decodeURIComponent(body.slice(sep + 1));
    /* if github not set (deep link), derive it */
    if (currentGithub === LIVE && !path.startsWith("http")) {
      currentGithub = "https://github.com/" + DATA.repo + "/blob/" + DATA.branch + "/" + path;
    }
    showReader(path, title);
  } else {
    reader.classList.remove("open");
    document.body.style.overflow = "";
  }
});
if (location.hash.startsWith("#view/")) {
  const body = decodeURIComponent(location.hash.slice(6));
  const sep = body.indexOf("|");
  const path = sep < 0 ? body : body.slice(0, sep);
  const title = sep < 0 ? "" : decodeURIComponent(body.slice(sep + 1));
  showReader(path, title);
}

/* theme */
const themeBtn = document.getElementById("themeBtn");
function applyTheme(t) {
  document.documentElement.setAttribute("data-theme", t);
  try { localStorage.setItem("alj-theme", t); } catch (e) {}
}
themeBtn.onclick = () => {
  const cur = document.documentElement.getAttribute("data-theme");
  applyTheme(cur === "dark" ? "light" : "dark");
};
(function () {
  let t = "light";
  try { t = localStorage.getItem("alj-theme") || "light"; } catch (e) {}
  applyTheme(t);
})();

search.addEventListener("input", e => { state.q = e.target.value.trim().toLowerCase(); render(); });

renderTags();
render();
</script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
        .replace("__DATE__", data["generated"])
        .replace("__LIVE__", BLOB + "README.md")
        .replace("__SIBLINGS__", "".join(
            f'<a class="sib" href="{s["url"]}" target="_blank" rel="noopener">{s["name"]}</a>'
            for s in SIBLINGS))
        .replace("__TITLE__", TITLE)
        .replace("__MARKED__", marked_js.replace("</script>", "<\\/script>")))

out = ROOT / "index.html"
out.write_text(html, encoding="utf-8")
n_items = sum(len(c["items"]) for c in categories)
n_tags = len({t for c in categories for it in c["items"] for t in it["tags"]})
print(f"Wrote {out} — {len(categories)} categories, {n_items} items, {n_tags} tags")
