---
title: zero-to-sglang (Datawhale × RadixArk)
short: zero-to-sglang
summary: Datawhale×RadixArk 联合出品推理引擎课：概念→手搓 mini-sglang→读 SGLang 源码→提 PR，中英双语
source: https://github.com/datawhalechina/zero-to-sglang
date: 2026-11-10
tags: [sglang, inference, from-scratch, course, chinese, datawhale, llm, serving]
---
# zero-to-sglang 从零构建 SGLang

> **Datawhale** 与 **RadixArk**（SGLang 团队创立的公司）联合出品的推理引擎课程，1.8k★。
> 定位非常明确：先讲清"推理到底在做什么"，再**手写一个 mini-sglang**，然后回到真实 SGLang
> 源码理解前沿优化，最后带你走完提第一个 PR 的全流程。中英双语（`course-material/ch/` 与
> `eng/`），2026-08-24 开写，**2026-11-10 全部章节完稿**；配套视频预计 11 月底上线。

## 为什么值得看

推理框架的教程通常走两个极端：要么停在概念层不碰代码，要么直接把你丢进 SGLang 源码里
不知道从哪下手。这门课走中间路线——**每个抽象都落到一份可运行的代码上**：

- 概念 → 为什么需要 KV Cache、prefill 与 decode 的区别、compute-bound 与 memory-bound 的真实含义
- 实现 → 从 200 行 forward 开始，逐层加 KV Cache、HTTP 服务、Continuous Batching、Paged KV Cache、RadixAttention
- 源码 → 回到真实 SGLang 看这些机制在生产实现里怎么做
- 参与 → profiling / trace 分析 + CI 与 review 流程

## 课程结构（4 部分 + 预备）

| 部分 | 章 | 关键内容 |
|------|----|----------|
| **Part 0 预备** | 0.1 编码伦理与开源精神 | 管好自己的代码、像人一样沟通、先 profile、开源协作规范 |
| | 0.2 部署第一个 SGLang 服务 | 环境搭建；在自己的 GPU 上跑 Qwen3-0.6B |
| **Part I 基础**（纯概念，无代码、无 GPU） | 1. LLM 导论 | LLM 是什么与演进、Transformer 架构、自回归生成 |
| | 2. 推理导论 | 训练 vs 推理、prefill/decode、compute-bound vs memory-bound、Roofline 模型 |
| | 3. GPU 导论 | GPU 架构基础、推理在 GPU 上如何执行、从硬件角度理解瓶颈 |
| | 4. KV Cache | 从 attention 推导 KV Cache、缓存生命周期、显存定量分析 |
| | 5. Benchmark 导论 | TTFT / TPOT / ITL / Goodput、分位数与尾延迟、如何设计与读 benchmark |
| **Part II 手搓 Mini SGL** | 1. 推理引擎长什么样 | 整体架构、模块拆分、本部分路线图 |
| | 2. 请求的一生（真实 SGLang） | 一个请求从到达到响应的完整生命周期 |
| | 3. 第一个 200 行 | embedding / attention / LM head 与生成的源码走读 |
| | 4. KV Cache：从 O(n²) 到 O(n) | 实现缓存并优化 attention 计算 |
| | 5. HTTP 与并发请求 | HTTP 基础与请求流；隔离、流式输出、取消 |
| | 6. Continuous Batching 与调度器 | 连续批处理、调度器状态、资源上限、延迟与吞吐权衡 |
| | 7. Paged KV Cache 与显存管理 | 分页 KV Cache 与 GPU 显存管理 |
| | 8. RadixAttention 与前缀缓存 | 基数树 + 前缀复用 |
| | 9. 多进程与张量并行 | 多进程执行与 TP |
| | 10. 投机解码 | 起草与验证、贪心/采样接受、拒绝修正、性能权衡 |
| **Part III 前沿技术**（深入真实 SGLang） | 1. Attention 后端 | FlashInfer / Triton / FA3 / FlashMLA 的职责、tiled attention、选型 |
| | 2. 量化与低精度推理 | 数值格式与 scale、decode 加速、KV Cache 容量、精度权衡、量化标签与加载 |
| | 3. 分层缓存 | L1/L2/L3 缓存层级、前缀匹配、备份恢复、预取 |
| | 4. 扩展：DP Attention / EP / PP | TP 的扩展上限、DP Attention、EP、PP 与组合并行 |
| | 5. Prefill-Decode 分离 | prefill 干扰、请求交接、KV 传输开销、资源配比与负载评估 |
| **Part IV 参与贡献**（可选） | 1. 用 Cookbook 部署 | 配方选择、启动配置、服务校验、小规模 benchmark |
| | 2. Profiling 与 Trace 分析 | profiling 基础 + 一个已合并 PR 的完整案例：trace、改动、验证 |
| | 3. SGLang PR 流程 | 开源协作、PR 生命周期、CI 与 review、第一次贡献 |

