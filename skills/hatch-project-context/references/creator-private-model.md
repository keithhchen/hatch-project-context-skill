# Hatch：在 Agent Corpus 基础上增加 Creator Private Model 能力

---

## 1. 当前产品架构

Hatch 当前交付的 Agent 由以下部分组成：

The Agent currently delivered by Hatch consists of the following layers:

| Layer | 作用|
|---|---|
| System Prompt / Instructions | 全局行为、优先级、边界、长期生效规则|
| Skills | 可复用的方法、流程与局部能力|
| External Tools | 搜索、文件、API、MCP 等执行能力|
| Knowledge | 专家材料、案例和长尾知识|

Runtime 在每个任务中加载对应 Agent Corpus，并负责模型调用、工具执行、上下文、对话状态和交付。

The Runtime loads the corresponding Agent Corpus for each task and is responsible for model calls, tool execution, context, conversation state, and delivery.

Creator Factory 当前负责把专家材料和 Creator judgment 编译为 Agent Corpus。当前实现明确属于 **prompt-and-corpus compilation**，不包含 Fine-Tuning 或模型权重更新。

The Creator Factory currently compiles expert materials and Creator judgment into an Agent Corpus. The current implementation is explicitly **prompt-and-corpus compilation** and does not include Fine-Tuning or model-weight updates.

Factory 已包含：

The Factory already includes:

- Evidence extraction
- Creator questions / reference answers
- Candidate Corpus compilation
- Development evaluation
- Regression evaluation
- Sealed held-out evaluation
- Correction / revision
- Immutable release


---

## 2. 新增能力：Fine-Tuning Layer

未来 Hatch 在现有 Context / Harness Engineering 基础上增加：

In the future, Hatch adds the following capability on top of its existing Context / Harness Engineering stack:

**Creator-specific Fine-Tuning**

整体结构变为：

The overall architecture becomes:

```text
Context / Harness Engineering

System Prompt
Skills
Tools
Knowledge
Runtime
Eval
Release

        +

Model Adaptation

Creator-specific LoRA
Creator-specific Merged Model
```

Fine-Tuning 不替代 System、Skills、Tools 或 Knowledge。

Fine-Tuning does not replace System, Skills, Tools, or Knowledge.

它增加的是一个新的模型参数层。

It adds a new model-parameter layer.

---

## 3. 什么进入 Context，什么进入 Weights

不同类型的信息适合不同承载方式。

Different types of information are better suited to different layers.

| 信息类型| 主要承载位置|
|---|---|
| 最新知识、事实、案例| Knowledge / RAG |
| 明确方法和工作流程| Skills |
| 产品边界、全局要求| System Prompt |
| 外部执行能力| Tools / Runtime |
| 稳定的行为模式| Fine-Tuning |
| 稳定的 judgment| Fine-Tuning |
| 稳定的 tool-use policy | Fine-Tuning / Trajectory Training |

因此 Fine-Tuning 的主要目标不是把 Creator 的全部知识塞入模型，而是参数化已经重复观察到的：

The primary purpose of Fine-Tuning is therefore not to place all Creator knowledge inside model weights. It is to parameterize repeatedly observed:

- judgment
- behavior
- preference / taste
- decision boundary
- tool policy
- agent policy

对应三类主要训练数据：

Three primary categories of training data correspond to these objectives:

| 数据| 学习目标| 典型训练方式|
|---|---|---|
| Behavior / Output | 应该怎么回答| SFT |
| Judgment / Preference | 什么答案更好| DPO |
| Agent Trajectory | 应该怎么行动| Trajectory SFT / RL |


---

# 4. 数据来源

训练数据主要来自 Creator 对真实消费者任务的校准。

Training data primarily comes from Creator calibration of real consumer tasks.

基本数据链路：

The basic data flow is:

