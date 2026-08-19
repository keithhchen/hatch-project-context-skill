# Hatch data sources

## Source selection

| Source | Use for | Do not treat as |
|---|---|---|
| Feishu knowledge base | Internal product definition, architecture, market notes, guides, historical decisions | Proof of current implementation or release status |
| One Pager | Approved public positioning, creator/customer value, business model, partner messaging | Internal implementation specification |
| Market Analysis | Vertical scoring, North America/Japan entry hypotheses, GTM framing | Independently verified market fact |

## Feishu knowledge base

- Name: `Hatch 项目知识库`
- Space ID: `7675607658325445581`
- Visibility: private team space
- Root node token: `FD0Lw7BcbiPIFvkVQ4OcS3EHnwd`
- Tenant base URL: `https://rcnk9aqjekzv.feishu.cn`

Top-level categories:

| Category | Node token | Contents |
|---|---|---|
| 产品定义 | `U1EJwdKcWisIxek6jbTcfUOqnWd` | Current product definition; latest selected product meeting |
| 技术架构 | `DRpgwGjymiaZ6tkV87fcF8Npnih` | Hatch product architecture |
| 市场与赛道 | `STi0w16nJixyHRkf33qctt0BnYc` | Hatch Verticals |
| 用户指南 | `ZgaGw1Gh0i6ccykehe6ccccdnQc` | Beta launch instructions |
| 会议与决策 | `JhNwwG2Uyi6uAKk4F0tcNDkFnRY` | Selected historical smart minutes |

Use the configured executable:

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli wiki nodes list \
  --params '{"space_id":"7675607658325445581","page_size":50}' \
  --format json
```

List a category by adding `parent_node_token`:

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli wiki nodes list \
  --params '{"space_id":"7675607658325445581","parent_node_token":"CATEGORY_NODE_TOKEN","page_size":50}' \
  --format json
```

Fetch a document from its Wiki URL or token:

```bash
LARK_CLI_NO_PROXY=1 /Users/keithchen/.nvm/versions/node/v22.22.0/bin/lark-cli docs +fetch \
  --api-version v2 --doc 'WIKI_URL_OR_TOKEN' --format json
```

Read `data.document.content`. Retain the title, URL, revision, and date when provenance matters. Do not expose local Lark credentials or configuration.

## One Pager

- URL: <https://hatch-onepager.vercel.app/>
- Current role: public source of truth for Hatch's external narrative.
- Main sections: product gap, platform workflow, user interviews, business model, vision, and partners.
- Use its current wording for public-facing claims such as expert creators turning methods into paid agents that deliver usable work.
- Retrieve the live page with web access. If semantic page access fails, use a read-only HTTP request such as:

```bash
curl -L --max-time 20 -sS 'https://hatch-onepager.vercel.app/'
```

Do not infer that a described feature is deployed or released merely because it appears on the page.

## Market Analysis

- URL: <https://hatch-market-entry.keithchen.chatgpt.site/>
- Current role: working market-entry thesis for North America and Japan.
- Main sections: selection framework, North America, Japan, and GTM.
- Core evaluation dimensions: existing payment behavior, clear job, clear output, expert delta, labor compression, repeatability, and evalability.
- Retrieve the live page with web access. If semantic page access fails, use:

```bash
curl -L --max-time 20 -sS 'https://hatch-market-entry.keithchen.chatgpt.site/'
```

Attribute scores, rankings, and market recommendations to this analysis. Re-check cited primary sources before presenting time-sensitive numbers or high-confidence market facts.

## Conflict examples

- If Feishu describes an internal experiment but the One Pager presents a finalized external position, use the One Pager for public copy and disclose the internal uncertainty only for internal work.
- If a smart minute claims a feature works but the task concerns present product behavior, inspect the real product path and mark the meeting claim unverified.
- If Market Analysis and Hatch Verticals rank a segment differently, preserve both rationales and identify their dates and evaluation criteria before recommending a choice.
