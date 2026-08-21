---
title: Hatch 的 Product authority 与版本模型
source_kind: codex_session
source_ref: thread://01a009a1-d72c-7be1-8e36-2f7ca4b47a8a
provenance: observed
selection_reason: Keith 明确纠正旧模型并确认 Product-only source of truth
---

# Hatch 的 Product authority 与版本模型

## Canonical model

```text
Product
├── Files
├── Source Snapshots
└── Versions / Runs
    └── source_snapshot_id
```

Files 属于 Product，而不是 Version。Product Files 是持续存在的原材料集合；当用户启动新的 Run 时，系统从当时的 Product Files 锁定一个不可变 Source Snapshot。Version 或 Run 只引用该 Snapshot。

Product 和 Task 不能同时成为同一产品生命周期的 authority。旧的 Task-centric 模型已经被 Product-only 模型替代，不应继续通过双写、隐藏兼容接口或第二套 ID 维持。

## 为什么需要不可变 Snapshot

- 可以追溯某个 Version 使用了哪些原材料；
- 新增文件不会静默改变已经发布的 Version；
- Eval、correction 和 regression 可以绑定精确输入；
- 失败和重跑不会覆盖历史事实；
- 发布结果可以验证来源、版本和质量门槛。

## 蒸馏系统的抽象

Keith 确认过的核心抽象是：

```text
immutable artifacts
+ event graph
+ quality gates
+ derived state
```

- `immutable artifacts` 保存原材料、LLM 产物、correction、Eval 和发布候选；
- `event graph` 记录节点执行、打回、重跑和回退关系；
- `quality gates` 决定何时允许进入下一阶段或发布；
- `derived state` 从事实和事件推导当前状态，避免由多个地方分别写入冲突状态。

## FAST FORWARD, KEEP AHEAD

当新的 identity 或 source-of-truth 已经明确替换旧模型时，代码、数据、路由、测试和文档应直接切换到新模型。只有不可重写的历史事实可以在清晰的 read-time migration boundary 被读取。

不要为了兼容已经被否定的抽象而维持双重 authority。

## 来源

- Codex task `01a009a1-d72c-7be1-8e36-2f7ca4b47a8a`
- Codex task `019fff45-1450-7d00-be58-ace148ea9341`
- 关键时间：2026-08-14T14:40:56Z、2026-08-14T15:29:11Z、2026-08-16T09:27:42Z、2026-08-16T09:53:54Z