```text
Consumer Task
↓
Creator Agent Execution
↓
Creator Review / Correction / Comparison
↓
Structured Expert Signal
↓
Dataset
↓
Fine-Tuning
↓
Candidate Model
↓
Blind Evaluation
```

Hatch 当前 Factory 已经存在部分必要的数据结构：

The current Hatch Factory already contains part of the required data structure:

```text
Question
Creator Reference
Candidate Output
Eval Verdict
Correction
Regression Case
Held-out Case
```


未来可以进一步增加：

Future extensions can include:

- post-edit
- chosen / rejected pair
- rejection reason
- counterfactual
- decision flip
- trajectory
- real task outcome

消费者数据进入训练体系需要单独的数据授权与用途约束。当前 Hatch V1 默认不允许 Buyer private data 自动进入 Creator learning dataset。

Consumer data entering the training system requires separate authorization and purpose constraints. Under the current Hatch V1 boundary, Buyer private data does not automatically enter the Creator learning dataset.

---

## 4.1 Behavior / Output Data 示例

这一类数据回答：

This category of data answers:

> **面对这个任务，专家认为应该如何回答？**
> **Given this task, how should the expert respond?**

例如：

Example:

```text

我们做一个帮助专家创建 AI Agent 的平台。
开发两个月，还没有付费用户。
现在应该继续开发还是融资？

```

Expert / preferred output:

```text
现在优先级不是融资，也不是继续扩大产品，
而是获得真实交易信号。

未来两周选择一个窄 vertical，
尝试卖出 3 个付费 pilot，
并验证用户究竟为什么结果愿意付钱。


```

这种数据可以用于 **SFT**。

This type of data can be used for **SFT**.

模型主要学习：

The model primarily learns:

```text
Input
↓
What to focus on
↓
What to output
↓
How to structure the answer
↓
How to express it
```

即：

In other words:

> **Behavior / Output Data 教模型“应该怎么回答”。**
> **Behavior / Output Data teaches the model how it should respond.**


---

## 4.2 Judgment / Preference Data 示例

这一类数据不只是告诉模型“正确答案是什么”，而是表达：

This category does not merely tell the model what the correct answer is. It expresses:

> **两个合理答案之间，为什么专家认为一个比另一个更好？**
> **Between two plausible answers, why does the expert prefer one over the other?**

例如：

Example:

```text

公司没有付费用户，现在应该融资还是继续开发？

```

Chosen:

```text
先验证真实付费需求。
只有当需求已经成立、增长受到资本约束时，
融资才成为主要问题。


Fundraising becomes the primary issue only after demand has been established
```

Rejected:

```text
AI 市场正在快速增长，竞争越来越激烈，
因此应该尽快融资扩大团队并抢占窗口。


```

Reason:

```text
Rejected answer 把市场增长和竞争当成融资理由，
却没有解决当前最大的未知变量——
是否存在真实付费需求。


The rejected answer treats market growth and competition
```

这里真正被表达的数据不是一个表面答案，而是一组 judgment relationships：

The actual signal is not merely the surface answer, but a set of judgment relationships:

```text
Market growth
≠
Product-market validation

Competition increases
≠
Fundraising is automatically correct

Largest unresolved uncertainty
>
Macro narrative
```

这种数据可以形成：

This can produce:

```text
Prompt
+
Chosen
+
Rejected
+
Preference / Reason
```

并用于 DPO 或其他 preference-learning 方法。

It can then be used for DPO or other preference-learning methods.

> **Judgment / Preference Data 教模型“什么答案更好，以及 decision boundary 在哪里”。**
> **Judgment / Preference Data teaches the model which answer is better and where the decision boundary lies.**


---

## 4.3 Agent Trajectory Data 示例

对于需要实际执行任务的 Agent，最终答案本身不足以描述专家能力。

For Agents that must execute real tasks, the final answer alone is not sufficient to describe expert capability.

需要记录：

The relevant signal may include:

```text
Task
↓
Choose Next Action
↓
Call Tool
↓
Observe Result
↓
Update Judgment
↓
Call Next Tool
↓
...
↓
Final Answer
```

例如：

Example:

```text

判断 Acme AI 是否值得作为直接竞争对手重点研究。

Determine whether Acme AI should be treated
```

Trajectory:

```text
1.

首先确认产品和真实客户情况。


2.

公司描述自己为 AI expert marketplace...


3.

仅有 marketing 信息不足，
需要寻找客户、融资和 traction。


4.

融资 400 万美元，并有两个公开客户案例。


5.

继续判断产品 primitive 是否真正重叠。

Continue by determining whether


6.

产品主要进行专家知识问答，
没有任务执行和交付 workflow。


7.

值得持续跟踪，但目前不是直接竞争对手。

```

这里训练的不是最后一句话，而是整个 **Agent Policy**：

The training target is not just the final sentence, but the broader **Agent Policy**:

- 什么时候搜索
- 搜索什么
- 什么 evidence 仍然缺失
- observation 后如何更新判断
- 是否继续调查
- 什么时候停止
- 如何形成最终结论

这类数据可以用于 Trajectory SFT；如果未来存在可靠、可计算的 reward，也可以进一步支持 RL。

This type of data can be used for Trajectory SFT; where reliable and computable rewards exist, it can also support later RL.

> **Trajectory Data 教模型“为了得到答案，应该怎么行动”。**
> **Trajectory Data teaches the model how it should act in order to reach an answer.**


---

## 4.4 一个完整 Expert Dataset Unit

高价值训练数据不一定是一条独立的 Question → Answer。

A high-value training unit does not necessarily consist of a single Question → Answer pair.

例如，一个创业导师的数据单元可以是：

For example, one dataset unit for a startup advisor could contain:

### 原始案例

```text
B2B SaaS


95%

Seed

应该扩大销售还是继续产品开发？

```

### 专家答案

```text
优先扩大销售。

```

### 专家理由

```text
Retention 已经足够证明产品价值，
当前最大的 constraint 是 distribution。


```

### 被拒绝的替代方案

```text
继续开发更多功能以强化产品壁垒。

Continue developing more features
```

### 被拒绝的理由

```text
目前不存在产品不足的 evidence，
继续开发不能解决最大的瓶颈。


```

### 反事实

只改变一个关键变量：

Change one critical variable:

```text

95%
↓
40%
```

新的 Expert Answer：

New Expert Answer:

```text
停止扩大销售，
先解决 retention。


```

这组数据比一个单独答案提供更多信息，因为它明确表达：

This data unit contains substantially more information than a single answer because it expresses:

```text
When distribution is the constraint
When product / retention is the constraint
```

也就是：

In other words:

> **什么变量真正改变专家的 decision。**
> **Which variable actually changes the expert’s decision.**

因此，一个高价值 Expert Dataset 的单位可以是：

A high-value Expert Dataset unit can therefore contain:

```text
Original Case
+
Expert Answer
+
Reason
+
Rejected Alternative
+
Rejected Reason
+
Counterfactual
+
Decision Flip
+
Edge Cases
```


---

# 5. Creator 体验

Fine-Tuning 不要求 Creator 在创建 Agent 时提前准备训练数据。

Fine-Tuning does not require the Creator to prepare a training dataset when creating an Agent.

产品路径可以是：

The product path can be:

```text
Create Agent
↓
Launch with System + Skills + Tools + Knowledge
↓
Real Consumers Begin Using It
↓
Creator Continuously Calibrates
↓
Accumulate Sufficient High-Quality Data
↓
Hatch Assesses Training Readiness
↓
Train Creator-Specific Model
↓
Blind-Evaluate Against Existing Agent Baseline
↓
Deploy When Evaluation Criteria Are Met
```

因此 Creator 可以先使用现有 Agent Corpus 能力，再随着真实使用逐步获得模型微调能力。

