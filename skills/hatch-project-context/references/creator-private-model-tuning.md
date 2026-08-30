# Hatch: Adding Creator Private Model Capabilities on Top of the Agent Corpus

---

## 1. Current Product Architecture


The Agent currently delivered by Hatch consists of the following layers:

| Layer |Role |
|---|---|
| System Prompt / Instructions |Global behavior, priorities, boundaries, and persistent rules |
| Skills |Reusable methods, workflows, and local capabilities |
| External Tools |Execution capabilities such as search, files, APIs, and MCP |
| Knowledge |Expert materials, cases, and long-tail knowledge |


The Runtime loads the corresponding Agent Corpus for each task and is responsible for model calls, tool execution, context, conversation state, and delivery.


The Creator Factory currently compiles expert materials and Creator judgment into an Agent Corpus. The current implementation is explicitly **prompt-and-corpus compilation** and does not include Fine-Tuning or model-weight updates.


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

## 2. New Capability: Fine-Tuning Layer


In the future, Hatch adds the following capability on top of its existing Context / Harness Engineering stack:

**Creator-specific Fine-Tuning**


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
or
Creator-specific Merged Model
```


Fine-Tuning does not replace System, Skills, Tools, or Knowledge.


It adds a new model-parameter layer.

---

## 3. What Goes Into Context vs. Weights


Different types of information are better suited to different layers.

|Information Type |Primary Layer |
|---|---|
|Current knowledge, facts, cases | Knowledge / RAG |
|Explicit methods and workflows | Skills |
|Product boundaries and global requirements | System Prompt |
|External execution capabilities | Tools / Runtime |
|Stable behavioral patterns | Fine-Tuning |
|taste | Fine-Tuning |
| 稳定的 tool-use policy | Fine-Tuning / Trajectory Training |


The primary purpose of Fine-Tuning is therefore not to place all Creator knowledge inside model weights. It is to parameterize repeatedly observed:

- judgment
- behavior
- preference / taste
- decision boundary
- tool policy
- agent policy


Three primary categories of training data correspond to these objectives:

|Data |Learning Objective |Typical Training Method |
|---|---|---|
| Behavior / Output |How to respond | SFT |
| Judgment / Preference |Which answer is better | DPO |
| Agent Trajectory |How to act | Trajectory SFT / RL |


---

# 4. Data Sources


Training data primarily comes from Creator calibration of real consumer tasks.


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


Future extensions can include:

- post-edit
- chosen / rejected pair
- rejection reason
- counterfactual
- decision flip
- trajectory
- real task outcome


Consumer data entering the training system requires separate authorization and purpose constraints. Under the current Hatch V1 boundary, Buyer private data does not automatically enter the Creator learning dataset.

---

## 4.1 Behavior / Output Data Example


This category of data answers:

> **Given this task, how should the expert respond?**


Example:

```text
User:

我们做一个帮助专家创建 AI Agent 的平台。

We are building a platform that helps experts create AI Agents.
We have been developing for two months and still have no paying users.
Should we continue building or start fundraising?
```

Expert / preferred output:

```text

未来两周选择一个窄 vertical，
尝试卖出 3 个付费 pilot，


The priority right now is neither fundraising nor expanding the product.

Over the next two weeks, select one narrow vertical,
try to sell three paid pilots,
and determine what outcome customers are actually willing to pay for.
```


This type of data can be used for **SFT**.


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


In other words:

> **Behavior / Output Data teaches the model how it should respond.**


---

## 4.2 Judgment / Preference Data Example


This category does not merely tell the model what the correct answer is. It expresses:

> **Between two plausible answers, why does the expert prefer one over the other?**


Example:

```text
Prompt:


The company has no paying users.
Should it raise money or continue building?
```

Chosen:

```text


Validate real paying demand first.

Fundraising becomes the primary issue only after demand has been established
and growth is constrained by capital.
```

Rejected:

```text
AI 市场正在快速增长，竞争越来越激烈，


