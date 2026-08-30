# Hatch: Adding Creator Private Model Capabilities on Top of the Agent Corpus

## 1. Current Product Architecture

The Agent currently delivered by Hatch consists of the following components:

| Layer | Role |
|---|---|
| System Prompt / Instructions | Global behavior, priorities, boundaries, and persistent rules |
| Skills | Reusable methods, workflows, and local capabilities |
| External Tools | Execution capabilities such as search, files, APIs, and MCP |
| Knowledge | Expert materials, cases, and long-tail knowledge |

The Runtime loads the corresponding Agent Corpus for each task and is responsible for model calls, tool execution, context, conversation state, and delivery.

The Creator Factory currently compiles expert materials and Creator judgment into an Agent Corpus. The current implementation is explicitly **prompt-and-corpus compilation** and does not include fine-tuning or model weight updates.

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

In the future, Hatch will add the following capability on top of the existing context / harness engineering stack:

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
Creator-specific merged model
```

Fine-tuning does not replace System, Skills, Tools, or Knowledge.

It adds a new model-parameter layer.

---

## 3. What Goes Into Context vs. What Goes Into Weights

Different types of information are better suited to different layers.

| Information Type | Primary Layer |
|---|---|
| Latest knowledge, facts, and cases | Knowledge / RAG |
| Explicit methods and workflows | Skills |
| Product boundaries and global requirements | System Prompt |
| External execution capabilities | Tools / Runtime |
| Stable behavioral patterns | Fine-tuning |
| Stable judgment / taste | Fine-tuning |
| Stable tool-use policy | Fine-tuning / trajectory training |

The primary purpose of Fine-Tuning is therefore not to put all of a Creator’s knowledge into the model. It is to parameterize patterns that have been repeatedly observed, including:

- judgment
- behavior
- preference / taste
- decision boundary
- tool policy
- agent policy

The current exploration identifies three primary categories of training data:

| Data | Learning Objective | Typical Training Method |
|---|---|---|
| Behavior / Output | How the model should respond | SFT |
| Judgment / Preference | Which answer is better | DPO |
| Agent Trajectory | How the model should act | Trajectory SFT / RL |

---

## 4. Data Sources

Training data will primarily come from Creator calibration of real consumer tasks.

The basic data flow is:

```text
Consumer Task
↓
Creator Agent execution
↓
Creator review / correction / comparison
↓
Structured expert signal
↓
Dataset
↓
Fine-tuning
↓
Candidate model
↓
Blind evaluation
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

In the future, this can be extended to include:

- post-edit
- chosen / rejected pair
- rejection reason
- counterfactual
- decision flip
- trajectory
- real task outcome

A high-value data unit can therefore expand from a simple:

```text
Question → Answer
```

into:

```text
Case
+ Expert Answer
+ Alternative
+ Preference
+ Why
+ Counterfactual
+ Decision Flip
+ Edge Case
```

Consumer data entering the training system requires separate authorization and purpose constraints. The current V1 does not allow Buyer private data to automatically enter the Creator learning dataset.

---

## 5. Creator Experience

Fine-tuning does not require a Creator to prepare training data when creating an Agent.

The product path can be:

```text
Create Agent
↓
Launch System + Skills + Tools + Knowledge
↓
Real consumers begin using it
↓
Creator continuously calibrates
↓
Accumulate sufficient high-quality data
↓
Hatch assesses training readiness
↓
Train Creator-specific model
↓
Blind-evaluate against the existing Agent baseline
↓
Deploy once requirements are met
```

A Creator can therefore begin with the existing Agent Corpus capabilities and gradually gain model fine-tuning capabilities as real usage accumulates.

Fine-tuning is a later-stage capability, not a prerequisite for Agent creation.

---

## 6. Private Model Asset

The training output can be:

### Creator-specific LoRA Adapter

```text
Shared Base Model
+
Creator A LoRA
Creator B LoRA
Creator C LoRA
```

or:

### Creator-specific Merged Model

```text
Base Model
+
Creator Adapter
↓
Merged Creator Model
```

A LoRA is tied to a specific base checkpoint, but the adapter itself can be independently stored, versioned, and exported.

The Creator can own and export their own adapter / model weights.

Hatch does not claim ownership over Creator data or model assets.

---

## 7. Asset Value for the Creator

Today, a Creator’s AI assets mainly include:

- source materials
- prompts
- skills
- knowledge base
- workflows
- product configuration

Fine-tuning can add:

- proprietary training dataset
- Creator-specific LoRA
- Creator-specific merged model
- model evaluation history
- model versions

Model weights are a more tangible technical asset because they:

- can exist as independent files;
- can be versioned;
- can be deployed;
- can be exported;
- can be combined with a base model;
- can be independently tested through held-out evaluation.

At the same time, even if another party obtains the same course materials, Prompt, or Skills, it will not automatically obtain the adapter weights created through the Creator’s calibration of real tasks.

---

