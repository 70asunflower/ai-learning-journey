---
source: https://llamafactory.readthedocs.io/zh-cn/latest/index.html
date: 2026-04-04
tags: [fine-tuning, framework, lora, qlora, llama, qwen, chinese-doc]
---

# LlamaFactory

## 核心要点（摘要）

开源大模型高效微调工具链，零代码 CLI/Web UI 支持 100+ LLM 和 VLM 微调。支持 LoRA/QLoRA、全量微调、冻结微调等多种方法，提供统一训练推理接口。

## 详细内容

### 主要特性

- **训练方法**：全量微调、LoRA/QLoRA（2-8bit 量化）、冻结微调、GaLore/BAdam/Adam-mini 等优化算法
- **先进算法**：DoRA、LongLoRA、PiSSA、OFT、PPO、DPO、KTO、ORPO
- **性能优化**：FlashAttention-2、Unsloth 加速、NEFTune、RoPE 缩放
- **监控工具**：LlamaBoard、TensorBoard、WandB、MLflow、SwanLab
- **推理部署**：OpenAI 风格 API、vLLM/SGLang 后端、Gradio UI

### 支持模型（部分）

LLaMA, Llama 2/3/4, Qwen/Qwen2/Qwen3, Mistral, Mixtral, DeepSeek, Gemma, GLM, Phi, InternLM, LLaVA, MiniCPM 等 100+ 模型

### 训练方式

连续预训练、SFT、奖励建模、PPO、DPO、KTO、ORPO、多模态训练、Agent 微调

## 个人备注

与 ms-swift 类似但更专注于训练侧，中文文档完善。与 Unsloth 微调指南配合使用效果佳。

_Last updated: 2026-04-04_