The AI market is growing rapidly and competition is intensifying,
so the company should raise money quickly,
expand the team, and capture the market window.
```

Reason:

```text
Rejected answer 把市场增长和竞争当成融资理由，


The rejected answer treats market growth and competition
as reasons to fundraise,
while failing to address the largest current unknown:
whether real paying demand exists.
```


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


It can then be used for DPO or other preference-learning methods.

> **Judgment / Preference Data teaches the model which answer is better and where the decision boundary lies.**


---

## 4.3 Agent Trajectory Data Example


For Agents that must execute real tasks, the final answer alone is not sufficient to describe expert capability.


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


Example:

```text
Task:

判断 Acme AI 是否值得作为直接竞争对手重点研究。

Determine whether Acme AI should be treated
as a direct competitor worth intensive research.
```

Trajectory:

```text
1.

Assistant:

First confirm the product and actual customer situation.

Tool:
web_search


2.

Observation:
公司描述自己为 AI expert marketplace...

The company describes itself as an AI expert marketplace...


3.

Assistant:
仅有 marketing 信息不足，
需要寻找客户、融资和 traction。

Marketing information alone is insufficient.
Look for customers, funding, and traction.

Tool:
web_search


4.

Observation:

The company has raised $4 million
and has two public customer cases.


5.

Assistant:
继续判断产品 primitive 是否真正重叠。

Continue by determining whether
the underlying product primitives actually overlap.

Tool:
open_page


6.

Observation:
没有任务执行和交付 workflow。

The product primarily provides expert Q&A
and does not include task execution or delivery workflows.


7.

Final:

Worth monitoring,
but not currently a direct competitor.
```


The training target is not just the final sentence, but the broader **Agent Policy**:

when to search
what to search for
what evidence is still missing
how to update judgment after an observation
whether to continue investigating
when to stop
how to form the final conclusion


This type of data can be used for Trajectory SFT; where reliable and computable rewards exist, it can also support later RL.

> **Trajectory Data teaches the model how it should act in order to reach an answer.**


---

## 4.4 A Complete Expert Dataset Unit


A high-value training unit does not necessarily consist of a single Question → Answer pair.


For example, one dataset unit for a startup advisor could contain:

### Original Case

```text
Company:
B2B SaaS

ARR:
$500k

Growth:
20% MoM

Retention:
95%

Funding:
Seed

Question:

Should the company expand sales or continue product development?
```

### Expert Answer

```text

Prioritize expanding sales.
```

### Expert Reason

```text
Retention 已经足够证明产品价值，
当前最大的 constraint 是 distribution。


Retention is already strong enough to validate product value.
The largest current constraint is distribution.
```

### Rejected Alternative

```text

Continue developing more features
to strengthen the product moat.
```

### Rejected Reason

```text
目前不存在产品不足的 evidence，


There is currently no evidence that product capability is the main problem.
Additional development does not address the largest bottleneck.
```

### Counterfactual


Change one critical variable:

```text
Retention:

95%
↓
40%
```


New Expert Answer:

```text
先解决 retention。


Stop expanding sales.
Solve retention first.
```


This data unit contains substantially more information than a single answer because it expresses:

```text
When distribution is the constraint
vs.
When product / retention is the constraint
```


In other words:

> **Which variable actually changes the expert’s decision.**


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

# 5. Creator Experience


Fine-Tuning does not require the Creator to prepare a training dataset when creating an Agent.


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


The Creator can therefore begin with the existing Agent Corpus capabilities and gradually gain model Fine-Tuning capabilities as real usage accumulates.


Fine-Tuning is a later-stage capability, not a prerequisite for Agent creation.

---

# 6. Private Model Asset


The training output can be:

### Creator-Specific LoRA Adapter

```text
Shared Base Model

