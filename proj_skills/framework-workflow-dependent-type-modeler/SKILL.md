---
name: framework-workflow-dependent-type-modeler
description: Model extracted Prism workflows for paper writing with dependent-type-style contexts, indexed assessments, judgments, and explicit adapters. Use when value-sensitive dependencies should be visible in a workflow appendix while separating native nominal contracts from proposed type refinements.
---

# Framework Workflow Dependent Type Modeler

Produce `PrismWorkflowDependentTypeModel` version `1.0.0` from a frozen `PrismWorkflowAppendixSource` packet. This is a manual mathematical authoring lane, not a Prism compiler extension or proof assistant. Default to the paper's named reasoning workflows; label the Prism ME development lifecycle separately if requested.

Read [the packet contract](references/dependent-type-model-contract.md) before modeling. Use [the worked native example](references/worked-example.md) for the abductive motif, retained claim bindings, and proposed assessment indices. Missing source facts go back to `$framework-prism-workflow-extractor`; do not silently extend the frozen evidence boundary.

1. Preserve source identity, digest, profile, evidence posture, branch provenance, and coverage gaps. Keep exact nominal signatures beside their mathematical presentation.
2. Introduce an ordered context/telescope of named values and assumptions. A later binding may depend only on earlier bindings. Separate data values, relation records, and actual proof terms.
3. Use `Γ ⊢ t : T` for a typing judgment. Use dependent `Π` or `Σ` when a declared family actually depends on the bound value; use arrows and ordinary records for constant families. Record whether each family is native or a proposed refinement and how its indices constrain terms.
4. Compose by explicit let binding and capture-avoiding substitution. Retain original claim bindings through assessment and routing; a value of `Assessment(c₁)` cannot be used as `Assessment(c₂)` by renaming or similarity.
5. Preserve `Generated[T]` and source-explicit `.value` adapters. Generation is an opaque declared boundary, with no inferred totality, normalization, monad laws, or erased effects. An opaque operation symbol supports descriptive syntax, not an execution theorem.
6. Preserve relation annotations and guards. A source/target certificate record or successful test is not automatically a proof of truth, an identity witness, or permission to cast. For equality distinguish definitional conversion from identity types and explicit transport.
7. Keep alternatives, stop outcomes, feedback, partial order, and joins visible. Do not turn a routing value into executed branching or a feedback sketch into structural recursion with a termination proof.

Deliver a context table, operation judgments, one representative derivation, an index mismatch example, adapter/equality obligations, and claim boundaries in the request output directory. Route candidate claims through `$framework-paper-claim-curator` and hand the packet to `$framework-paper-dependent-type-writer`. The category model is optional comparative input; do not infer a categorical semantics, equivalence, or automatic translation from shared notation.

Before delivery check free variables, telescope order, instantiated indices, wrapper boundaries, all required named ports, source references, and native/proposed labels. Report manual checking as manual checking. Do not invent an installed checker or claim the paper's entire calculus has metatheoretic properties because these local judgments are readable.
