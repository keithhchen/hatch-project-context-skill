# Hatch 数据源

## 数据源选择

| 数据源 | 适合用于 | 不应视为 |
|---|---|---|
| 飞书知识库 | 内部产品定义、技术架构、市场资料、使用指南和历史决策 | 当前实现或发布状态的证据 |
| One Pager | 已批准的对外定位、Creator/Customer 价值、商业模式和合作伙伴沟通 | 内部实现规范 |
| Market Analysis | 赛道评分、北美与日本市场进入假设和 GTM 框架 | 已独立验证的市场事实 |

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

使用已配置的可执行文件读取根目录：

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli wiki nodes list \
  --params '{"space_id":"7675607658325445581","page_size":50}' \
  --format json
```

读取某个目录时增加 `parent_node_token`：

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli wiki nodes list \
  --params '{"space_id":"7675607658325445581","parent_node_token":"CATEGORY_NODE_TOKEN","page_size":50}' \
  --format json
```

使用 Wiki URL 或 token 读取文档：

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli docs +fetch \
  --api-version v2 --doc 'WIKI_URL_OR_TOKEN' --format json
```

读取 `data.document.content`。需要记录来源时，保留标题、URL、revision 和日期。不要暴露本地飞书凭据或配置。

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
