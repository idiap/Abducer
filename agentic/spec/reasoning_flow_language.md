<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Epistemic Reasoning Flow Language

ERFL 0.3 is a compact language for describing goal-oriented reasoning flows while
abstracting away skills, agents, tools, artifacts, and runtime implementation.
Its central invariant is relational coherence: every transition must conserve
at least one named claim or epistemic-state handle and must state what relation
licenses the transition.

Its eight symbols are:

| Symbol | Reasoning type |
|---|---|
| D | deductive entailment |
| A | abductive hypothesis formation |
| I | inductive generalization |
| T | structural analogy and transfer |
| C | contrastive counterfactual reasoning |
| M | model-based reasoning |
| R | critical refutational testing |
| E | evidential status calibration |

An occurrence has the form alias, type, and relational interface:

    h:A[gap->hypothesis]

This names one abductive occurrence h, consuming gap and producing hypothesis.
Repeated uses of A or E remain distinct occurrences.

Relations are deliberately few:

| Form | Meaning |
|---|---|
| X -requires> Y | structural dependency only; supplies no warrant |
| X -assume> Y | a candidate is retained explicitly as a premise |
| X -test> Y | a claim becomes the object of refutational testing |
| X -calibrate> Y | findings and verdicts feed status calibration |
| X -constrain> Y | status or defeaters narrow admissible outputs |
| X -generalize> Y | cases become a scoped provisional generalization |
| X -transfer> Y | a source structure enters an explicit transfer |
| X -probe> Y | a claim is examined through a model or contrast |
| X -revise> Y | a calibrated or adverse result starts a revised occurrence |
| X -preserve> X | type and epistemic interface are explicitly conserved |
| X > Y | legacy unlabelled dependency; rejected by strict coherence validation |
| X vertical-bar Y | retain a set-valued alternative with a common output interface |
| X & Y | require both branches before joining |
| X? | optional reasoning operation |
| repeat m..n [reasoning] until predicate | bounded goal-directed iteration |
| on predicate => stop or accept | terminal disposition |
| on predicate => switch @workflow | switch reasoning workflow |

Long statements may be split across physical lines by placing `...` at the end
of every continued line. Indentation is ignored by the parser and can therefore
be used to align occurrences and relations:

    steps e0:E[kb,source->ground] -constrain> ...
          a0:A[ground->candidate] -test> ...
          r0:R[candidate->verdict] -calibrate> ...
          e1:E[candidate,verdict->status]

This is exactly equivalent to one logical `steps` line. The explicit marker is
required: indentation alone never creates continuation, grouping, sequence, or
scope. A final `...` without another physical line is a syntax error.

Example:

    erfl 0.2
    reasoning abductive_discovery {
      goal "find a discriminating explanation" -> calibrated_epistemic_status
      steps a:A[gap->hypothesis] -assume> d:D[hypothesis->consequence] -test> r:R[consequence->verdict] -calibrate> e:E[consequence,verdict->status]
      repeat 1..3 [a:A[status->hypothesis2] -assume> d:D[hypothesis2->consequence2] -test> r:R[consequence2->verdict2] -calibrate> e:E[consequence2,verdict2->status2]] until e.promotable measure obligation_reduction
      on r.refuted => stop
      on e.promotable => accept
      on reasoning.stalled => switch @conceptual_frontier_deepening
    }

A goal need not be reducible to a short natural-language description. The
compact form above remains shorthand for simple cases. A complex goal is a
first-class specification with addressable critic criteria, evidence
obligations, constraints, and an explicit satisfaction policy:

    erfl 0.3
    reasoning critical_review {
      goal {
        summary "admit only a claim that survives the specified review"
        target critically_calibrated
        criterion validity "Every inferential step is licensed by stated premises."
        criterion alternatives "The strongest live alternative explanation is tested."
        criterion scope "The conclusion stays within the evidence and model scope."
        evidence audit_trace "A claim-linked trace records tests, verdicts, and unresolved objections."
        constraint no_laundering "Not-refuted and conditional results cannot be promoted to proved."
        satisfy all(validity,alternatives,scope)
      }
      steps r:R[candidate->verdict] -calibrate> e:E[candidate,verdict->status]
      on e.critically_calibrated => accept
      on e.refuted => stop
    }

Criteria are independently identifiable so critic results can refer to them
without parsing prose. Evidence and constraints remain obligations even though
`satisfy` ranges over criteria: reaching the target state requires the
calibration occurrence to report their disposition. ERFL does not infer that a
criterion passed merely because the route terminated.

## Knowledge-base references

A document preamble connects a local symbol to a specific KB resource:

    @KB kb0 connect(file("KB/yang-mills-existence-and-mass-gap.kb.md"))

Interactions are directional and separate from epistemic composition:

    e0 <-query- kb0
    e0 <-search- kb0
    e1 -persist-> kb0

