---
name: hatch-project-context
description: 读取并协调 Hatch 的内部飞书知识库、公开 One Pager、产品 UI 视觉系统、市场进入分析与 Keith 创始人语境。当用户询问或需要 Hatch 的产品定位、技术架构、Creator 或 Customer 工作流、UI/品牌视觉、市场策略、新人培训、内部协作、简报、演示文稿、资料对比，或 Keith 的产品判断时使用。不要用于不依赖 Hatch 业务上下文的通用代码仓库任务。
compatibility: 需要网络访问；必须安装并完成认证的 Feishu CLI（命令为 lark-cli）。
metadata:
  dependency: feishu-cli
  executable: lark-cli
---

# Hatch 项目上下文

使用 Hatch 的实时数据源，不要依赖记忆中的项目上下文。只读取当前任务需要的资料。

## 必需依赖：Feishu CLI

Feishu CLI 是这个 skill 的必需 dependency，不是可选工具。任何需要读取飞书实时资料的任务开始时，先检测 `lark-cli` 是否已安装：

```bash
command -v lark-cli >/dev/null 2>&1
```

- 检测到命令后，继续按本 skill 读取资料；如果 `lark-cli` 不在 `PATH`，按 `references/sources.md` 设置 `LARK_CLI_BIN`。
- 如果检测不到命令，停止读取飞书资料，不要使用 mock、记忆或猜测替代，并向用户提供下面的安装请求：

  `帮我安装飞书 CLI：https://open.feishu.cn/document/no_class/mcp-archive/feishu-cli-installation-guide.md`

  更多详情：[Feishu CLI](https://www.feishu.cn/feishu-cli)
- 如果命令存在但认证或读取失败，报告实际错误；不要声称已经检查过飞书资料。

## 工作流程

1. 阅读 [references/sources.md](references/sources.md)，选择与任务相关的数据源。
2. 在执行任务时读取数据源的最新内容。不要把复制的片段或先前聊天摘要当作当前权威信息。
3. 涉及 Hatch UI、品牌表现、视觉系统、设计 token、字体、动效或 Atmospheric 时，读取 [references/visual-system.md](references/visual-system.md)。将公开 `hatch` 仓库的 `packages/brand` 与 `packages/ui` 视为实现 source of truth；保持视觉定义在 UI scope 内，不要无依据扩展成完整平面品牌手册。
4. 涉及 Creator Private Model、Fine-Tuning、model asset、training dataset、LoRA、merged model、Creator ownership 或 Hatch value capture 时，读取 [references/creator-private-model.md](references/creator-private-model.md)；需要英文资料或英文输出时，同时读取 [references/creator-private-model-tuning.md](references/creator-private-model-tuning.md)。将这些文档作为产品和商业设计参考，不把其中的方案自动当作当前已实现能力。
5. 区分不同数据源的职责：
   - 使用飞书获取内部决策、技术架构、运营背景、使用指南和会议历史。
   - 使用 One Pager 获取已批准的对外定位、商业模式表述和合作伙伴沟通语言。
   - 使用 Market Analysis 获取市场进入假设、赛道选择和 GTM 框架。
   - 使用 Founder Context 获取 Keith 的创始人经历、稳定产品判断、质量标准、架构原则和工作方式。
6. 根据任务目的、数据源职责和日期处理冲突。明确指出重要冲突，不要静默合并不同结论。
7. 根据用户要求生成回答或交付物，并链接实际使用的数据源。说明会议纪要和市场结论的证据等级。

## 数据源权威性

- 回答内部产品意图时，优先使用相关飞书正式文档，其次才是会议纪要。
- 编写对外材料时，优先使用当前 One Pager。除非用户明确要求且适合共享，否则不要暴露内部措辞。
- 选择市场或赛道时，把 Market Analysis 视为工作假设，而不是已验证事实。涉及实时、精确或高风险的外部结论时，使用一手来源重新验证。
- 回答 Keith 的创始人判断时，使用 Founder Context，并像处理其他数据源一样根据主题、日期和 `provenance` 判断适用性。
- 判断当前实现、发布、authentication、payment、entitlement 或 Runtime 行为时，检查真实产品链路。内容资料不能作为 UAT 或发布证据。
- 当两个数据源冲突时，分别说明结论、来源和日期，再指出当前任务应以哪个来源为准。

## 处理飞书资料

- 使用数据源说明中的已认证 `lark-cli` 访问飞书。
- 默认只读。除非用户明确要求，否则不要移动、编辑、分享文档或修改权限。
- 优先使用正式产品文档，不要优先依赖 AI 生成的智能纪要。
- 把智能纪要视为可能不准确的材料。重要结论需要用原始文字记录或正式文档确认。
- 不要大范围复制私人、健康、融资、凭据、权限控制或其他敏感信息。
- 如果认证或实时依赖不可用，明确报告阻碍。不要用 mock 数据替代，也不要声称已经检查数据源。

## 常见任务

- 解释 Hatch 的产品定位、技术架构、Creator 流程、Customer 流程或商业模式。
- 准备内部新人培训、产品简报、市场计划、合作伙伴材料或会议资料。
- 对比内部策略与对外表述。
- 从 Keith 的创始人视角解释产品判断、质量标准、架构原则和工作方式。
- 追溯某项 Hatch 决策在何时、何处形成。
- 识别过时、冲突、敏感或尚未验证的项目结论。
