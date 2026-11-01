# 参与维护

新增资源 / 笔记 / 代码示例的流程。人类和 agent 都按这套走。

> 仓库里有两份自动化工具说明：[`scripts/README.md`](scripts/README.md)（脚本清单）和
> `.workbuddy/skills/ai-journey-add/`（agent 用的完整操作手册，含 `gh` 推送凭据细节）。

## 加一条资源（0-Resources/）

1. 在对应子目录建 `.md` 文件（如 `0-Resources/4-Tools-Frameworks/<name>.md`），文件名小写连字符
2. 开头写 frontmatter：
   ```markdown
   ---
   source: <原始 URL>
   date: YYYY-MM-DD
   tags: [tag1, tag2]
   ---
   ```
3. 正文：摘要、要点，或带出处标注的完整内容
4. 结尾写 `_Last updated: YYYY-MM-DD_`
5. 加进该子目录的 `README.md` 表格
6. 加进根 `README.md` 导航里对应的 `<details>` 段
7. 加进 `0-Resources/0-Index.md`
8. 重跑 `python scripts/generate_index.py`

## 加一条笔记（1-Notes/）

1. 在对应子目录建 `.md` 文件（如 `1-Notes/2-Models/Qwen-Series/<model>.md`）
2. frontmatter **和资源不同**，用笔记的 schema（以 `1-Notes/0-Template.md` 为准）：
   ```markdown
   ---
   topic: 主题
   date: YYYY-MM-DD
   tags: []
   status: reading   # reading / writing / done
   ---
   ```
3. 正文：自己的理解、代码实验、踩过的坑
4. 结尾写 `_Last updated: YYYY-MM-DD_`
5. 加进该目录的 `README.md` 索引
6. 加进根 `README.md` 导航

## 加一个代码示例（2-Code/）

1. 建子目录 `2-Code/<project-name>/`
2. 包含 `main.py`、`requirements.txt`、`README.md`
3. 加进 `2-Code/README.md` 的示例表格

## 硬性规则

- **文件名**：小写、连字符分隔（如 `qwen3-vl-best-practice.md`）
- **导航**：每个新文件都必须在根 `README.md` 导航里出现
- **资源索引**：`0-Index.md` 要镜像所有资源。`index.html` 的 `generated` 日期取自该表
  最新一行日期，**没有 footer 需要手动 bump**
- **标签**：只用规范写法。`scripts/tags.json` 登记了「废弃写法 → 规范写法」，
  `python scripts/normalize_tags.py` 会改写，CI 会拒绝任何残留别名；
  `--report` 打印标签频次和单例标签（判断该不该合并）
- **Changelog**：新行插在**表头下方**（日期倒序，CI 强制）
- **Last updated**：每个资源/笔记文件结尾都要有 `_Last updated: YYYY-MM-DD_`
- **网页索引**：`index.html` 由 `scripts/generate_index.py` 从根 `README.md` 导航生成，
  加完资源要重跑并提交重新生成的文件

## 提交前自检

```bash
python scripts/check_consistency.py     # 必须 0 error(s), 0 warning(s)
python scripts/normalize_tags.py --check  # 必须 "Tags already canonical."
python scripts/generate_index.py        # 重跑应无 diff
```

## 更新 README 预览图

`assets/preview.png` 是 `index.html` 的截图，界面有较大变化时重截一次：

```bash
python -m http.server 8765 --bind 127.0.0.1     # 另开一个终端
# Chrome 路径按本机调整
chrome --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1200,1000 --virtual-time-budget=4000 \
  --screenshot="$PWD/assets/preview.png" \
  "http://127.0.0.1:8765/index.html"
```

无头 Chrome 默认按暗色渲染，所以预览图是暗色版。
