---
title: AI Infra 大话西游 (Ringi)
short: AI Infra 大话西游
summary: 大厂工程师 Ringi 的 AI Infra 全栈专栏：9 卷 44 讲 + 5 个 Capstone，三账本/算子/GPU 互联/分布式训练/推理/云原生
source: https://github.com/lilinji/ai-infra-odyssey
date: 2026-11-21
tags: [ai-infra, llm, gpu, cuda, distributed-training, inference, tutorial, chinese, book, kernel, serving, optimization]
---
# AI Infra 大话西游之水滴石穿

> 作者 **Ringi Lee**（大厂 AI Infrastructure 工程师），副标题「从基础设施到智能未来的工程哲学与实战指南」。
> **170★ / 24 forks**，Python，仓库创建于 2026-09-10、最后 push 2026-09-28（2026-11-21 核验）。
> 定位是面向想进大厂 AI Infra / GPU 计算 / 大模型分布式训练与推理优化 / 云原生平台的工程师与架构师。

## 规模与形态

| 项 | 内容（README 口径） |
|------|------|
| 内容量 | 全书 **9 大分卷 · 44 篇万字核心讲义 + 5 大生产级 Capstone**，声明"全套 49 篇已 100% 完结交付" |
| 学习时长 | 80 小时核心必修 + 12 小时选修扩展 + 5 大企业级实战 |
| 文档形态 | **Mintlify** 交互式技术专著（Claude Docs 陶土色视觉 + 暗黑模式 + Diátaxis 架构），源码在 `docs/`，共 **62 篇 MDX**（口径与上面的 49 篇不一致，见注意事项） |
| 配套资产 | 全景 8 层架构图 SVG、9 页企业级交付汇报 SVG + 可编辑 PPTX、封面图、LaTeX 公式规范、自动公式校验脚本 |
| License | **README 未声明**，GitHub API 也未识别 SPDX；引用/转载前需向作者确认 |

## 九卷大纲

| 卷 | 讲数 | 关键内容 |
|----|------|----------|
| **一 · 性能工程与系统前置基石** | 11 | C++/Python 底层与 PyBind11、GEMM 算力账本、Cache Line/NUMA、perf/eBPF、PyTorch 内存布局与 Autograd 生命周期、CUDA Stream/CUDA Graph、Transformer 算子执行图、Collective 原语、三账本建模、Profiler 实战 |
| **二 · GPU 硬件微架构与集群互联** | 10 | SM/Warp/Tensor Core/HBM3e + Roofline、Alpha-Beta 通信模型、PCIe/NVLink/NVSwitch/Fat-Tree/Rail、RDMA 与 GPUDirect、TMA/Copy Engine/mbarrier、GPU-Initiated RDMA、NCCL 拓扑切换、通信计算重叠、XID 掉卡与 NCCL Hang 诊断、异构算力选型 |
| **三 · CUDA 编程与高性能算子优化** | 4 | CUDA 内存层次与合并访问、Reduce/Online Softmax/RMSNorm 融合、GEMM 六级优化与 Tensor Core、FlashAttention-1/2 与 Triton |
| **四 · 大模型架构与显存精细建模** | 2 | MHA/MQA/GQA 演进、RoPE、SwiGLU；训练与推理四大显存账本、7B/70B 手算、KV Cache 容量模型 |
| **五 · 大规模分布式训练系统** | 4 | DDP 梯度分桶与重叠、ZeRO-1/2/3 与 FSDP-2、TP/PP/SP/CP 的物理映射、Megatron 3D + MoE 专家并行与万卡排障 |
| **六 · 在线推理系统与性能工程** | 5 | Prefill vs Decode 与 TTFT/TPOT、PagedAttention 与连续批处理、vLLM 的 Chunked Prefill/投机采样/前缀缓存、PD 分离、容量规划与 SLO 治理 |
| **七 · 云原生 AI 平台与生产工程** | 4 | Container Toolkit / Device Plugin / DRA、Gang 调度 / Kueue / HAMi、Serving 高可用与 P99 契约、四级存储金字塔与百秒级自愈 |
| **八 · Post-Training 与相邻 Infra** | 4 | SFT/LoRA/RLHF 资源评估（PPO/DPO/GRPO）、RAG 与 Agent 基础设施、NPU/DPU 异构抽象、大厂系统设计题库 |
| **九 · 生产级 Capstone** | 5 | 见下表 |

## 五大 Capstone

