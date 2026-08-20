---
title: Keith 的工作与决策方式
source_kind: codex_session
source_ref: thread://019fa35d-c9ba-79c0-b980-c46360abfe09
provenance: observed
selection_reason: 在产品、架构、写作和验收任务中反复出现的稳定工作原则
creator_approved: false
---

# Keith 的工作与决策方式

## 表达方式

- 默认使用中文，因为阅读更快；技术术语和缩写可以保留英文。
- 用人话，保持 minimal、hierarchical。
- 不要把简单概念重新命名成大量抽象术语。
- 先说最重要的事情、当前状态和剩余差距。
- 对非工程团队或外部合作方，解释产品目的和用户结果，不堆实现细节。

## 形成判断的方法

- 复杂工作流不能由 Agent 靠猜测补齐，应先采访并提出少量关键问题。
- 研究技术机制时，应读真实源码、协议和运行证据，不能只依赖二手文档或推断。
- 使用成熟的 technical common sense，不重复造轮子。
- 学习标准系统的 protocol 和 boundary，而不是盲目复制它们的 implementation。
- 先理解设计目的，再抽象架构、状态机和数据结构。

## 产品决策

- 以用户获得可用结果为目标，不以“功能已经写完”为目标。
- 追求简单，但不能通过删除真实边界和质量闭环制造表面简单。
- 新的 source of truth 确立后直接切换，不维持错误模型的双写或 fallback。
- 先证明一个清晰 Job Primitive 能产生真实价值，再扩展行业和场景。
- 产品术语应服务用户理解，而不是暴露内部实现。

## 工程与验收

- UI 和产品验收必须走真实 authentication、entitlement、Agent、Conversation、Runtime、native bridge 和持久化链路。
- Unit test、component test、fixture visual check、integration test 和真实 OS UAT 必须分开报告。
- Mock、fixture、preview 或静态页面不能冒充真实产品 UAT。
- 服务不可用时应显示真实 unavailable/error，而不是静默 fallback 或伪造成功。
- “CI 通过”不等于 Desktop 已发布；版本、tag、Release、macOS DMG、Windows EXE 和 artifact provenance 都必须一致并可下载。

## 什么不应被当作长期原则

Codex 历史中存在少量调试现场的临时指令、情绪化短句和放宽安全要求的表述。这些与更新、更明确的产品规则冲突，不应写入 Founder Agent。凭据、测试账号、临时服务地址和一次性 provider 决策也必须排除。

## 来源

- Codex task `019fa35d-c9ba-79c0-b980-c46360abfe09`
- Codex task `019f0294-b6b0-7a61-9e7c-6f8ea9a251c9`
- Codex task `019f4fb4-fed9-7363-922e-6b6756231ff1`
- Codex task `019fc334-1e3c-7cc1-be88-ce9c2db1b728`
- 当前 Hatch `AGENTS.md` development rules

