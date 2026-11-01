# 辅助脚本

**唯一数据源** = 每个资源文件的 frontmatter（`title` / `summary` / `source` / `date` / `tags`）。
所有索引类文件都是生成物，不需要手写。

## 脚本列表

### build.py

从资源 frontmatter 生成全部派生产物：

| 产物 | 生成范围 |
|------|----------|
| `0-Resources/0-Index.md` | 整个文件 |
| `0-Resources/<子目录>/README.md` | `<!-- BUILD:TABLE:START/END -->` 之间 |
| `README.md` 资源导航 | `<!-- BUILD:NAV:START/END -->` 之间 |
| `README.md` 文本版地图 | `<!-- BUILD:MAP:START/END -->` 之间 |
| `README.md` 文本版技术栈树 | `<!-- BUILD:TREE:START/END -->` 之间 |
| `index.html` | 整个文件 |

```bash
python scripts/build.py            # 重写全部产物
python scripts/build.py --check    # 只检查是否最新，有差异 exit 1（CI / 提交前用）
```

幂等：内容不变时重跑不产生 diff。`index.html` 的 `generated` 日期取资源 `date` 的最大值。

### check_consistency.py

语义检查（CI 中先于 build 运行）：

- 资源 frontmatter 五项齐全、`date` 格式合法
- 文件名小写连字符规范
- `_Last updated: YYYY-MM-DD_` 结尾
- tag 必须是规范写法（别名表见 `scripts/tags.json`）
- 内部死链（markdown `](...)` 与 HTML `<a href>` 都查）
- Changelog 无重复行、日期倒序

```bash
python scripts/check_consistency.py   # 0 error(s), 0 warning(s) 为通过
```

**不检查**生成物是否同步 —— 那是 `build.py --check` 的职责。两个工具各管一段，
避免同一份数据两套判定逻辑。

### normalize_tags.py

按 `scripts/tags.json` 的别名表把 tag 改写成规范写法（作用于资源 frontmatter 和
`0-Index.md` 的 tag 列）。

```bash
python scripts/normalize_tags.py --check    # 只报告，有别名残留则 exit 1
python scripts/normalize_tags.py            # 就地改写
python scripts/normalize_tags.py --report   # tag 频次 / 单例 tag
```

## 约定

- 资源 frontmatter：`title` / `summary` / `source` / `date` / `tags` 五项必填
- `summary` 同时用于网页卡片和子目录表格，40–60 字最佳
- 资源文件结尾：`_Last updated: YYYY-MM-DD_`
- 新 tag 前先查 `scripts/tags.json`；确实是新概念才新增，近义词写进别名表
- 生成块不要手改（`BUILD:NAV` / `BUILD:TABLE` / `BUILD:MAP` / `BUILD:TREE` 标记之间）