The inverted arrows say that `e0` draws material from `kb0`; query addresses
known members, while search may inspect a broader indexed subset. The regular
arrow says that calibrated occurrence `e1` writes a versioned successor. A
querying or searching occurrence must expose `kb0` among its inputs, and only
an `E` occurrence may persist. The declaration precedes `reasoning`; it is
environmental context, not an inference step. The underlying KB object
may carry the richer epistemic contract defined by
`agentic/spec/knowledge_base.schema.json`; the reasoning program does not restate it.

Persistence has one boundary:

    source material
      -> proposed members (artifacts; no KB authority)
      -> validated writeback
      -> KB version n+1 (authoritative problem snapshot)
      -> derived indexes, graphs, and reports (regenerable views)

Revision outputs remain proposals until authorized writeback persists a
successor of the referenced KB. Generated artifacts and reasoning logs never
become KB members implicitly.

The grammar is:

    document  := physical_line_continuation* "erfl" VERSION kb_resource* reasoning
    physical_line_continuation := statement_fragment "..." NEWLINE
    reasoning := "reasoning" ID "{" goal steps kb_interaction* repeat* handler+ "}"
    kb_resource := "@KB" ID "connect(file(" STRING "))"
    kb_interaction := OCCURRENCE "<-" ("query" | "search") "-" KB_ID
                    | OCCURRENCE "-persist->" KB_ID
    goal      := "goal" STRING "->" STATE | structured_goal
    structured_goal := "goal" "{" ["summary" STRING] "target" STATE
                       criterion+ evidence* constraint* satisfy "}"
    criterion := "criterion" ID STRING
    evidence  := "evidence" ID STRING
    constraint:= "constraint" ID STRING
    satisfy   := "satisfy" ("all" | "any") "(" ID ("," ID)* ")"
    steps     := "steps" expression
    repeat    := "repeat" INT ".." INT "[" expression "]" "until" predicate
    handler   := "on" predicate "=>" ("stop" | "accept" | "switch @" ID)
    expression:= sequence
    sequence  := choice (RELATION choice)*
    choice    := parallel ("|" parallel)*
    parallel  := atom ("&" atom)*
    atom      := [ALIAS ":"] TYPE "[" HANDLES "->" HANDLES "]" ["?"]
               | ALIAS ":_" "[" HANDLES "->" HANDLES "]"
               | "(" expression ")"
    predicate := (ALIAS | "reasoning") "." STATUS

ERFL encodes epistemic dependency, not temporal telemetry. A projection may
collapse ingestion, orchestration, persistence, reporting, and adjacent
repetitions of the same reasoning type. Parallel branches mean all epistemic
contributions are required; alternatives do not imply that execution chooses
randomly. Workflow switches are explicit and never inferred from prose.

The complete repository representation set and its task-facing alias mapping
are indexed in `agentic/registries/reasoning_flow_catalog.yaml`. The narrower
`reasoning_flow_projections.yaml` registry records the source-projected named
workflow subset and must not be interpreted as the complete flow inventory.

Every complete reasoning path must end in a named E occurrence so that its claim
ceiling and unresolved obligations remain visible. Acceptance and workflow
switches require a predicate on such a calibrated occurrence. Iteration is
always bounded and declares an observable progress measure. A successful
workflow execution does not by itself satisfy an epistemic goal.

The underscore occurrence is an unresolved projection gap. It conserves
structure and handles without pretending to know which reasoning type occurred.
A reasoning program containing such a gap is descriptive and non-executable.

Each reasoning occurrence has a standard semantic codomain declared in
agentic/registries/epistemic_output_types.yaml. Compact flows may leave that
codomain implicit. Named semantic ports become mandatory when alternatives,
joins, workflow handoffs, or iteration deltas would otherwise admit more than
one assignment. Artifact or packet names are never valid semantic port types.

Relational coherence additionally conserves claim identity, scope, provenance,
taints, claim ceilings, and open obligations. Deduction from an abductive
candidate means entailed if that candidate holds; it does not validate the
candidate. Not-refuted-within-scope is not proof. Calibration creates no new
substantive claim.

## Predicate-map abstraction

For a system-level view, detailed `steps` collapse to an ordered,
duplicate-free predicate signature. Its domain is the named reasoning program
and its range is a qualified named output:

    reasoning::conceptual_hypothesis_exploration_loop ...
      -constrain, transfer, assume, test, calibrate> ...
      output::conceptual_hypothesis_exploration_loop.refinement_status

Connections between reasoning programs pass through that named output:

    output::conceptual_hypothesis_exploration_loop.refinement_status ...
      -> reasoning::abducer_work_loop

The predicate map hides occurrences and ports while preserving relation order,
output identity, terminality, and cross-reasoning connections. The generated
system map is `agentic/reasoning_flows/all-reasoning.pmap`; its natural-language
reference is `docs/reference/reasoning-predicate-map.md`.