## 8. Asset Value for Hatch

Hatch does not rely on ownership of Creator data as its primary moat.

What Hatch accumulates over time is:

### Expert Data Production Infrastructure

Specifically:

```text
Real-world tasks
→ Agent execution
→ Creator calibration
→ Structured training data
→ Dataset versioning
→ Training
→ Eval
→ Regression
→ Deployment
```

Fine-tuning itself is rapidly becoming commoditized.

With tools such as Qwen, LoRA / QLoRA, TRL, and Unsloth, the engineering barrier and GPU cost of training have fallen significantly. For experiments involving hundreds of training examples, the primary costs are usually not GPU compute, but:

- expert time
- data construction
- preference annotation
- counterfactual construction
- edge cases
- blind evaluation

Hatch’s core technical asset is therefore not the training algorithm itself, but:

> **The systematic capability to continuously transform real expert work into high-quality, trainable, and evaluable data.**

---

## 9. Why It Is Harder to Replicate Than Prompt / Corpus Alone

Prompt, Skill, and Knowledge are all explicit software assets.

They can be:

- read;
- exported;
- rewritten;
- recombined;
- implemented in another Agent framework.

Creator-specific model weights are produced through a different process:

```text
Real distribution
+
Agent mistakes
+
Creator calibration
+
Preference
+
Counterfactual
+
Repeated evaluation
```

Even if a competitor can replicate the Agent software architecture, it cannot directly replicate the expert calibration history that has already occurred or the parameters trained from that history.

With Fine-Tuning added, Hatch can therefore produce two categories of assets:

| Type | Form |
|---|---|
| Explicit Agent Assets | System / Skills / Knowledge / Tools |
| Parameterized Model Assets | LoRA / Model Weights |

Both are built on top of the same Hatch Factory, Runtime, Eval, and Release infrastructure.

---

## 10. Criteria for Adopting Fine-Tuning

Fine-tuning is not assumed to be superior to Context Engineering by default.

Each training effort should be compared against:

```text
Base Model
Best System Prompt
Few-shot
Agent Corpus
Fine-tuned Model
```

using genuinely held-out cases for evaluation.

Fine-Tuning should only be deployed when it produces a material improvement in at least one of the following dimensions:

- expert-aligned quality
- consistency
- decision-boundary accuracy
- tool-use behavior
- generalization
- deployment characteristics

This means Hatch is adding a new **model adaptation capability**, rather than replacing the existing Context / Harness Engineering stack with Fine-Tuning.

---

## 11. One-Sentence Architecture Definition

**Current**

```text
Creator Agent
=
System Prompt
+ Skills
+ Tools
+ Knowledge
+ Hatch Runtime / Eval / Release
```

**With Fine-Tuning**

```text
Creator Agent
=
Existing Context / Harness Engineering
+
Optional Creator-specific Model Adaptation
```

The core change is straightforward:

> **On top of the existing Agent Corpus and Harness, Hatch adds the capability to parameterize selected expert judgment, behavior, and agent policy into model weights.**

---

# 7. New Asset Class for Creators

Adding Fine-Tuning on top of the existing Agent Corpus creates a new category of independent technical assets for Creators: **Creator-specific model assets**.

Today, the Creator primarily owns explicit assets within Hatch:

| Asset | Form |
|---|---|
| Source Materials | Courses, articles, cases, and methodology materials |
| System Instructions | Global behavior and boundaries |
| Skills | Reusable methods and workflows |
| Knowledge | Domain knowledge, cases, and long-tail materials |
| Product Configuration | Tools, Runtime, and product configuration |

Fine-Tuning adds:

| New Asset | Form |
|---|---|
| Training Dataset | Dataset created through Creator calibration of real consumer tasks |
| LoRA Adapter | Creator-specific parameter delta based on a particular Base Model |
| Merged Model | Independent model created by merging the Base Model and Creator Adapter |
| Model Versions | Model versions produced from different training data, Base Models, and training methods |
| Evaluation Record | Performance record of each model version on Blind / Regression Eval |

A LoRA can be independently stored, versioned, deployed, and exported, and can be combined with its corresponding Base Model.

The Creator’s AI assets therefore expand from:

```text
Content
+ Prompt
+ Skills
+ Knowledge
```

to:

```text
Content
+ Agent Corpus
+ Training Dataset
+ Private Model Weights
```

The Model Asset does not replace the Agent Corpus.

System, Skills, Knowledge, and Tools continue to carry dynamic knowledge, explicit rules, runtime capabilities, and editable configuration. Fine-Tuning further writes the judgment, behavior, and tool policy suitable for parameterization into model parameters.

### 7.1 A More Tangible Technical Asset

Compared with a Prompt or software configuration, a Creator-specific model asset has several concrete technical properties:

- it exists as an independent model or adapter file;
- it has an explicit Base Model dependency;
- it can be identified through a digest / version;
- it can be independently deployed;
- it can be exported to other compatible inference infrastructure;
- it can be quantitatively evaluated against other model versions;
- it can continuously produce new versions as new data becomes available.

