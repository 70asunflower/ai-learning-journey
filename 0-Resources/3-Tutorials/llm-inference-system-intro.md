---
source: https://mp.weixin.qq.com/s/driajBoZ0iqzwLCMfss3Ng
date: 2026-06-05
tags: [llm-inference, vllm, sglang, kv-cache, continuous-batching, speculation, system-optimization]
---

# 大模型推理系统入门：从模型优化到调度优化

> 以 vLLM / SGLang 为主线，系统性建立 LLM 推理系统技术地图

## 基本信息

| 项目 | 详情 |
|------|------|
| **作者** | 一起推理吧（公众号） |
| **类型** | 系统入门科普 |

## 推理基础

- **两阶段**：Prefill（并行计算，计算密集型）→ Decode（逐 token 生成，显存密集型）
- **核心指标**：TTFT（首 token 延迟）、TPOT（每输出 token 延迟）、Throughput（吞吐量）、Tail Latency (P95/P99)

## 模型侧优化

| 技术 | 说明 |
|------|------|
| **KV Cache 管理** | PagedAttention — 分页管理，减少显存碎片（vLLM 核心技术） |
| **Attention 优化** | FlashAttention — IO-aware，减少 HBM 数据搬运 |
| **MLP 优化** | MoE — 稀疏激活，减少无效计算 |
| **分布式并行** | TP / PP / DP / EP 四种并行策略 |

## 系统侧优化

| 技术 | 说明 |
|------|------|
| **Batching** | Static → Dynamic → Continuous → Selective 演进路线 |
| **调度优化** | Chunked Prefill / Disaggregated（Prefill-Decode 分离）解决冲突与平衡 |
| **Prefix Caching** | 复用共享前缀计算，Cache-aware Scheduling |
| **Speculative Decoding** | 小模型候选 + 大模型批量验证，加速推理 |
| **Admission Control** | 限流、公平性、长尾控制 |

## 与现有资源关联

此文章的系统级视角与以下资源互补：

- [nano-vllm](https://github.com/70asunflower/ai-learning-journey/blob/main/0-Resources/4-Tools-Frameworks/nano-vllm.md) — vLLM 核心原理（PagedAttention / Continuous Batching）极简实现
- [mini-sglang](https://github.com/70asunflower/ai-learning-journey/blob/main/0-Resources/4-Tools-Frameworks/mini-sglang.md) — SGLang 另一技术路线（RadixAttention / 前缀缓存）
- [Infinitensor 夏立营 2025](https://github.com/70asunflower/ai-learning-journey/blob/main/0-Resources/3-Tutorials/infinitensor-winter-camp-2025.md) — 推理 infra 全栈训练营

_Last updated: 2026-06-05_