| 项目 | 实战内容 |
|------|----------|
| 1. 万卡 Scaling Study | 手撕 64 卡跨机 18 倍网络断崖、DDP 梯度重叠临界点、FSDP 1.5 倍通信税，输出扩展性仿真报告 |
| 2. Serving 吞吐倍增与 P99 治理 | 电商客服场景，实测 Chunked Prefill 重叠，声称吞吐翻倍、P99 延迟降 65%（作者自述，未独立复核） |
| 3. 榨干片上 SRAM | Online Softmax 单趟递推证明、SRAM 分块与 Bank Conflict 消除、复现高保真 FlashAttention-2 核心内核 |
| 4. 平台架构设计 RFC | RFC-AI-0045：Gang 调度、Kueue 弹性配额、HAMi 显存硬隔离、8×400G 双轨网络、XID 容灾自愈 |
| 5. FlashAttention 全景与 Token 生成链路 | FA-1/2/3 微架构演进、FlashDecoding、Decode 阶段 GEMV 访存账本、PagedAttention 到 PD 分离全链路 |

## 这个专栏的方法论

- **三账本**：算力（Compute）/ 显存（Memory）/ 通信（Communication）三本账，遇到瓶颈先算账再谈优化。
- **Ringi 工程师三问闭环 / No Naked Formula 2.0**：每篇必须回答 Shape 是什么、钱花在哪、机器上怎么跑、Evidence 在哪、Production 怎么选——不允许只堆名词或给简化版伪代码。
- 配套 `python3 scripts/verify_latex_formulas.py` 做公式语法与 GitHub 渲染校验；`DESIGN.md`、`theme/`、`templates/` 是可复用的写作与视觉规范。

## 学习路线

- **初学者**：第一篇（系统前置）→ 第二篇（硬件微架构）→ 第三篇（CUDA 算子）→ 第四篇（显存建模）→ 第五/六篇（训练与推理系统）。
- **资深架构师**：直奔第九篇的五个 Capstone，用万卡 Scaling、Serving 优化、SRAM 算子压榨与平台 RFC 检验全栈内功。

## 与库内资源的分工

| 资源 | 关系 |
|------|------|
| [深入理解 AI Infra](../3-Tutorials/bojieli-ai-infra-book.md) | 同类全景书，李博杰那本偏"数据搬移主线 + 定量估算"；这本从 C++/PyTorch 底层一路写到万卡平台与面试题库，工程粒度更细 |
| [AI Infra 其实没有多少新东西](../3-Tutorials/ai-infra-nothing-new.md) | 先读这篇短文建立直觉，再进本专栏逐层算账 |
| [Modern GPU Programming For MLSys](../3-Tutorials/mlc-modern-gpu-programming.md) | 与第三篇 CUDA/FlashAttention 章节互补：MLC 那门更偏 Blackwell 新硬件特性 |
| [The Ultra-Scale Playbook](../3-Tutorials/ultrascale-playbook.md) | 与第五篇分布式训练重叠；Playbook 偏 HuggingFace/nanotron 实战，这里偏原理推导与通信账本 |
| [大模型推理系统入门](../3-Tutorials/llm-inference-system-intro.md) / [zero-to-sglang](../3-Tutorials/zero-to-sglang.md) | 第六篇的 PagedAttention/PD 分离在这里讲系统账，后两者带你手搓实现 |
| [AIPerf (NVIDIA)](../4-Tools-Frameworks/aiperf.md) | 第六篇容量规划与 SLO 治理的实测工具端 |

## 注意点

- ⚠️ 仓库约 **306 MB**（含 SVG/PPTX 等资产），`git clone` 建议加 `--depth 1`。
- ⚠️ README 对篇数有两种说法：顶部"49 篇（44 讲 + 5 Capstone）"，文档预览处"62 篇 MDX"；后者可能计入了模板/规范类文件，引用时以原文两种口径为准。
- ⚠️ **没有公开在线站点**：只提供本地 Mintlify 预览（`npm run dev` 或 `npx mintlify dev --dir docs --port 3001`，访问 `http://localhost:3001`），需要先 clone。
- License 未声明，GitHub 也未识别 SPDX，商用/转载前先问作者。

## 个人备注

库里已有的 AI Infra 全景资源都是"讲清一条主线"，这本是少见的**把 44 讲按工程师成长顺序串成必修课**的写法：每讲都在回答"机器上到底怎么跑"，还配了五大 Capstone 和面试题库。第五篇的通信账本、第七篇的云原生调度正好补上我之前只零散看过的部分；先把第一篇和第二篇过一遍建立账本直觉，再按当前工作挑第五/六篇深读。

_Last updated: 2026-11-21_
