---
source: https://pdos.csail.mit.edu/6.824/
date: 2026-09-01
tags: [distributed-systems, raft, mapreduce, go, fault-tolerance, replication, consistency, mit, course]
links:
  - https://pdos.csail.mit.edu/6.824/
  - https://pdos.csail.mit.edu/6.824/schedule.html
  - https://pdos.csail.mit.edu/6.824/labs/lab-mr.html
  - https://pdos.csail.mit.edu/6.824/labs/lab-raft1.html
---

# MIT 6.5840 (原 6.824) — Distributed Systems

> MIT CSAIL PDOS 组的分布式系统研究生核心课（现编号 6.5840，前身 6.824），Spring 2026 开课中。三大主线：**容错（fault tolerance）、复制（replication）、一致性（consistency）**，以经典分布式系统论文 case study + 5 个硬核 Go 编程 lab 闻名，是分布式训练/推理 infra 的系统课地基。

## 课程概况

- **性质**：研究生 12-unit 核心课，讲座 + 论文研读 + 编程 lab + 期中/期末
- **先修**：计算机系统基础（6.1910/6.004）+ 系统工程课（6.1800/6.033 或 6.1810/xv6），需较强编程能力
- **语言**：Go（所有 lab）
- **社区**：Piazza 问答；历年站点（2000-2025）全公开，讲义/论文/quiz 自学友好
- **注意**：Gradescope 提交仅限选课学生，自学走历年网站即可

## 5 个 Lab（递进式，全部 Go）

| Lab | 内容 | 核心能力 |
|-----|------|----------|
| Lab 1 | MapReduce | 分片、worker 调度、崩溃恢复、协调者容错 |
| Lab 2 | KV Server（无 Raft） | 线性一致性（linearizability）、客户端会话、重复请求去重 |
| Lab 3 | Raft | 领导者选举、日志复制、持久化、崩溃恢复 |
| Lab 4 | KV Raft | 在 Raft 之上建 KV 服务（快照、日志压缩、去重） |
| Lab 5 | Sharded KV | 分片控制 + 配置迁移（rebalancing），含 ShardKVs 的迁移与垃圾回收 |

## 核心论文主题（典型讲次）

GFS、MapReduce、primary/backup 复制、**Raft**（共识）、ZooKeeper、线性一致性与因果一致性、两阶段提交/分布式事务（Spanner、FaRM）、memcached/Redis 缓存、崩溃恢复（RRaft-Aries）、FLP 不可能性、容错虚拟机（FT-VM）等。2026 版 schedule 以站点为准：https://pdos.csail.mit.edu/6.824/schedule.html

## 为什么放进 AI 学习路径

- **分布式训练/推理的底层语义**：参数服务器、数据并行里的 collective、检查点恢复、容错调度，本质都是这课讲的问题（复制、一致性、故障恢复）
- **vLLM/Ray/K8s 这类系统栈**：读完 Raft lab 再看 etcd/K8s 控制面会豁然开朗
- **面试硬通货**：Raft 手写实现是国内大厂 infra 岗高频考点
- 姊妹课 6.1810 (xv6) 打底 OS，本课向上接分布式；与「10 门地狱级 CS 公开课」条目里其它系统课互补

## 学习建议

1. 先修 xv6 或等价系统课基础（线程/RPC/锁）
2. 按顺序做 lab，**Lab 3 (Raft) 是分水岭**——预留至少 2-3 周整块时间
3. 每篇论文课前读 + 课后对照 lecture notes 补漏
4. 自学者用历年网站（如 https://pdos.csail.mit.edu/6.824/2022/ 有完整视频）

_Last updated: 2026-09-01_