The Creator can therefore begin with the existing Agent Corpus capabilities and gradually gain model Fine-Tuning capabilities as real usage accumulates.

Fine-Tuning 是后续能力，不是 Agent 创建的前置条件。

Fine-Tuning is a later-stage capability, not a prerequisite for Agent creation.

---

# 6. Private Model Asset

训练结果可以是：

The training output can be:

### Creator-Specific LoRA Adapter

```text
Shared Base Model

+
Creator A LoRA
Creator B LoRA
Creator C LoRA
```

或者：

or:

### Creator-Specific Merged Model

```text
Base Model
+
Creator Adapter
↓
Merged Creator Model
```

LoRA 与具体 Base Checkpoint 绑定，但 Adapter 可以独立保存、版本化和导出。

A LoRA is tied to a specific Base Checkpoint, but the Adapter itself can be independently stored, versioned, and exported.

Creator 可以拥有并导出自己的 Adapter

The Creator can own and export their own Adapter / Model Weights.

Hatch 不主张对 Creator Data 和模型资产拥有 ownership。

Hatch does not claim ownership over Creator Data or model assets.

---

# 7. Creator 的新资产类别

在现有 Agent Corpus 基础上增加 Fine-Tuning 后，Creator 会新增一类独立的技术资产：

Adding Fine-Tuning on top of the existing Agent Corpus creates a new category of independent technical assets for the Creator:

> **Creator-Specific Model Assets**

当前 Creator 在 Hatch 中主要拥有显式资产：

Today, the Creator primarily owns explicit assets:

| Asset | 形式|
|---|---|
| Source Materials | 课程、文章、案例、方法材料|
| System Instructions | 全局行为与边界|
| Skills | 可复用的方法和流程|
| Knowledge | 专业知识、案例与长尾材料|
| Product Configuration | Tools、Runtime、产品配置|

Fine-Tuning 增加：

Fine-Tuning adds:

| New Asset | 形式|
|---|---|
| Training Dataset | Creator 对真实消费者任务进行校准后形成的数据集|
| LoRA Adapter | 基于特定 Base Model 的 Creator-specific 参数增量|
| Merged Model | Base Model 与 Creator Adapter 合并后的独立模型|
| Model Versions | 不同训练数据、Base Model 和训练方法产生的模型版本|
| Evaluation Record | 每个模型版本在 Blind / Regression Eval 上的表现记录 / Performance record of each model version on Blind|

Creator 的 AI 资产因此从：

The Creator’s AI assets therefore expand from:

```text
Content
+
Prompt
+
Skills
+
Knowledge
```

扩展为：

to:

```text
Content
+
Agent Corpus
+
Training Dataset
+
Private Model Weights
```

这里的 Model Asset 不替代 Agent Corpus。

The Model Asset does not replace the Agent Corpus.

System、Skills、Knowledge 和 Tools 仍然承担动态知识、明确规则、运行时能力和可编辑配置；Fine-Tuning 进一步把适合参数化的 judgment、behavior 和 tool policy 写入模型参数。

System, Skills, Knowledge, and Tools continue to carry dynamic knowledge, explicit rules, runtime capabilities, and editable configuration. Fine-Tuning further parameterizes suitable judgment, behavior, and tool policy into model parameters.

---

## 7.1 更 Tangible 的技术资产

与 Prompt 或软件配置相比，Creator-specific Model Asset 具备几个明确的技术属性：

Compared with a Prompt or software configuration, a Creator-specific Model Asset has several concrete technical properties:

- 有独立的 Model 或 Adapter 文件；
  it exists as an independent Model or Adapter file;

- 有明确的 Base Model dependency；
  it has an explicit Base Model dependency;

- 可以通过 digest / version 标识；
  it can be identified through a digest / version;

- 可以独立部署；
  it can be independently deployed;

- 可以导出到其他兼容 inference infrastructure；
  it can be exported to other compatible inference infrastructure;

