---
source: https://www.xiaohongshu.com/ (小红书帖子 + 优化整理)
date: 2026-04-21
tags: [llm, training, distributed-training, inference, algorithm, engineering, roadmap]
---

# LLM 算法与工程学习路线

> 从算法原理到分布式训练到推理部署的完整路线，按优先级分层：🔥 必做 → 🔍 深入 → 💡 了解

## 一、LLM 算法基础

### 1.1 Tokenizer 原理 🔥
- 手写 BPE 合并过程（小语料用 Python）
- 搞懂 sentencepiece / tiktoken + `<unk>` `<eos>` `<pad>` 设计
- **补充**：理解 Byte-level BPE 为何取代 char-level（OOV 问题根源）

### 1.2 后训练算法 🔥
- **SFT**：数据质量 > 数量，chat template 设计
- **DPO**：理解 preference pair → implicit reward → policy gradient 等价
- **GRPO / RLHF (PPO)**：GRPO 无需 value model，PPO 更稳定但工程更重
- **补充**：ORPO / SimPO 等新变体了解即可，核心是 DPO + GRPO

### 1.3 模型架构演进 🔍
- 归一化位置：Pre-LN (LLaMA) vs Post-LN (GPT-2)
- 激活函数：SwiGLU vs GELU
- 位置编码：RoPE vs ALiBi vs RoPE scaling
- 注意力改进：GQA (LLaMA-2) → MQA → MLA (DeepSeek)
- MoE 架构：DeepSeek-V3 / Mixtral 的路由与负载均衡
- **建议**：不要逐个学，对比着看差异更清晰

### 1.4 Scaling Laws 💡
- Chinchilla 定律：模型参数量 vs 数据量的最优比例
- 为什么 7B 模型用 2T token 训练是欠训练
- **实用价值**：帮你决定"该训多大模型配多少数据"

### 1.5 上下文长度扩展 🔍
- RoPE scaling（NTK-aware / YaRN / Dynamic NTK）
- 训练短序列 → 推理长序列的策略
- 注意力机制的长序列瓶颈与解决思路

---

## 二、分布式训练

### 2.1 数据并行 🔥
- **DDP**：all-reduce 原理 + torch profiler 看通信耗时
- **FSDP**：分片参数/梯度/优化器状态，对比 DDP 显存（省 50%+）
  - `auto_wrap_policy` + `cpu_offload` 配置
  - FSDP vs ZeRO-1/2/3 对应关系

### 2.2 模型并行 🔍
- **TP（张量并行）**：行切/列切权重矩阵，通信量 = 2×batch×hidden
- **PP（流水线并行）**：1F1B 微批次调度，bubble 率优化
- **EP（专家并行）**：MoE 模型的专家分布策略
- 跑通 Megatron / DeepSpeed TP+PP 示例

### 2.3 显存优化 🔥
- **能预估显存占比**（这是基本功）
  - 模型参数 × 2 (FP16) + 优化器状态 × 2 (momentum+variance) + 梯度 × 1 + 激活 × N
- 激活重计算（selective recomputation 策略）
- 混合精度：FP16 需 loss scaling，BF16 无脑用
- 梯度累积（模拟超大 batch）

### 2.4 训练稳定性 🔥
- DeepSpeed ZeRO-3 配置（offload 选项）
- 训练 7B 模型（单机 8 卡试起来）
- 梯度范数监控 ｜ NaN 自动跳过 ｜ `detect_anomaly`
- **补充**：NCCL 超时 / OOM 排查是工程必修课

---

## 三、工程实践

### 3.1 Data Pipeline 🔥
- JSONL → Dataset 类 → DataLoader
- 数据配比（WeightedRandomSampler）
- 换数据配比 → 观察下游指标
- **补充**：数据去重（MinHash）和质量过滤（perplexity filter）比配比更重要

### 3.2 训练 + 评估 🔥
- 每个 step 输出 loss，每个 epoch 算 perplexity
- NaN 检测：跳过 batch / 降低 LR / 保存现场
- `torch.cuda.amp` 捕获溢出警告
- **补充**：eval loss 比 train loss 更重要，过拟合的信号在 eval 上

### 3.3 保存 / 加载 / 断点续训 🔥
- checkpoint 必须存：model、optimizer、scheduler、seed、step
- 从任意 step 恢复，loss 一致
- **补充**：自动保留最近 N 个 + 最优 checkpoint，磁盘不够别全存

### 3.4 超参调优 🔍
- 前期剧烈震荡 → 降 LR + 加长 warmup + 提 batch size
- Loss spike → 数据异常 / 梯度裁剪失效 / LR 过大
- 不同阶段 LR 经验：预训练 (1e-4~3e-4)、SFT (1e-5~5e-5)、DPO (5e-7~1e-6)、GRPO (1e-6)
- **LR 是最关键的超参，没有之一**

---

## 四、推理与部署

> **这块原清单完全缺失，但对工程落地最关键**

### 4.1 推理基础 🔥
- KV Cache 原理：为什么自回归推理的瓶颈是显存不是算力
- Prefill vs Decode 阶段差异（compute-bound vs memory-bound）
- Continuous Batching / PagedAttention（vLLM 核心思想）

### 4.2 量化 🔥
- W8A8 / W4A16 / GPTQ / AWQ / GGUF 区别与选择
- 何时用量化：7B→4bit 可在 8GB 显卡跑
- 和训练阶段 TinyML 6.5940 的量化知识打通

### 4.3 推理框架 🔍
- vLLM / TensorRT-LLM / SGLang 选型
- Speculative Decoding（小模型猜 + 大模型验）
- **实践**：用 vLLM 部署一个 7B 模型，测吞吐和延迟

### 4.4 服务化 💡
- OpenAI-compatible API 封装
- 多卡 tensor parallel 推理
- 流式输出 SSE 实现

---

## 五、评估体系

> **原清单缺失：训完怎么评测？**

### 5.1 基础评估 🔥
- 通用能力：MMLU / C-Eval / CMMLU
- 数学推理：GSM8K / MATH
- 代码：HumanEval / MBPP
- 长文本：Needle-in-a-Haystack / LongBench

### 5.2 对齐评估 🔍
- MT-Bench / AlpacaEval（指令遵循）
- 安全性评估：红队测试 / harmful prompt 拒绝率

### 5.3 评估实践 💡
- lm-evaluation-harness 使用
- 自建评测集：覆盖你的业务场景
- **关键**：eval 分数和真实体感经常不一致，人工抽检不可省

---

## 六、性能分析（进阶）

### 6.1 GPU Profiling 🔍
- 用 Nsight Systems 分析 Transformer block 瓶颈（gemm / softmax / all-reduce）
- torch.profiler + TensorBoard 可视化

### 6.2 算子优化 💡
- FlashAttention-2：对训练稳定性和速度的影响
- 读 FlashAttention-2 CUDA / Triton 代码
- 算子融合（kernel fusion）减少显存访问

---

## 优先级总结

| 阶段 | 必做 🔥 | 推荐 🔍 | 了解 💡 |
|------|---------|---------|---------|
| 算法 | Tokenizer, SFT/DPO/GRPO | 架构演进, 长上下文 | Scaling Laws |
| 训练 | DDP/FSDP, 显存预估, 稳定性 | TP/PP, 超参调优 | NCCL 排查 |
| 工程 | Data Pipeline, 评估, 断点续训 | 数据去重/过滤 | 自动 checkpoint 管理 |
| 推理 | KV Cache, 量化 | vLLM 部署 | Speculative Decoding |
| 评测 | MMLU/GSM8K | MT-Bench | 自建评测集 |

---

*Last updated: 2026-04-21*
