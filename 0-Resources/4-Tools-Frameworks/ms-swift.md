---
source: https://swift.readthedocs.io/zh-cn/latest/
date: 2026-03-31
tags: [fine-tuning, deployment, vision, multi-modal, swift]
---

# ms-swift

> ModelScope's fine-tuning & deployment framework for LLMs and multi-modal models.
> Official docs: https://swift.readthedocs.io/zh-cn/latest/

## Overview

ms-swift supports 600+ text LLMs and 300+ multi-modal models through the full pipeline: training → inference → evaluation → quantization → deployment.

## Key Capabilities

### Training

- **Lightweight**: LoRA, QLoRA, DoRA, LoRA+, LLaMAPro, LongLoRA, LoRA-GA, ReFT, RS-LoRA, Adapter, LISA
- **Full-parameter**: DDP, DeepSpeed ZeRO2/3, FSDP/FSDP2, Megatron (TP/PP/SP/CP/ETP/EP/VPP)
- **Memory**: GaLore, Q-Galore, UnSloth, Liger-Kernel, Flash-Attention 2/3, Ulysses, Ring-Attention
- **Quantization training**: BNB, AWQ, GPTQ, AQLM, HQQ, EETQ — 7B training needs only 9GB VRAM
- **Multi-modal**: Packing (100%+ speedup), text/image/video/audio mixed training, vit/aligner/llm separate control
- **Reinforcement learning**: GRPO, DAPO, GSPO, SAPO, CISPO, CHORD, RLOO, Reinforce++
- **Preference tasks**: DPO, KTO, RM, CPO, SimPO, ORPO, GKD

### Inference & Deployment

- **Engines**: PyTorch, vLLM, SGLang, LmDeploy
- **API**: OpenAI-compatible interface
- **Quantization export**: AWQ, GPTQ, FP8, BNB
- **Evaluation**: EvalScope backend with 100+ datasets

### Hardware

- NVIDIA: A10, A100, H100, RTX series, T4, V100
- CPU, MPS
- Ascend NPU (domestic)

## Why ms-swift?

- **Day-0 support** for popular models
- **150+ built-in datasets** for pre-training, SFT, human alignment, multi-modal
- **One-command training** — just prepare your dataset and go
- **Web-UI** available for training, inference, evaluation, and quantization

---

*Last updated: 2026-03-31*
