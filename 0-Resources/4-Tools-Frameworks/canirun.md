---
source: https://www.canirun.ai/
date: 2026-04-09
tags: [local-ai, compatibility, llama.cpp, ollama, lm-studio, quantization, gpu]
---

# CanIRun.ai — 本地 AI 模型硬件兼容性检测工具

## 核心要点（摘要）

CanIRun.ai 是一个免费的在线工具，帮助用户检测自己的电脑硬件配置能跑哪些本地 AI 模型。网站自动识别 GPU、VRAM、RAM 和 CPU 规格，然后在浏览器端展示与硬件匹配的模型列表及兼容性评分。

## 详细内容

### 功能特性

- **硬件自动检测**：通过浏览器 API 自动检测 GPU 型号、显存、内存、CPU 等规格
- **兼容性评级**：Runs great / Runs well / Decent / Tight fit / Barely runs / Too heavy 六档
- **多维度筛选**：按任务类型（Chat / Code / Reasoning / Vision）、提供商（Meta / Google / OpenAI 等）、许可证、架构类型（Dense / MoE）筛选
- **排序方式**：按参数量、上下文长度、显存占用、速度、人气排序
- **量化格式**：显示各模型的量化等级（Q2_K ~ F16）

### 数据来源

- llama.cpp
- Ollama
- LM Studio

### 支持的模型规模

从 0.6B 到 1T 参数均有覆盖，示例包括：
Llama 3.1 8B、Qwen 3.5 9B、Phi-4 14B、GPT-OSS 120B、DeepSeek R1、Gemma 3 27B、Llama 3.3 70B 等

### 工具定位

快速评估本地硬件能力、选择合适的模型大小和量化精度，是本地部署大模型的**选型参考工具**。由 midudev 开发，完全免费使用。

## 个人备注

本地大模型部署选型工具，部署前先在这里评估硬件能跑什么模型、该用哪种量化级别。配合 Ollama / llama.cpp / LM Studio 使用效果更佳。

_Last updated: 2026-04-09_
