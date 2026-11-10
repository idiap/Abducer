<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Essential Reasoning Types and Skill Materializations

This is an initial epistemological map of the framework. It separates what
licenses a conclusion from how the framework executes, schedules, validates,
or presents work.

A reasoning type is an abstract epistemic operation. A skill is a concrete
materialization of one or more such operations. A reasoning style is an
ordered composition of types, normally implemented by several skills.
Consequently, the mapping is many-to-many:

    reasoning type  --materialized by--> one or more skills
    skill           --may realize------> primary + secondary types
    reasoning style --composes---------> several types + guards

The machine-readable initial map is
agentic/registries/essential_reasoning_types.yaml.

The dual [epistemic output typology](epistemic-output-types.md) specifies what
each reasoning relation may emit, the properties carried by those outputs, and
which downstream consumers may use them.

The compact composition language is specified in
agentic/spec/reasoning_flow_language.md. Curated examples live under
agentic/reasoning_flows, while the source-bound occurrence projections are
generated at agentic/state/reasoning_type_workflow_projections.json.

ERFL 0.2 treats relational coherence as the primary invariant. Reasoning-type
letters name types; local aliases name distinct occurrences; bracketed
interfaces conserve claim and state identity; labelled edges state the
epistemic relation:

    a:A[gap->hypothesis]
      -assume> d:D[hypothesis->claim]
      -test> r:R[claim->verdict]
      -calibrate> e:E[claim,verdict->status]

The chain means that deduction is conditional on the abductive hypothesis,
refutation tests the derived claim, and calibration consumes both claim and
verdict. It does not mean that deduction validates the hypothesis.

## Initial ontology

| Type | Epistemic function | Maximum licensed status |
|---|---|---|
| Deductive entailment | Derive what follows from typed premises and rules | Entailed given premises |
| Abductive hypothesis formation | Propose explanations, missing premises, or bridges | Candidate explanation |
| Inductive generalization | Infer a scoped pattern from multiple cases | Provisional generalization |
| Structural analogy and transfer | Transport a candidate through an explicit correspondence | Candidate transfer |
| Contrastive counterfactual reasoning | Compare a baseline with a controlled alternative | Contrast supported |
| Model-based reasoning | Probe behavior through an explicit idealized model | Model supported |
| Critical refutational testing | Search for counterexamples, contradictions, and defeaters | Refuted, or not refuted within scope |
| Evidential status calibration | Assign or conserve status using evidence and promotion rules | Creates no substantive claim |

The first six are core inference families. The last two are cross-cutting
epistemic controls: they are essential to reliable reasoning compositions but
do not function like ordinary conclusion-generating inference.

## What is deliberately not an essential reasoning type

Generative reasoning describes an execution mode, not a warrant. Workflow
composition, dependency closure, and deterministic validation describe
operational capabilities. Ingestion and reporting move or present epistemic
content. None independently licenses a scientific or mathematical conclusion.

This distinction matters for orchestrators. For example, the cohere-fast
orchestrator composes reasoning-bearing skills, but successful control flow
does not inherit their epistemic authority and is not itself a scientific
inference.

## Example compositions

Abductive discovery:

    abduction
      -> deductive consequence tracing
      -> counterfactual or model probes
      -> refutational testing
      -> status calibration

Proof search:

    abductive or analogical candidate
      -> deductive derivation
      -> premise and transfer audit
      -> status calibration

Theory abstraction:

    induction over cases
      -> structural analogy
      -> abductive synthesis
      -> deductive predictions
      -> critical testing

Model-mediated inquiry:

    bounded model
      -> controlled contrasts
      -> scoped generalization
      -> status calibration

## Reading the mappings

Each curated skill has one primary reasoning type, optional secondary types,
an epistemic role, and a confidence level. A validator can materialize a type
without generating its candidate conclusions: for example, an entailment-gap
auditor tests deductive entailment while primarily serving refutational
testing.

The map is intentionally marked curated exemplars, not complete coverage. The
next refinement should inspect the remaining skills individually, record input
and output epistemic states at the skill-contract level, and distinguish true
multi-type skills from orchestrators that merely invoke several types.

The initial structural projection maps 8 of 104 workflow skill occurrences.
It is therefore explicitly degraded and non-executable. Unmapped occurrences
and ambiguous conditional joins remain visible gaps; they are never silently
removed or inferred from a skill name.

The curated ERFL files are consequently labelled hypothesized summaries rather
than certified projections. Source-derived relations currently remain
relationally unknown until skill mappings bind claim identity, input/output
ports, scope, provenance, taints, claim ceilings, and join modality. Structural
dependency is represented as requires and never promoted automatically to
supports.