- 可以和其他模型版本进行定量 Eval；
  it can be quantitatively evaluated against other model versions;

- 可以持续通过新数据产生新版本。
  new versions can be produced as additional data becomes available.

因此它不仅是 Hatch 平台内部的一组配置，而是一项 Creator 可以实际持有和迁移的技术/IP 资产。

It is therefore not merely a set of configurations inside Hatch, but a technical/IP asset that the Creator can actually possess and migrate.

这里不主张其具有特定的会计或财务资产属性。“Asset”在这里指的是其作为：

This does not claim any particular accounting or financial-asset classification. “Asset” here refers to its nature as:

> **可保存、可版本化、可部署、可迁移的软件与模型资产。**
> **a storable, versionable, deployable, and portable software and model asset.**

---

## 7.2 更高的复制成本

System Prompt、Skills 和 Knowledge 都属于显式资产。

System Prompt, Skills, and Knowledge are explicit assets.

获得相同内容后，另一方理论上可以重新实现相似的 Context

Once the same content is obtained, another party can theoretically recreate similar Context / Harness Engineering.

Creator-specific Model 的产生则依赖另一组历史数据：

A Creator-specific Model depends on another layer of historical data:

```text
Real Consumer Tasks
+
Agent Output
+
Creator Calibration
+
Corrections / Preferences
+
Decision Boundaries
+
Training
+
Evaluation
```

因此，即使第三方获得相同课程、Prompt 或 Knowledge，也不会自动获得：

Therefore, even if a third party obtains the same courses, Prompt, or Knowledge, it does not automatically obtain:

- 历史消费者任务
- Creator Calibration / Creator calibration;
- Preference / Correction 数据
- Decision Boundary 数据
- 最终训练得到的 Adapter Weights

其复制成本不主要来自模型文件本身不可读取，而来自：

The higher replication cost does not primarily come from the model file being unreadable. It comes from:

> **需要重新生产形成这些模型参数所依赖的专家校准历史。**
> **The need to reproduce the history of expert calibration from which those model parameters were created.**

---

## 7.3 Creator 所有权

Hatch 不取得 Creator Data 的 ownership。

Hatch does not take ownership of Creator Data.

Creator-specific Training Data、LoRA Adapter 和最终模型可以按照产品和合同约定归 Creator 所有，并允许 Creator 导出其 Adapter

Creator-specific Training Data, LoRA Adapters, and final models can belong to the Creator under the applicable product and contractual terms, and the Creator can export their Adapter / Model Asset.

Hatch 的产品原则因此可以表述为：

Hatch’s product principle can therefore be stated as:

> **Creator owns the intelligence; Hatch provides the infrastructure used to produce it.**

对于使用真实消费者 interaction 形成训练数据的场景，需要另外取得适当的数据授权与用途许可。

Where real consumer interactions are used to produce training data, appropriate data authorization and purpose permissions must be obtained separately.

---

# 8. Hatch 的价值捕获

Hatch 的商业价值不依赖于拥有 Creator Data，也不依赖于禁止 Creator 导出模型。

Hatch’s commercial value does not depend on owning Creator Data or preventing Creators from exporting their models.

Hatch 提供的是一套持续生产、训练、验证和运行 Creator-specific AI Assets 的基础设施。

Hatch provides the infrastructure for continuously producing, training, validating, and operating Creator-specific AI Assets.

完整链路包括：

The complete lifecycle includes:

```text
Consumer Task
```

其中真正具有持续价值的部分，不只是 Fine-Tuning 计算本身。

The persistent value in this system is not limited to Fine-Tuning compute itself.

当前开源生态已经显著降低 SFT、DPO、LoRA / QLoRA 等训练方式的工程门槛和 GPU 成本。

The current open-source ecosystem has significantly reduced the engineering barrier and GPU cost of SFT, DPO, LoRA / QLoRA, and related methods.

