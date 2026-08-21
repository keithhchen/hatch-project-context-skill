# Hatch 数据源

## 数据源选择

| 数据源 | 适合用于 | 不应视为 |
|---|---|---|
| 飞书知识库 | 内部产品定义、技术架构、市场资料、使用指南和历史决策 | 当前实现或发布状态的证据 |
| One Pager | 已批准的对外定位、Creator/Customer 价值、商业模式和合作伙伴沟通 | 内部实现规范 |
| Market Analysis | 赛道评分、北美与日本市场进入假设和 GTM 框架 | 已独立验证的市场事实 |
| Founder Context | Keith 的经历、产品判断、质量标准、架构原则和工作方式 | 当前实现、实时决策或对外定稿 |

## 飞书知识库

- 名称：`Hatch 项目知识库`
- Space ID：`7675607658325445581`
- 可见性：私有团队知识库
- 根节点 token：`FD0Lw7BcbiPIFvkVQ4OcS3EHnwd`
- 租户地址：`https://rcnk9aqjekzv.feishu.cn`

一级目录：

| 目录 | Node token | 内容 |
|---|---|---|
| 产品定义 | `U1EJwdKcWisIxek6jbTcfUOqnWd` | 当前产品定义和最新选定的产品会议 |
| 技术架构 | `DRpgwGjymiaZ6tkV87fcF8Npnih` | Hatch 产品架构 |
| 市场与赛道 | `STi0w16nJixyHRkf33qctt0BnYc` | Hatch Verticals |
| 用户指南 | `ZgaGw1Gh0i6ccykehe6ccccdnQc` | 测试版启动说明 |
| 会议与决策 | `JhNwwG2Uyi6uAKk4F0tcNDkFnRY` | 选定的历史智能纪要 |

使用已认证的 `lark-cli` 读取根目录。默认从 `PATH` 查找；如果命令不在 `PATH`，先设置 `LARK_CLI_BIN` 为实际路径：

```bash
LARK_CLI_BIN="${LARK_CLI_BIN:-lark-cli}"
LARK_CLI_NO_PROXY=1 "$LARK_CLI_BIN" wiki nodes list \
  --params '{"space_id":"7675607658325445581","page_size":50}' \
  --format json
```

读取某个目录时增加 `parent_node_token`：

```bash
LARK_CLI_BIN="${LARK_CLI_BIN:-lark-cli}"
LARK_CLI_NO_PROXY=1 "$LARK_CLI_BIN" wiki nodes list \
  --params '{"space_id":"7675607658325445581","parent_node_token":"CATEGORY_NODE_TOKEN","page_size":50}' \
  --format json
```

使用 Wiki URL 或 token 读取文档：

```bash
LARK_CLI_BIN="${LARK_CLI_BIN:-lark-cli}"
LARK_CLI_NO_PROXY=1 "$LARK_CLI_BIN" docs +fetch \
  --api-version v2 --doc 'WIKI_URL_OR_TOKEN' --format json
```

读取 `data.document.content`。需要记录来源时，保留标题、URL、revision 和日期。不要暴露本地飞书凭据或配置。

## Founder Context

这是与飞书知识库、One Pager 和 Market Analysis 并列的一个数据源，位于 `references/founder-context/`，内部包含 9 个按主题拆分的文件。下面的文件只用于该数据源内部按需读取，不是 9 个独立数据源：

| 主题 | 文件 | 使用范围 |
|---|---|---|
| 创始人经历与 Hatch 来源 | [01-founder-origin-and-why-hatch.md](founder-context/01-founder-origin-and-why-hatch.md) | Founder–Market Fit、产品起源和主动蒸馏信念 |
| 产品命题 | [02-hatch-product-thesis.md](founder-context/02-hatch-product-thesis.md) | 一句话定义、产品流程、用户承诺和非目标 |
| Creator-first 品牌与分发 | [03-creator-first-brand-and-distribution.md](founder-context/03-creator-first-brand-and-distribution.md) | 品牌主次、消费者入口和分发原则 |
| 专家价值 | [04-expert-value-selection-standards-and-difference.md](founder-context/04-expert-value-selection-standards-and-difference.md) | 专家差异、选择标准和 Eval 含义 |
| 产品楔子与验证 | [05-creator-product-wedge-and-validation.md](founder-context/05-creator-product-wedge-and-validation.md) | 课程与咨询之间的产品层、收入验证和渠道价值 |
| 蒸馏与质量系统 | [06-creator-distillation-quality-system.md](founder-context/06-creator-distillation-quality-system.md) | 蒸馏输入、Creator 监督、Eval、回流和发布门槛 |
| Product authority 与版本 | [07-product-authority-and-version-model.md](founder-context/07-product-authority-and-version-model.md) | Product-only authority、Snapshot、事件图和迁移原则 |
| Agent Runtime | [08-agent-runtime-philosophy.md](founder-context/08-agent-runtime-philosophy.md) | 协议、Server/Desktop 边界、Runtime 和方法保护 |
| 工作与决策方式 | [09-founder-working-and-decision-style.md](founder-context/09-founder-working-and-decision-style.md) | 表达、判断、产品决策、工程与验收原则 |

读取 Founder Context 时，根据当前问题选择相关内部文件，并保留其中记录的 `provenance`、来源和日期。

## One Pager

- URL：<https://hatch-onepager.vercel.app/>
- 当前职责：Hatch 对外叙事的公开事实来源。
- 主要部分：产品空白、平台工作流、用户访谈、商业模式、愿景和合作伙伴。
- 编写对外材料时，使用页面当前表述，例如“帮助专业 Creator 把方法转化为能交付可用成果的付费 Agent”。
- 优先通过网页访问能力读取实时页面。如果语义化访问失败，使用只读 HTTP 请求：

```bash
curl -L --max-time 20 -sS 'https://hatch-onepager.vercel.app/'
```

不要因为某项功能出现在网页中，就推断该功能已经部署或正式发布。

## Market Analysis

- URL：<https://hatch-market-entry.keithchen.chatgpt.site/>
- 当前职责：北美和日本市场进入的工作假设。
- 主要部分：筛选模型、北美、日本和 GTM。
- 核心评价维度：已有付费行为、明确 Job、明确 Output、Expert Delta、Labor Compression、Repeatability 和 Evalability。
- 优先通过网页访问能力读取实时页面。如果语义化访问失败，使用：

```bash
curl -L --max-time 20 -sS 'https://hatch-market-entry.keithchen.chatgpt.site/'
```

明确说明评分、排名和市场建议来自这份分析。对外呈现实时数字或高置信度市场事实前，重新检查页面引用的一手来源。

## 冲突处理示例

- 如果飞书记录的是内部实验，而 One Pager 已形成确定的对外定位，对外文案使用 One Pager；只在内部任务中说明尚未解决的不确定性。
- 如果智能纪要声称某项功能已可用，但任务要求判断当前产品行为，检查真实产品链路，并把会议中的说法标记为未验证。
- 如果 Market Analysis 与 Hatch Verticals 对某个赛道的排名不同，保留双方依据，并在提出建议前说明日期和评价标准。
