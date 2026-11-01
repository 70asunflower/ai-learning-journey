# 辅助脚本

用于自动化维护任务的脚本。

## 脚本列表

### generate_index.py

从 README.md 的 `📚 Resources` 块 + `0-Resources/0-Index.md` 重新生成 `index.html`（自包含单文件阅读器）。幂等：`generated` 日期取 0-Index.md 表格中**最新的一条资源日期**，因此新增资源会自动更新日期，不需要手改任何 footer，本地与 CI 生成结果字节级一致。

```bash
python scripts/generate_index.py
```

### check_consistency.py

一致性门禁（CI 中在 regenerate 之前运行，失败即中断构建）：

- 磁盘资源文件 ↔ 子目录 `README.md` 表 ↔ `0-Index.md` ↔ 根 `README.md` 导航
- 每条注册链接必须真实可达（内部死链检测）
- frontmatter 基础检查（`title` 或 `source`、`_Last updated` footer）
- Changelog 重复行守卫 + **日期必须倒序**（新行插在表头下方）
- **tag 必须是规范写法**：出现 `scripts/tags.json` 里登记的别名即报错

```bash
python scripts/check_consistency.py   # 0 error(s), 0 warning(s) 为通过；有 error 时 exit 1
```

### normalize_tags.py

按 `scripts/tags.json` 的别名表把 tag 改写成规范写法，同时作用于资源 frontmatter 和 `0-Index.md` 的 tag 列，保证两处用词一致。

```bash
python scripts/normalize_tags.py --check    # 只报告，有别名残留则 exit 1
python scripts/normalize_tags.py            # 就地改写
python scripts/normalize_tags.py --report   # 打印 tag 频次 / 单例 tag（判断是否该合并）
```

## 约定

- 资源文件 frontmatter：`source: <URL>` / `date: YYYY-MM-DD` / `tags: [a, b]`
- 文件结尾：`_Last updated: YYYY-MM-DD_`（下划线包裹）
- `0-Index.md` 的 tag 列用反引号包裹、`#` 前缀：`` `#tag1 #tag2` ``（tag 可含 `.`，如 `#llama.cpp`）
- 新 tag 前先查 `scripts/tags.json`；确实是新概念才新增，近义词写进别名表而不是让两种写法并存