It is therefore not merely a set of configurations inside the Hatch platform, but a technical/IP asset that the Creator can actually possess and migrate.

This does not make any claim about a specific accounting or financial-asset classification. “Asset” here refers to its nature as a **storable, versionable, deployable, and portable software and model asset**.

### 7.2 Higher Replication Cost

System Prompt, Skills, and Knowledge are explicit assets.

Once the same content is obtained, another party could theoretically recreate similar Context / Harness Engineering.

A Creator-specific model, however, depends on a different set of historical data:

```text
Real consumer tasks
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

Therefore, even if a third party obtains the same courses, Prompt, or Knowledge, it does not automatically obtain the training data created through historical consumer tasks and Creator calibration, nor does it automatically obtain the final adapter weights.

The higher replication cost does not primarily come from the model file being unreadable. It comes from:

> **The need to reproduce the history of expert calibration from which those model parameters were created.**

The high-value unit of data is also not limited to Question → Answer. It can include Expert Answer, Rejected Alternative, Reason, Counterfactual, Decision Flip, and Edge Case.

### 7.3 Creator Ownership

Hatch does not take ownership of Creator Data.

Creator-specific training data, LoRA adapters, and final models can belong to the Creator under the applicable product and contractual terms, and the Creator can export their adapter / model asset.

Hatch’s product principle can therefore be stated as:

> **Creator owns the intelligence; Hatch provides the infrastructure used to produce it.**

Where real consumer interactions are used to form training data, appropriate data authorization and purpose permissions must be obtained separately. Under the current Hatch V1 data boundary, Buyer private data is not automatically included in the Creator learning dataset.

---

# 8. Hatch Value Capture

Hatch’s commercial value does not depend on owning Creator data or preventing Creators from exporting their models.

Hatch provides the infrastructure for continuously producing, training, validating, and operating Creator-specific AI assets.

The complete technical lifecycle includes:

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

The persistent value in this system is not limited to the Fine-Tuning compute itself.

The current open-source ecosystem has significantly reduced the compute barrier and GPU cost of SFT, DPO, LoRA / QLoRA, and related training methods. For datasets containing hundreds of examples, the primary costs are often expert time, data construction, Preference, Counterfactual, Edge Case creation, and Blind Evaluation rather than a single GPU Run.

Hatch’s value therefore concentrates in three commercial layers.

## 8.1 Creator Platform

Creators first use Hatch for:

- Agent Corpus construction;
- System / Skills / Knowledge management;
- Runtime;
- Eval;
- Regression;
- Release;
- Version management;
- Creator calibration workflow.

These capabilities already provide standalone value before a Creator reaches Fine-Tuning readiness.

The corresponding business model is recurring software and infrastructure revenue, such as Creator subscriptions, workspace fees, or product-level SaaS fees.

---

## 8.2 Model Development

Once a Creator has accumulated sufficient data, Hatch can additionally provide model-development capabilities:

- Training readiness assessment;
- Dataset construction;
- Train / Validation / Blind Test split;
- Base Model selection;
- SFT;
- DPO;
- Trajectory Training;
- Candidate evaluation;
- Prompt / Corpus / Fine-Tuned baseline comparison;
- Adapter / Model versioning;
- Export.

What is being sold here is not simply GPU time.

GPU Training itself is becoming commoditized. Hatch provides:

> **The complete production process from real expert calibration to a validated Private Model Asset.**

This layer can therefore support higher-value premium model-development service / infrastructure revenue.

---

## 8.3 Managed Model Infrastructure

Even when a Creator owns and can export their weights, they still require infrastructure to operate the model over time, including:

- compatible Base Model management;
- LoRA loading;
- Multi-LoRA serving;
- inference deployment;
- autoscaling;
- GPU utilization management;
- model version routing;
- observability;
- rollback;
- security;
- regression testing;
- retraining.

Therefore:

```text
Creator owns the model
≠
Creator must operate the model infrastructure
```

Hatch can support asset portability while providing the default managed deployment environment.

Commercially, this can generate recurring:

- inference revenue;
- hosting fees;
- model management fees;
- usage-based infrastructure revenue.

This means Hatch does not need to rely on data or model lock-in to create recurring revenue.

The Creator can take the asset elsewhere; Hatch captures value by continuing to provide a more convenient and complete infrastructure for producing and operating models.

---

## 8.4 Hatch’s Core Commercial Asset

Hatch therefore does not need to own all Creator training data.

What Hatch accumulates over time is an **Expert Data and Model Production Infrastructure**:

```text
Agent Creation
+
Real-world Execution
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

> **To convert judgment generated through real professional services into trainable data with relatively low expert-time overhead, and then turn that data into validated, deployable Creator-specific model assets.**

Hatch captures value by continuously providing this infrastructure, rather than by taking ownership of Creator intelligence.
