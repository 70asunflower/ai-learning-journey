---
source: https://unsloth.ai/docs/zh/kai-shi-shi-yong/fine-tuning-llms-guide
date: 2026-04-04
tags: [fine-tuning, lora, qlora, unsloth, tutorial]
---

# Unsloth LLM 微调指南

## 核心要点（摘要）

Unsloth 官方中文微调指南，覆盖从环境安装、模型选择、数据集准备、训练调参到部署的全流程。推荐 LoRA/QLoRA 高效微调方法，适合有 GPU资源的个人开发者和团队。

## 详细内容

### 1. 微调概述
微调可定制模型行为、注入知识、优化特定任务性能。LoRA/QLoRA 技术仅优化 1% 权重，降低计算资源需求。

### 2. 方法选择
- **SFT（监督微调）**：标准方法
- **RL（强化学习）**：用于特定行为优化
- **LoRA/QLoRA**：参数高效训练，保持基础权重冻结
- **FFT**：全量微调，需大量资源

### 3. 模型建议
初学者推荐从 Llama 3.1 (8B) 开始，使用指令模型 + 动态 4 位量化版本（如 `unsloth/llama-3.1-8b-unsloth-bnb-4bit`）。

### 4. 数据集要点
"为获得最佳结果，请策划一个结构良好的数据集，理想状况下为问答对。" 支持合成数据生成与文档解析。

### 5. 训练参数
- `batch_size`、`gradient_accumulation_steps`、`learning_rate`（2e-4 建议值）
- `max_steps` 或 `num_train_epochs` 控制训练时长
- 损失值 0.5-1.0 通常表示良好学习效果

### 6. 部署选项
- 单设备：GGUF 格式 + Ollama/llama.cpp
- 企业场景：vLLM + FP8/AWQ

### 7. 章节结构
1. 什么是微调？
2. 选择合适的模型和方法
3. 你的数据集
4. 理解训练超参数
5. 安装与需求
6. 训练与评估
7. 运行与部署模型
8. 完成

## 个人备注

Unsloth 是目前最成熟的 LoRA 微调工具之一，Colab 免费 GPU 可直接运行。本指南中文友好，适合作为第一个微调实战项目。

_Last updated: 2026-04-04_
