---
title: Hatch 的 Agent Runtime 哲学
source_kind: codex_session
source_ref: thread://019f0294-b6b0-7a61-9e7c-6f8ea9a251c9
provenance: observed
selection_reason: 跨多次技术讨论保持稳定的协议、云端与本地边界及安全原则
creator_approved: false
---

# Hatch 的 Agent Runtime 哲学

## 学习 protocol，不照搬 implementation

Hatch 应学习 Codex、Claude Code 和 Agent Skills 等成熟系统的协议与运行机制，但不绑定某一家模型厂商的具体 API 或 hosted tool implementation。

Skill、Tool、session、event stream、approval 和 progressive disclosure 应尽量遵循成熟开放定义。模型调用层保持 model-agnostic，避免把某个 SDK、模型名或供应商变成产品概念。

## Server 与 Desktop 的责任

```text
Server
├── Agent thinking / agent loop
├── session 与 chat history
├── Skill discovery 与加载
├── Tool routing 与 policy
├── 云端 API、Web、MCP 和 integrations
└── auth、billing、evals、traces

Desktop / local runner
├── Workspace 授权
├── filesystem read/write
├── shell / process / git
├── 本地审批与取消
└── 确定性的工具执行
```

Server 不应根据用户电脑上的绝对路径直接读取文件。本地 runner 负责 path containment 和 OS boundary；Server 只看到经过授权的 capability 和 Tool Result。

对 Agent 来说，broker 不应成为额外概念。它只是在调用普通 Tool；工具最终由云端还是本地执行，是 Runtime 的路由责任。

## 产品表面

- Web 是浏览、购买、订阅和 Creator 管理的业务端；
- Registry 是 Agent 产品与版本的 authority；
- Runtime 负责运行 Agent；
- Desktop 是用户使用完整 Creator Agent、连接本地 Workspace 并完成工作的主要客户端。

## 保护 Creator 的方法

目标不是让 Agent 少知道，而是让 Agent 能完整使用 Creator 的方法完成工作，同时不泄露内部 System Prompt、Skill、reference、私有资料、工具配置或凭据。

正常回答应输出结果，不复现底层方法文件。Hatch 不向消费者展示模型的私有 thinking 过程；Tool、approval 和工作状态可以用产品化 UI 展示。

## 不应写死的内容

- 当前模型名称；
- 当前云厂商；
- 临时 endpoint；
- 某一 SDK 的类名；
- 调试 harness；
- 已被替换的本地 Runtime 叙事。

## 来源

- Codex task `019f0294-b6b0-7a61-9e7c-6f8ea9a251c9`
- Codex task `019f7137-065c-74f1-9fd6-3d7ce5ed277b`
- Codex task `019fe5d0-e7b7-7971-a4ac-a5c233a748b0`
- Codex task `019fd52e-ec4c-73b2-be36-51b6f285dc05`
- 关键时间：2026-06-26 至 2026-08-10

