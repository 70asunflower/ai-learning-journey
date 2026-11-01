# 官方文档与最佳实践

收集官方发布的权威指南、部署文档。

## 资源列表

<!-- BUILD:TABLE:START -->
| Resource | Description | Date |
| :--- | :--- | :--- |
| [CUDA Programming Guide](cuda-programming-guide.md) | NVIDIA 官方 GPU 并行编程模型文档 | 2026-04-03 |
| [vLLM 中文文档](vllm-docs-zh.md) | vLLM 官方中文文档（hyper.ai 翻译）：安装/量化/LoRA/分布式推理/部署/设计文档/API | 2026-07-07 |
| [LLM Inference Handbook (Modular)](llm-inference-handbook.md) | 官方 LLM 推理手册：概念/指标/优化/GPU架构/部署模式（含交互计算器） | 2026-08-01 |
<!-- BUILD:TABLE:END -->

## 文件命名规范

```
小写、连字符分隔（与 CONTRIBUTING.md 的规则一致）
例如：cuda-programming-guide.md / vllm-docs-zh.md / llm-inference-handbook.md
```

## 内容格式

每个文件开头应包含：

```markdown
---
title: 标题
summary: 一句话说明（同时用于网页卡片和本表格）
source: 原始链接
date: 收藏日期
tags: [标签1, 标签2]
---
```

正文建议按 `## 核心要点（摘要）` / `## 详细内容` / `## 个人备注` 三段组织，
结尾写 `_Last updated: YYYY-MM-DD_`。