+
Creator A LoRA
Creator B LoRA
Creator C LoRA
```


or:

### Creator-Specific Merged Model

```text
Base Model
+
Creator Adapter
↓
Merged Creator Model
```


A LoRA is tied to a specific Base Checkpoint, but the Adapter itself can be independently stored, versioned, and exported.

Model Weights。

The Creator can own and export their own Adapter / Model Weights.


Hatch does not claim ownership over Creator Data or model assets.

---

# 7. New Asset Class for Creators


Adding Fine-Tuning on top of the existing Agent Corpus creates a new category of independent technical assets for the Creator:

> **Creator-Specific Model Assets**


Today, the Creator primarily owns explicit assets:

| Asset |Form |
|---|---|
| Source Materials |Courses, articles, cases, and methodology materials |
| System Instructions |Global behavior and boundaries |
| Skills |Reusable methods and workflows |
| Knowledge |Domain knowledge, cases, and long-tail materials |
| Product Configuration |Tools, Runtime, and product configuration |


Fine-Tuning adds:

| New Asset |Form |
|---|---|
| Training Dataset |Dataset produced through Creator calibration of real consumer tasks |
| LoRA Adapter |Creator-specific parameter delta based on a particular Base Model |
| Merged Model |Independent model created by merging the Base Model and Creator Adapter |
| Model Versions |Versions produced from different datasets, Base Models, and training methods |
| Evaluation Record |Regression Eval |


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


The Model Asset does not replace the Agent Corpus.


System, Skills, Knowledge, and Tools continue to carry dynamic knowledge, explicit rules, runtime capabilities, and editable configuration. Fine-Tuning further parameterizes suitable judgment, behavior, and tool policy into model parameters.

---

## 7.1 A More Tangible Technical Asset


Compared with a Prompt or software configuration, a Creator-specific Model Asset has several concrete technical properties:

  it exists as an independent Model or Adapter file;

  it has an explicit Base Model dependency;

  it can be identified through a digest / version;

  it can be independently deployed;

  it can be exported to other compatible inference infrastructure;

  it can be quantitatively evaluated against other model versions;

  new versions can be produced as additional data becomes available.


It is therefore not merely a set of configurations inside Hatch, but a technical/IP asset that the Creator can actually possess and migrate.


This does not claim any particular accounting or financial-asset classification. “Asset” here refers to its nature as:

> **a storable, versionable, deployable, and portable software and model asset.**

---

## 7.2 Higher Replication Cost


System Prompt, Skills, and Knowledge are explicit assets.

Harness Engineering。

Once the same content is obtained, another party can theoretically recreate similar Context / Harness Engineering.


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


Therefore, even if a third party obtains the same courses, Prompt, or Knowledge, it does not automatically obtain:

historical consumer tasks;
- Creator Calibration / Creator calibration;
preference and correction data;
decision-boundary data;
the final trained Adapter Weights.


The higher replication cost does not primarily come from the model file being unreadable. It comes from:

> **The need to reproduce the history of expert calibration from which those model parameters were created.**

---

## 7.3 Creator Ownership


Hatch does not take ownership of Creator Data.

Model Asset。

Creator-specific Training Data, LoRA Adapters, and final models can belong to the Creator under the applicable product and contractual terms, and the Creator can export their Adapter / Model Asset.


Hatch’s product principle can therefore be stated as:

> **Creator owns the intelligence; Hatch provides the infrastructure used to produce it.**


Where real consumer interactions are used to produce training data, appropriate data authorization and purpose permissions must be obtained separately.

---

# 8. Hatch Value Capture


Hatch’s commercial value does not depend on owning Creator Data or preventing Creators from exporting their models.


Hatch provides the infrastructure for continuously producing, training, validating, and operating Creator-specific AI Assets.


The complete lifecycle includes:

```text
Consumer Task
→ Agent Runtime
→ Creator Calibration
→ Structured Dataset
→ Dataset Versioning
→ Training
→ Evaluation
→ Model Version
→ Deployment
→ New Calibration Data
```


The persistent value in this system is not limited to Fine-Tuning compute itself.


The current open-source ecosystem has significantly reduced the engineering barrier and GPU cost of SFT, DPO, LoRA / QLoRA, and related methods.


For experiments involving hundreds of examples, the primary inputs are often:

- Expert Time
- Data Construction
- Preference Annotation
- Counterfactual Construction
- Edge Cases
- Blind Evaluation


rather than a single GPU Run.


Hatch’s Value Capture is concentrated across three commercial layers.

---

## 8.1 Creator Platform


Creators first use Hatch for:

- Agent Corpus Construction
- System / Skills / Knowledge Management
- Runtime
- Eval
- Regression
- Release
- Version Management
- Creator Calibration Workflow


These capabilities provide standalone value before the Creator reaches Fine-Tuning readiness.


The corresponding business model can include recurring software and infrastructure revenue such as:

- Creator Subscription
- Workspace Fee
- Product-Level SaaS Fee

---

## 8.2 Model Development


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


What is being sold here is not simply GPU time.


GPU Training itself is becoming commoditized. Hatch provides:

> **The complete production process from real expert calibration to a validated Private Model Asset.**

Infrastructure Revenue。

This layer can support higher-value Premium Model Development Service / Infrastructure Revenue.

---

## 8.3 Managed Model Infrastructure


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


Therefore:

```text
Creator Owns the Model
≠
Creator Must Operate the Model Infrastructure
```


Hatch can support Asset Portability while providing the default Managed Deployment Environment.


Commercially, this can generate recurring:

- Inference Revenue
- Hosting Fees
- Model Management Fees
- Usage-Based Infrastructure Revenue


This means Hatch does not need to rely on Data or Model Lock-In to create recurring revenue.


The Creator can take the asset elsewhere; Hatch captures value by continuing to provide a more convenient and complete infrastructure for model production and operation.

---

## 8.4 Hatch’s Core Commercial Asset


Hatch does not need to own all Creator training data.


What Hatch accumulates over time is an:

> **Expert Data and Model Production Infrastructure**


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


Its core capability is:


> **To convert judgment generated through real professional services into trainable data with relatively low expert-time overhead, and then turn that data into validated, deployable Creator-Specific Model Assets.**


Hatch captures value by continuously providing this infrastructure, rather than by taking ownership of Creator Intelligence.

---

# 9. Why It Is Harder to Replicate Than Prompt / Corpus Alone


Prompt, Skill, and Knowledge are explicit software assets.


They can be:

read;
exported;
rewritten;
recombined;
reimplemented in another Agent Framework.


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


Even if a competitor can replicate the Agent software architecture, it cannot directly replicate the expert-calibration history that has already occurred or the parameters trained from that history.


With Fine-Tuning added, Hatch can therefore produce two categories of assets:

|Type |Form |
|---|---|
| Explicit Agent Assets | System / Skills / Knowledge / Tools |
| Parameterized Model Assets | LoRA / Model Weights |


Both are built on top of the same Hatch Factory, Runtime, Eval, and Release Infrastructure.

---

# 10. Criteria for Adopting Fine-Tuning


Fine-Tuning is not assumed to be superior to Context Engineering by default.


Each training effort should be compared against at least:

```text
Base Model
Best System Prompt
Few-Shot
Agent Corpus
Fine-Tuned Model
```


Evaluation should use genuinely Held-Out Cases.


Fine-Tuning should only be deployed when it produces an actual improvement in at least one relevant dimension, such as:

- Expert-Aligned Quality
- Consistency
- Decision-Boundary Accuracy
- Tool-Use Behavior
- Generalization
- Deployment Characteristics


This means Hatch is adding a new:

> **Model Adaptation Capability**

Harness Engineering。

rather than replacing the existing Context / Harness Engineering stack with Fine-Tuning.

---

# 11. One-Sentence Architecture Definition

### Current

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

### With Fine-Tuning

```text
Creator Agent
=
Existing Context / Harness Engineering
+
Optional Creator-Specific Model Adaptation
```


The core change is straightforward:


> **On top of the existing Agent Corpus and Harness, Hatch adds the capability to parameterize selected expert Judgment, Behavior, and Agent Policy into model weights.**