## 与库内资源的分工

| 资源 | 层级 | 与本文的关系 |
|------|------|--------------|
| [大模型推理系统入门](llm-inference-system-intro.md) | 概念地图 | 先读它拿到全局技术地图，再进本课的 Part I 补硬件与指标细节 |
| [nano-vllm](../4-Tools-Frameworks/nano-vllm.md) / [mini-sglang](../4-Tools-Frameworks/mini-sglang.md) | 极简实现 | 两处是"读代码"，本课是"**跟着写代码**"：Part II 就是把 mini-sglang 的思路逐步实现一遍 |
| [vLLM 中文文档](../1-Official-Docs/vllm-docs-zh.md) | 官方文档 | 引擎层 API 与部署参数查文档；本课负责机制理解 |
| [Infinitensor 冬令营](infinitensor-winter-camp-2025.md) / [Infra Seminars 2026](infra-seminars-2026.md) | 课程 | 更宽的 infra 全栈视角；本课是单点打穿的推理引擎专精路线 |

**建议顺序**：推理系统入门（1 天）→ 本课 Part I（无 GPU，1 周）→ 本课 Part II 手搓（2–3 周，
与 nano-vllm / mini-sglang 对读）→ Part III 挑与当前工作相关的章（量化 / PD 分离 / 并行）。

## 前置与硬件

- Python 熟练 + 软件工程基本习惯；PyTorch 与神经网络基础；线代与概率（知道矩阵乘和 attention 怎么算即可）
- CUDA 基础**不要求**（Part I 从零补）；**Part I 完全不需要 GPU**，Part II 大部分可在 CPU 调试，
  Part III 的完整实现与性能测试建议上 GPU（云也行）
- 无 GPU 也能走完 60% 的内容，这是它比多数推理课门槛低的地方

## 注意点

- ⚠️ 仓库约 **133 MB**（含图片/站点资源），`git clone` 慢；只要正文可加 `--depth 1`
- License：README/LICENSE 声明 **CC BY-NC-SA 4.0**（GitHub 未自动识别 SPDX，转载前以原文为准）
- 视频课标"11 月底补完"，Youtube / B 站链接会陆续补进 Syllabus，目前以文字版为准
- 在线阅读：[中文](https://datawhalechina.github.io/zero-to-sglang/ch/) ·
  [English](https://datawhalechina.github.io/zero-to-sglang/eng/)

## 个人备注

目前 AI Infra 学习里最缺的一块恰好是"引擎内部怎么组织"——之前读 nano-vllm / mini-sglang
基本是看代码猜意图，缺一条从概念到实现的连续推导。这门课的 Part II 按"加一个特性 → 跑一次
性能对比"组织，正好补这条线；Part III 的 PD 分离与量化两章和手上的推理侧工作直接相关，
优先级排在 Part IV 之前。

_Last updated: 2026-11-10_