对于数百条数据的实验，真正主要的投入往往是：

For experiments involving hundreds of examples, the primary inputs are often:

- Expert Time
- Data Construction
- Preference Annotation
- Counterfactual Construction
- Edge Cases
- Blind Evaluation

而不是单次 GPU Run。

rather than a single GPU Run.

Hatch 的 Value Capture 主要集中在三个商业层。

Hatch’s Value Capture is concentrated across three commercial layers.

---

## 8.1 Creator 平台

Creator 首先使用 Hatch 完成：

Creators first use Hatch for:

- Agent Corpus Construction
- System / Skills / Knowledge Management
- Runtime
- Eval
- Regression
- Release
- Version Management
- Creator Calibration Workflow

这些能力在 Creator 尚未达到 Fine-Tuning readiness 时已经独立产生价值。

These capabilities provide standalone value before the Creator reaches Fine-Tuning readiness.

对应的商业模式可以是持续的软件与基础设施收入，例如：

The corresponding business model can include recurring software and infrastructure revenue such as:

- Creator Subscription
- Workspace Fee
- Product-Level SaaS Fee

---

## 8.2 模型开发

当 Creator 积累足够数据以后，Hatch 可以进一步提供：

Once the Creator has accumulated sufficient data, Hatch can additionally provide:

- Training Readiness Assessment
- Dataset Construction
- Train / Validation / Blind Test Split
- Base Model Selection
- SFT
- DPO
- Trajectory Training
- Candidate Evaluation
- Prompt / Corpus / Fine-Tuned Baseline Comparison
- Adapter / Model Versioning
- Export

这里出售的不是单纯的 GPU 时间。

What is being sold here is not simply GPU time.

GPU Training 本身正在商品化；Hatch 提供的是：

GPU Training itself is becoming commoditized. Hatch provides:

> **从真实专家 Calibration 到一个经过验证的 Private Model Asset 的完整生产过程。**
> **The complete production process from real expert calibration to a validated Private Model Asset.**

这一层可以形成更高价值的 Premium Model Development Service

This layer can support higher-value Premium Model Development Service / Infrastructure Revenue.

---

## 8.3 托管模型基础设施

即使 Creator 拥有并可以导出自己的 Weights，也仍然需要长期运行模型所需的基础设施，包括：

Even when the Creator owns and can export their Weights, they still require infrastructure to operate the model over time, including:

- Compatible Base Model Management
- LoRA Loading
- Multi-LoRA Serving
- Inference Deployment
- Autoscaling
- GPU Utilization Management
- Model Version Routing
- Observability
- Rollback
- Security
- Regression Testing
- Retraining

因此：

Therefore:

```text
Creator Owns the Model
≠
Creator Must Operate the Model Infrastructure
```

Hatch 可以允许 Asset Portability，同时提供默认的 Managed Deployment Environment。

Hatch can support Asset Portability while providing the default Managed Deployment Environment.

商业上可以形成持续的：

Commercially, this can generate recurring:

- Inference Revenue
- Hosting Fees
- Model Management Fees
- Usage-Based Infrastructure Revenue

这使 Hatch 不需要通过 Data 或 Model Lock-In 获得持续收入。

This means Hatch does not need to rely on Data or Model Lock-In to create recurring revenue.

Creator 可以带走资产；Hatch Capture Value 的基础是持续提供更方便、更完整的模型生产和运行基础设施。

The Creator can take the asset elsewhere; Hatch captures value by continuing to provide a more convenient and complete infrastructure for model production and operation.

---

## 8.4 Hatch 的核心商业资产

Hatch 自身不需要拥有所有 Creator 的训练数据。

Hatch does not need to own all Creator training data.

Hatch 长期积累的是一套：

What Hatch accumulates over time is an:

> **Expert Data and Model Production Infrastructure**

具体包括：

Specifically:

