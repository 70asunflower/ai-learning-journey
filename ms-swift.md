---
name: ms-swift
description: 魔搭社区大模型与多模态大模型微调部署框架
type: reference
---

# ms-swift 框架

> 官方文档：https://swift.readthedocs.io/zh-cn/latest/

## 简介

ms-swift 是魔搭社区提供的大模型与多模态大模型微调部署框架。

## 关键特性

- **600+ 纯文本大模型**：Qwen3、Qwen3-Next、InternLM3、GLM4.5、Mistral、DeepSeek-R1、Llama4 等
- **300+ 多模态大模型**：Qwen3-VL、Qwen3-Omni、Llava、InternVL3.5、MiniCPM-V-4、Ovis2.5、GLM4.5-V、DeepSeek-VL2 等

### 训练技术

- **Megatron 并行技术**：TP、PP、CP、EP 等加速
- **强化学习算法**：GRPO、DAPO、GSPO、SAPO、CISPO、RLOO、Reinforce++ 等
- **偏好学习算法**：DPO、KTO、RM、CPO、SimPO、ORPO 等
- **支持任务**：Embedding、Reranker、序列分类

### 部署与量化

- **推理加速**：vLLM、SGLang、LMDeploy
- **量化技术**：GPTQ、AWQ、BNB、FP8

## 全链路支持

```
训练（预训练/微调/对齐） → 推理 → 评测 → 量化 → 部署
```

## 相关链接

- [官方文档](https://swift.readthedocs.io/zh-cn/latest/)
- [Qwen3-VL 最佳实践](./Qwen3-VL-Best-Practice.md)
