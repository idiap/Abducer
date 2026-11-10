---
name: framework-workflow-example-designer
description: Design realistic, representative worked examples for every workflow in a paper appendix. Use with frozen workflow sources and optional categorical or dependent-type models to make each workflow's defining reasoning mechanism concrete before appendix writing.
---

# Framework Workflow Example Designer

Produce `WorkflowExamplePlan` version `1.0.0` using [the plan contract](references/example-plan-contract.md). Consume the frozen `PrismWorkflowAppendixSource`, paper audience and scope, and the category or dependent-type model when that presentation is selected. This is a manual paper authoring lane; designing an example does not run the workflow or change the manuscript.

1. Inventory every in-scope workflow before choosing cases. Preserve source IDs, profile/layer distinctions and digest. Give each workflow its own coverage row and at least one case; one appealing example for the whole appendix is insufficient. A missing source or model fact stays an explicit gap and goes back to extraction/modeling. Do not shrink scope to make coverage look complete.
2. Choose a plausible scientific or problem-solving question that makes this workflow useful. Supply enough actual input content, quantities, assumptions, or candidate explanations for a reader to follow the reasoning. Prefer the paper's domain, without copying a research conclusion merely to make the story successful.
3. Work through informative intermediate transformations tied to source occurrences: what is proposed, inferred, compared, challenged, revised, or learned? Distinguish source-supported mechanism from invented case data. Include the decisive branch, contrast, or dependency explaining why this particular workflow matters. A straight-line workflow can use a contrast with a tempting invalid shortcut; do not invent a runtime branch. Parallel workflows retain independence and a meaningful join.
4. Give a useful outcome and a stated limit. A refuted candidate can be valuable if the example identifies the counterexample and resulting change to the problem. A status such as “approved,” “receipt produced,” or “ready” is not the scientific outcome. Use administrative details only when they materially explain the reasoning; receipts, filenames, approvals and status transitions must not become the story.
5. Label authored cases as illustrative. Never present invented measurements, solver runs, expert judgments or successful proofs as observed evidence. For real traces, bind observations to exact evidence; separate illustrative additions. Derive small mathematical calculations explicitly and bound their claim. An example about a proof workflow does not prove the paper's target theorem.
6. Bind the case to the selected mathematical representation. Preserve category endpoints, wrappers and required retained inputs; do not infer commuting paths from similar outcomes. For dependent types preserve exact claim indices through assessment and routing, telescope order and native/proposed labels. Concrete evidence about `c₁` cannot be reassigned to `c₂` because their text resembles each other. Use only the model's justified equality/transport, with unresolved obligations retained.
7. Read the planned case as a domain reader: does each important step change the reader's understanding, and does the outcome answer the initial question? Compare cases across workflows. A shared scientific setting is welcome, but changing names in an identical story does not establish representativeness. Repair generic, implausible, uninformative or structurally mismatched examples before marking them ready.

Hand the plan to `$framework-paper-workflow-example-writer`, with candidate empirical or capability claims routed to `$framework-paper-claim-curator`. Coverage is complete only when every scoped workflow has a ready representative example and the corresponding source/model checks pass. Report blocked rows honestly; they do not count as covered. This requires one meaningful case per workflow, not execution of every branch or an exhaustive benchmark suite.

## Mandatory step explanation gate

Read [the shared step explanation contract](../framework-paper-workflow-appendix-writer/references/step-explanation-contract.md) for occurrence-level paper revisions.

Plan one continuous case per workflow, with concrete input and output at every binding, named joins and a changed-input contrast. Explicitly plan unresolved producer boundaries; never silently fill them.
