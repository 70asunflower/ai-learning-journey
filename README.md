# AI Learning Journey 🤖

> A collection of resources, notes, and project explorations in AI.

---

## 🗂️ Wiki Navigation

<details open>
<summary><b>📚 Resources</b></summary>

<details>
<summary>1-Official-Docs</summary>

- [CUDA Programming Guide](0-Resources/1-Official-Docs/cuda-programming-guide.md) — NVIDIA 官方 GPU 并行编程模型文档

</details>

<details open>
<summary>2-Papers</summary>

[📄 Papers Index](0-Resources/2-Papers/README.md)

</details>

<details open>
<summary>3-Tutorials</summary>

- [self-llm 大模型食用指南](0-Resources/3-Tutorials/self-llm.md) — DataWhale 社区维护的中文开源大模型入门教程，覆盖环境配置、部署使用、高效微调全流程
- [Sebastian Raschka Blog](0-Resources/3-Tutorials/sebastian-raschka-blog.md) — 深度学习、LLM、PyTorch 技术博客
- [📄 Tutorials Index](0-Resources/3-Tutorials/README.md)

</details>

<details open>
<summary>4-Tools & Frameworks</summary>

- [ms-swift 微调部署框架](0-Resources/4-Tools-Frameworks/ms-swift.md) — 魔搭社区大模型与多模态模型全链路框架，覆盖训练→推理→评测→量化→部署
- [ModelScope Notebook 免费试用](0-Resources/4-Tools-Frameworks/ModelScope-Notebook.md) — 魔搭云上开发环境，开箱即用 GPU/CPU，提供免费使用时长
- [TikTokenizer 可视化交互工具](0-Resources/4-Tools-Frameworks/tiktokenizer.md) — 可视化学习 LLM Tokenizer 工作原理的交互工具 (GPT2/CL100K 等编码器)
- [📄 Tools Index](0-Resources/4-Tools-Frameworks/README.md)

</details>

<details open>
<summary>5-Datasets</summary>

[📄 Datasets Index](0-Resources/5-Datasets/README.md)

</details>

[📋 Full Resource Index](0-Resources/0-Index.md)

</details>

<details open>
<summary><b>📝 Personal Notes</b></summary>

<details open>
<summary>1-Foundations</summary>

[📄 Foundations Index](1-Notes/1-Foundations/README.md)

</details>

<details open>
<summary>2-Models</summary>

[📄 Models Index](1-Notes/2-Models/README.md)

</details>

<details open>
<summary>3-Training</summary>

[📄 Training Index](1-Notes/3-Training/README.md)

</details>

<details open>
<summary>4-Deployment</summary>

[📄 Deployment Index](1-Notes/4-Deployment/README.md)

</details>

[📋 Note Template](1-Notes/0-Template.md)

</details>

<details>
<summary><b>💻 Code & Projects</b></summary>

<details open>
<summary>[Code Examples](2-Code/README.md)</summary>

_Empty — add a runnable example!_

</details>

<details open>
<summary>[Projects](3-Projects/README.md)</summary>

_Empty — create your first project!_

</details>

</details>

<details open>
<summary><b>🗃️ Misc</b></summary>

- [Stickies](_misc/personal-tools.md) — Windows 桌面便签工具，富文本+定时提醒+自动关闭

</details>

---

## 📁 Directory Structure

```
ai-learning-journey/
├── 0-Resources/          # Resource collection
│   ├── 1-Official-Docs/  # Official docs, best practices
│   ├── 2-Papers/         # Important papers
│   ├── 3-Tutorials/      # Quality tutorials & blogs
│   ├── 4-Tools-Frameworks/  # Tools & frameworks
│   └── 5-Datasets/       # Datasets
├── 1-Notes/              # Personal study notes
│   ├── 1-Foundations/    # Core concepts
│   ├── 2-Models/         # Model-specific notes
│   ├── 3-Training/       # Training techniques
│   └── 4-Deployment/     # Inference & deployment
├── 2-Code/               # Runnable code examples
├── 3-Projects/           # Comprehensive projects
├── _misc/                # Unclassified / personal tools
└── scripts/              # Helper scripts
```

## 🎯 How to Update (for agents & humans)

### Adding a New Resource (0-Resources/)

1. Create a `.md` file in the correct subfolder (e.g. `0-Resources/4-Tools-Frameworks/<name>.md`)
2. Start with this frontmatter:
   ```markdown
   ---
   source: <original URL>
   date: YYYY-MM-DD
   tags: [tag1, tag2]
   ---
   ```
3. Write the content: summary, key points, or full doc with source attribution
4. End with: `_Last updated: YYYY-MM-DD_`
5. Add it to the table in that folder's `README.md`
6. Add it to the wiki nav in this file under the correct `<details>` section
7. Add it to `0-Resources/0-Index.md`

### Adding a New Note (1-Notes/)

1. Create a `.md` file in the correct subfolder (e.g. `1-Notes/2-Models/Qwen-Series/<model>.md`)
2. Start with the same frontmatter as above
3. Write your personal understanding, code experiments, gotchas
4. End with: `_Last updated: YYYY-MM-DD_`
5. Add the link to the folder's `README.md` index
6. Add the link to the wiki nav in this file

### Adding to Code Examples (2-Code/)

1. Create a subfolder: `2-Code/<project-name>/`
2. Include: `main.py`, `requirements.txt`, `README.md`
3. Add it to `2-Code/README.md` examples table

### Key Rules

- **File names**: lowercase, hyphen-separated (e.g. `qwen3-vl-best-practice.md`)
- **Wiki nav**: every new file must be linked in this README's navigation
- **Resource Index**: `0-Index.md` mirrors all resources — keep it in sync
- **Changelog**: add a new row below for each update
- **Always include `Last updated`**: every resource/note file ends with `_Last updated: YYYY-MM-DD_`

## Changelog

| Date       | Content                                          |
|------------|--------------------------------------------------|
| 2026-03-31 | Repository init, wiki navigation, subfolder docs |
| 2026-03-31 | Added ms-swift framework documentation            |
| 2026-04-02 | Added TikTokenizer — interactive tokenizer visualization tool |
| 2026-04-03 | Added CUDA Programming Guide                     |
| 2026-04-04 | Added Sebastian Raschka Blog                   |
| 2026-03-31 | Added "How to Update" section for agents          |
