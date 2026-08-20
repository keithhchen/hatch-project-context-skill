---
title: Creator 蒸馏与质量系统
source_kind: codex_session
source_ref: thread://019ff138-fb97-7830-9c5e-04c01d2a424c
provenance: observed
selection_reason: 对 Creator 蒸馏输入、监督角色、Eval、失败回流和发布门槛的连续讨论
creator_approved: false
---

# Creator 蒸馏与质量系统

## 基本单元

蒸馏的最小产品单元是：一个 Creator、一个边界清楚的 SKU、一个待验证的版本。不要一开始试图复制 Creator 的全部能力。

先定义用户愿意购买的工作和可验收交付物，再决定需要提取哪些方法、数据、案例、Tools 和标准。

## 原材料优先级

Creator 当前对真实案例的批改和纠正最有价值，因为它直接暴露选择、标准和边界。其次是 Creator 授权的课程、文档、案例、历史交付和示范。公开内容主要用于补充背景，通常不足以展示真实决策过程。

经 Creator 明确授权后，Codex 工作记录也可以成为上下文来源，但不能默认扫描；必须限定任务或日期范围，过滤工具日志、凭据、第三方私人内容和无关项目。

## Creator 的角色

Creator 是 build-time supervisor，而不是产品上线后的常驻 human-in-the-loop。

在发布前，Creator 通过少量高价值行为提供监督：

- 批改真实或合成案例；
- 做 pairwise judgment；
- 修改标准答案或 rubric；
- 指出不符合自己的重点、取舍和边界；
- 确认候选版本是否达到署名标准。

上线后，普通运行不应依赖 Creator 实时参与；只有明确的边界案例才升级给本人。

## 质量闭环

建议的质量循环是：

```text
Evidence
→ Corpus Candidate
→ 生成式任务与候选结果
→ Eval 评估结果
→ Creator correction / failure reflection
→ Corpus 修正
→ regression + calibration
→ held-out gate
→ 发布
```

Eval 评估的是 Agent 生成的结果，而不只是让 Creator 回答一组 QA。Eval 失败不能只重新生成 held-out set；失败需要形成可消费的 correction、few-shot 或整体反思，并回流给 Corpus 生成环节。

先证明产品“与 ChatGPT 不同且有用”，再证明它在 Creator 未见过的 held-out cases 上持续有用。

## “源头的源头”

系统可以从资料中推测影响 Creator 的传统、人物和世界观，例如某位创业导师可能受到哪些企业家或思想流派影响。这类内容只能标为 `inferred`，展示证据并要求 Creator 确认、修改或拒绝；不得作为既定事实直接写入产品。

## 来源

- Codex task `019ff138-fb97-7830-9c5e-04c01d2a424c`
- Codex task `019fea3c-eca5-71b3-990d-7127f6c21fda`
- 关键时间：2026-08-11T14:30:26Z 至 2026-08-11T15:05:46Z