```text
Agent Creation
+
Real-World Execution
+
Expert Calibration
+
Data Construction
+
Training
+
Evaluation
+
Deployment
```

其核心能力是：

Its core capability is:

> **以较低的专家时间成本，把真实专业服务中产生的 Judgment 转化为可训练数据，并进一步转化为经过验证、可部署的 Creator-Specific Model Assets。**

> **To convert judgment generated through real professional services into trainable data with relatively low expert-time overhead, and then turn that data into validated, deployable Creator-Specific Model Assets.**

Hatch 的 Value Capture 来自持续提供这套基础设施，而不是取得 Creator Intelligence 的所有权。

Hatch captures value by continuously providing this infrastructure, rather than by taking ownership of Creator Intelligence.

---

# 9. 为什么比单纯 Prompt / Corpus 更难复制

Prompt、Skill 和 Knowledge 都属于显式软件资产。

Prompt, Skill, and Knowledge are explicit software assets.

它们可以被：

They can be:

- 阅读
- 导出
- 重写
- 重新组合
- 在另一套 Agent Framework 中实现

Creator-specific Model Weights 来自另一类生产过程：

Creator-specific Model Weights are produced through a different process:

```text
Real Distribution
+
Agent Mistakes
+
Creator Calibration
+
Preference
+
Counterfactual
+
Repeated Evaluation
```

竞争者即使能够复制 Agent 软件结构，也不能直接复制已经发生的专家校准历史和由其训练产生的参数。

Even if a competitor can replicate the Agent software architecture, it cannot directly replicate the expert-calibration history that has already occurred or the parameters trained from that history.

加入 Fine-Tuning 后，Hatch 可以同时产生两类资产：

With Fine-Tuning added, Hatch can therefore produce two categories of assets:

| 类型| 形式|
|---|---|
| Explicit Agent Assets | System / Skills / Knowledge / Tools |
| Parameterized Model Assets | LoRA / Model Weights |

两者共同建立在同一套 Hatch Factory、Runtime、Eval 和 Release Infrastructure 上。

Both are built on top of the same Hatch Factory, Runtime, Eval, and Release Infrastructure.

---

# 10. Fine-Tuning 的采用标准

Fine-Tuning 不默认优于 Context Engineering。

Fine-Tuning is not assumed to be superior to Context Engineering by default.

每次训练都应该至少与以下方案比较：

Each training effort should be compared against at least:

```text
Base Model
Best System Prompt
Few-Shot
Agent Corpus
Fine-Tuned Model
```

并使用真正 Held-Out Cases 进行评估。

Evaluation should use genuinely Held-Out Cases.

只有当 Fine-Tuning 在至少一个实际维度产生增益时才部署，例如：

Fine-Tuning should only be deployed when it produces an actual improvement in at least one relevant dimension, such as:

- Expert-Aligned Quality
- Consistency
- Decision-Boundary Accuracy
- Tool-Use Behavior
- Generalization
- Deployment Characteristics

这意味着 Hatch 增加的是一项新的：

This means Hatch is adding a new:

> **Model Adaptation Capability**

而不是用 Fine-Tuning 取代现有 Context

rather than replacing the existing Context / Harness Engineering stack with Fine-Tuning.

---

# 11. 一句话架构定义

### 当前

```text
Creator Agent
=
System Prompt
+
Skills
+
Tools
+
Knowledge
+
Hatch Runtime / Eval / Release
```

### 使用 Fine-Tuning

```text
Creator Agent
=
Existing Context / Harness Engineering
+
Optional Creator-Specific Model Adaptation
```

核心变化只有一个：

The core change is straightforward:

> **在已经存在的 Agent Corpus 和 Harness 基础上，增加把部分专家 Judgment、Behavior 和 Agent Policy 参数化进模型权重的能力。**

> **On top of the existing Agent Corpus and Harness, Hatch adds the capability to parameterize selected expert Judgment, Behavior, and Agent Policy into model weights.**
