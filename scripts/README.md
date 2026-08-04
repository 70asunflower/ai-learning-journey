# 辅助脚本

用于自动化维护任务的脚本。

## 脚本列表

### generate_index.py

从 README.md 的 `📚 Resources` 块 + `0-Resources/0-Index.md` 重新生成 `index.html`（自包含单文件阅读器）。幂等：`generated` 日期取自 0-Index.md 的 `_Last updated` footer，本地与 CI 生成结果字节级一致。

```bash
python scripts/generate_index.py
```

### check_consistency.py

四向一致性门禁（CI 中在 regenerate 之前运行，失败即中断构建）：

- 磁盘资源文件 ↔ 子目录 `README.md` 表 ↔ `0-Index.md` ↔ 根 `README.md` 导航
- 每条注册链接必须真实可达（内部死链检测）
- frontmatter 基础检查（`title` 或 `source`、`_Last updated` footer）
- Changelog 重复行守卫

```bash
python scripts/check_consistency.py   # 0 error(s), 0 warning(s) 为通过；有 error 时 exit 1
```

## 约定

- 资源文件 frontmatter：`source: <URL>` / `date: YYYY-MM-DD` / `tags: [a, b]`
- 文件结尾：`_Last updated: YYYY-MM-DD_`（下划线包裹，0-Index.md 同款）
- `0-Index.md` 的 tag 列用反引号包裹、`#` 前缀：`` `#tag1 #tag2` ``（tag 可含 `.`，如 `#llama.cpp`）
