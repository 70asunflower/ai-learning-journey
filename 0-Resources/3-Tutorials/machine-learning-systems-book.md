---
title: Machine Learning Systems (Harvard CS249r)
summary: MIT Press 2026 两卷本：单机→fleet 规模 28 章，配 TinyTorch/MLSys·im/Labs 生态
source: https://mlsysbook.ai/
date: 2026-10-20
tags: [ml-systems, ai-infra, tinyml, distributed-training, inference, hardware, mit, book, open-access]
links: 
- https: //github.com/harvard-edge/cs249r_book
---
# Machine Learning Systems（Harvard CS249r · MIT Press 2026）

> 哈佛 Vijay Janapa Reddi 团队的 ML 系统教材，MIT Press 2026 出版、**完全免费开放**（GitHub 28k★，月均 3.2 万读者 / 210 个国家）。自我定位「AI engineering 的物理学」——**principles-first**，从单机到 fleet 规模讲 ML 系统如何被构建、优化与部署。两卷本 + 完整课程生态（交互 Lab / 从零造框架 / 性能建模 / 真硬件部署 / 面试题库）。

## 两卷结构（共 28 章）

### Volume I — Introduction to Machine Learning Systems（单机）

| 部分 | 章节 |
|------|------|
| Part I Foundations | ML Systems · ML Workflow · Data Engineering |
| Part II Development | Neural Computation · Network Architectures · ML Frameworks · Model Training |
| Part III Optimization | Data Selection · **Model Compression** · **Hardware Acceleration** · Benchmarking |
| Part IV Deployment | Model Serving · ML Operations · Responsible Engineering |
| 附录 | D·A·M 分类法（Data/Algorithm/Machine 三元）、各维度基础、System Assumptions、Glossary |

### Volume II — Machine Learning Systems at Scale（fleet 规模）⭐

| 部分 | 章节 |
|------|------|
| Part I The Fleet | Compute Infrastructure · **Network Fabrics** · Data Storage |
| Part II Distributed ML | **Distributed Training** · **Collective Communication** · Fault Tolerance · Fleet Orchestration |
| Part III Deployment at Scale | **Performance Engineering** · **Inference at Scale** · Edge Intelligence · ML Operations at Scale |
| Part IV The Responsible Fleet | Security & Privacy · Robust AI · Sustainable AI · Responsible AI |
| 附录 | Single-Machine Foundations (D·A·M) · **C³ 分类法**、Fleet/Communication/Reliability/Inference 基础 |

> Vol II 是这本书对你最直接的部分：计算基建、网络 fabric、集合通信、分布式训练、推理服务、性能工程——正是 AI Infra 岗的核心知识域。

## 课程生态（不止是书）

| 组件 | 作用 |
|------|------|
| **Labs** | Marimo 交互笔记本：改参数看哪里崩，建立直觉 |
| **TinyTorch** | 20 个递进模块从零造 ML 框架（零魔法） |
| **MLSys·im** | 第一性原理性能建模，一条命令定位瓶颈 |
| **Hardware Kits** | Arduino / Seeed / Grove / 树莓派真机部署，真实内存与功耗预算 |
| **StaffML** | ML 系统岗面试题（物理推导向）+ mock interview |
| **Instructor Hub** | 两学期教学大纲、教学法指南、评分标准、TA 手册 |
| **Lecture Slides** | 35 套 Beamer 讲义 + 280 张原创 SVG 图 |

## 许可（按组件不同，引用时注意）

| 组件 | 许可 |
|------|------|
| 教材 / Labs / Kits / Slides / 讲师材料 | CC-BY-NC-SA 4.0（非商业，需署名，相同方式共享） |
| TinyTorch | MIT（可商用） |
| MLSys·im | Apache 2.0（可商用） |
| StaffML | AGPL v3（copyleft，改造后提供服务须开源） |

## 与库内资源的分工

- **vs Ultra-Scale Playbook**：那本专精训练并行（DP/TP/PP/CP/EP + ZeRO）实战，这本 Vol II 覆盖更宽（网络 fabric / 集合通信 / 容错 / 推理 / 可持续性）
- **vs 深入理解 AI Infra（李博杰）**：中国视角、量化估算方法论、"数据搬移"主线；这本是 MIT Press 教材体例，principles-first + 完整课程包
- **vs JAX Scaling Book**：那本是 JAX 单栈实操，这本是跨框架的系统原理
- **互补 MIT 6.5840**：6.5840 给分布式系统基础（Raft/一致性），这本 Vol II 给 ML 场景下的分布式训练与推理

## 建议读法

1. **Vol I 的 Part III（压缩/硬件加速/benchmark）** + **Vol II 的 Part II（分布式训练/集合通信）** 优先——与你 CUDA + 推理优化主线最贴
2. 配合 **MLSys·im** 做量化估算练习（比纯读公式有效）
3. **TinyTorch** 当造框架的实战补充，比读源码门槛低
4. 面试准备用 StaffML（物理推导型问题，和外企 infra 岗考察方式接近）

_Last updated: 2026-10-20_