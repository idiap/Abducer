<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Epistemic objects and reasoning operations

This reference governs how `to_prism` derives project-specific types from a
new project. It prevents epistemically different objects from collapsing into
generic names such as `Input`, `Output`, `Item`, `ReasoningResult`, or
`List[String]`.

> A type states what a value is, how it became available, and what downstream
> reasoning may legitimately do with it.

The target project supplies the vocabulary. Its instructions, schemas,
examples, hooks, validators, consumers, and tests must confirm every type and
field. Examples in Prism's argumentation, refinement, and release-readiness
catalogues induce candidate shapes only; they are not source-specific truth.

## Epistemic object families

These objects are not interchangeable. Give each relevant object a nominal,
domain-specific type.

| Object | Exact meaning | Required identifying fields | Example specific type |
| --- | --- | --- | --- |
| Statement | A linguistic token in a document, message, transcript, or tool response | text, author/speaker, source location, time/revision when relevant | `IncidentReportStatement` |
| Proposition | Truth-evaluable content independent of its particular wording | normalized content and referenced entities | `PossibleDatabaseSaturation` returning `Prop` |
| Claim | A proposition asserted by an accountable actor in a context | proposition, claimant, assertion context, time, qualification | `OperatorCauseClaim` |
| Observation | A record produced by a specified observation/measurement method | value, method/instrument, source, time, sampling context, limitations | `DatabaseLatencyObservation` |
| Evidence | An observation or attributable artifact considered in relation to a proposition under a rule | source object, target proposition, direction, provenance, policy | `Evidence[DatabaseLatencyObservation]` plus support/attack relation |
| Assumption | A proposition provisionally accepted without establishing it here | proposition, scope, owner, rationale, expiry/review condition | `IncidentTriageAssumption` |
| Hypothesis | A testable candidate explanation, prediction, interpretation, or bridge | proposition, explanatory target, mechanism, predictions, falsifiers | `IncidentCauseHypothesis` |
| Ranked hypothesis list | Ordered assessments of known hypotheses under declared criteria | candidates, criterion scores, scale/direction, weights, uncertainty, grounds, ties, method | `RankedIncidentHypotheses` |
| Critique | A structured assessment of a target artifact or inference | target, critic kind, standard, findings, severity, grounds, repair | `IncidentAnalysisCritique` |
| Objection | A reason against accepting a claim, inference, assumption, or decision | target, objection proposition, grounds, scope, response status | `CausalInferenceObjection` |
| Defeater | Information that lowers/removes warrant | target support relation, rebutting/undercutting kind, grounds, effect | `IncidentHypothesisDefeater` |
| Counterexample | An admissible case inconsistent with a universal claim or required property | target proposition, witness, admissibility grounds, violated condition | `RunbookCounterexample` |
| Judgment | An evaluator's assessment under an explicit standard | subject, standard, findings, confidence, evaluator, grounds | `IncidentSeverityJudgment` |
| Decision | An authorized commitment among alternatives | choice, alternatives, criteria, authority, rationale, effective time | `MitigationDecision` |
| Recommendation | Advice to an identified decision-maker, not a commitment | action, addressee, expected outcome, grounds, risks, preconditions | `MitigationRecommendation` |
| Action | A requested, attempted, or completed intervention | kind, target, actor/capability, preconditions, status, effects/failure | `RestartReadReplicaAction` |

### Distinctions that must survive conversion

**Statement is not proposition.** The same sentence in a ticket and a chat is
two statement tokens that may express one proposition. A quote carries
attribution; the proposition is what reasoning supports, attacks, or assumes.

**Observation is not evidence by itself.** A CPU measurement is an
observation. It becomes evidence for or against saturation through an explicit
relevance relation and material policy. The same observation may support one
hypothesis, defeat another, and be irrelevant to a third.

**Judgment, recommendation, decision, and action are distinct.** A severity
judgment evaluates. A recommendation advises. A decision commits an authorized
party. An action changes or attempts to change the world.

## Deriving project-specific contracts

For every workflow boundary:

1. Identify the domain referent from project nouns and downstream use:
   `CustomerRefundRequest`, not `Input`.
2. Identify its epistemic role from the table above.
3. Record who/what produced it, by which method, and from which source. Apply
   `Generated[T]`, `Evidence[T]`, or `Computed[T]` only when true.
4. Model consumer-visible alternatives as closed variants.
5. For every score, name criterion, direction, range/units, missing-data
   policy, aggregation rule, grounds, and uncertainty.
6. Preserve ties, disagreement, dissenting findings, unresolved objections,
   unsupported assumptions, and excluded candidates.
7. Separate operational error (`Result[T, E]`) from epistemic rejection or
   low support represented inside `T`.
8. Trace each field to a source contract, example, consumer, policy, or
   explicit reviewed decision.

Missing evidence warrants a specific `Option[T]`, uncertainty status, or
conversion issue—not an invented field and not a vague string.

### Example-derived starter patterns

Use these only when the target project contains the corresponding example.
They are deliberately small boundary patterns, not a universal ontology.

| Observed workflow example | Initial exact boundary | Keep inside the boundary type |
| --- | --- | --- |
| Incident or interpretation ranking | `HypothesisEvidence -> Generated[RankedHypotheses]` | candidates, criteria, grounds, ties, uncertainty, ranking method |
| Scientific-statement retrieval | `StatementRetrievalQuery -> RankedRelevantStatements` | source document/span, relevance score/basis, rank, corpus/index snapshot |
| Database access | `DatabaseQuery -> TabularResultSet` | parameters, schema/columns, rows, ordering, truncation, query provenance |
| Informal-logic review | `ArgumentFragment -> Generated[InformalLogicReview]` | premises/conclusion, stance, presumptions, defeaters, qualified position |
| SymPy autoformalization | `SympySource -> Generated[FormalizedEquation]`, then operational validation | parsed expression and assumptions in the generated artifact; identity/counterexample/trace checks remain separate |
| Equation formalization | `EquationStatement -> Generated[FormalizedEquation]` | symbols/assumptions plus SymPy and LaTeX representations when both are consumed |

Split one of these into additional nominal intermediate types only when the
source workflow exposes the intermediate as a port, validates it separately,
branches on it, or assigns it different provenance/assurance. For example,
`libs/mathformer/functions/sympy_pipeline.prism` justifies its several
`Sympy*Packet` and `Sympy*Report` types because distinct pipeline operations
consume and validate them. A project that only emits one equation artifact
does not inherit that entire type graph.

### Initial inference classes

Keep this classification small and occurrence-specific:

| Class | What licenses the output | Example |
| --- | --- | --- |
| Formal | explicit formal system, premises, and rules | checked logical derivation |
| Material/defeasible | domain content, relevance, evidence policy, and defeaters | ranking explanatory hypotheses or assessing an informal argument |
| Representational | an alignment/policy mapping one representation to another | statement or equation formalization |
| Symbolic-computational | named algorithm under assumptions and side conditions | SymPy transformation or equation solving |

Retrieval and database querying may be purely operational and need no
inference label. A workflow can combine classes, but do not create a new class
for every skill verb.

### Ranked hypotheses require a complete contract

“Return a ranked list of hypotheses” minimally induces these candidates:

```text
IncidentCauseHypothesis
  = project-recognized causal alternatives
HypothesisCriterion
  = explanatory coverage, contradiction count, test cost, etc.
CriterionAssessment
  = hypothesis + criterion + value/scale + grounds + uncertainty
IncidentHypothesisAssessment
  = hypothesis + assessments + defeaters + aggregate rationale
RankedIncidentHypotheses
  = ordered assessments + rule + ties + exclusions + evidence snapshot
```

The output is not `List[String]`. Rank is not truth: it is the result of a
particular rule applied to a particular candidate set and evidence state.
Generated hypotheses ordinarily remain `Generated[List[...]]` until assessed.

## Exact generative reasoning operations

The `to_prism` conversion profile wraps every epistemic result below in
`Generated[...]`. Retrieval/query, deterministic validation, symbolic
execution, and effectful action are operational or material boundaries. They
can consume or assess generated output, but cannot be folded into the
epistemic occurrence to give it stronger provenance or assurance.

| Operation | Required inputs | Exact output | Does not establish |
| --- | --- | --- | --- |
| Generate hypotheses | question, constraints, observations, generation policy | `Generated[CandidateHypothesisSet]` with origin and coverage notes | plausibility, rank, support, truth |
| Abduct | explanatory target, candidates, relevant evidence, criteria | `Generated[RankedHypotheses]` with residual anomalies | proof or certainty that the leader is true |
| Rank | fixed candidates, criteria/scales, evidence, tie/aggregation rule | `Generated[RankedAssessments]` with scores, grounds, ties, exclusions, sensitivity | new candidates or validation of winner |
| Compare | alternatives, dimensions, comparison basis | `Generated[AlternativeComparison]` with trade-offs and missing evidence | winner without a decision/ranking rule |
| Critique | target, critic standard, admissible grounds | `Generated[DomainCritique]` with located findings, severity, grounds, repair | falsity of the entire target |
| Adversarial review | target, threat model, roles, attack budget/scope | `Generated[AdversarialReview]` with challenges and surviving claims | exhaustive/unbiased review or automatic refutation |
| Refute | target proposition/inference, counterevidence, refutation rule | `Generated[CandidateDefeaters]` with affected scope | adjudicated negation of the target or unrelated claims |
| Calibrate | predictions/judgments, outcomes/reference evidence, method/population | `Generated[CalibrationAssessment]` with population, error, and uncertainty | deterministic statistical validation or correctness of one conclusion |
| Synthesize | typed findings/claims/evidence, compatibility/conflict policy | `Generated[IntegratedAssessment]` retaining provenance, conflict, and omission | consensus, proof, permission to erase dissent |
| Judge/recommend | alternatives, findings, objectives, constraints, identified addressee | `Generated[DomainJudgment]` or `Generated[DomainRecommendation]` | authorized decision or execution |

Parsing, routing, retrieval, formatting, prompting, retrying, and tool calling
are operational steps. They are not reasoning methods merely because a skill
performs them.

## Workflow reasoning occurrences compose skills many-to-many

A source skill is a capability/artifact, not automatically one reasoning
occurrence. Conversely, one workflow reasoning type can materialize through
several skills, and one skill can contribute to several reasoning occurrences.
Decompose by semantic transformation, not file boundaries:

```text
statements + observations
  -> claim-normalization skill
  -> hypothesis-generation skill
  -> evidence/assumption critic skills (parallel where independent)
  -> defeater/counterexample search skill
  -> abductive assessment + ranking skills
  -> synthesis skill preserving disagreement
  -> recommendation skill
  -> authorized decision
  -> effectful action skill/tool
```

For example, `libs/argumentation/skills/informal_logic/` and
`libs/argumentation/workflows/argumentation/` induce candidate types
such as `ArgumentStatement`, `NormalizedClaim`, `Premise`, `Conclusion`,
`ArgumentCritique`, and `RankedInterpretationHypotheses`. Refinement workflows
in `examples/language/refinement_loop/` induce `RevisionCandidate`,
`CriticFinding`, `RefinementFeedback`, `RefinementAttempt`, and
`ExhaustedRefinement`; `docs/tutorial/release_readiness/` induces
`ReleaseObservation`, `ReadinessClaim`, `ReleaseRiskObjection`,
`ReadinessJudgment`, and `ReleaseDecision`. These names illustrate what a
careful derivation might discover; a target project adopts them only when its
own evidence confirms the objects, fields, and operations.

The canonical `.prism` must expose this composition even if one provider prompt
asks one model to do everything. Split when an intermediate has an independent
consumer, review/critic/validator, branch/join, persistence boundary, or
different provenance/assurance. Merge complementary instructions and lenses
that jointly make one inseparable epistemic commitment. Operational work stays
in materialization. Record the chosen and rejected boundary in
`granularity_rationale`.

Each epistemic occurrence has its own domain signature
`Input -> Generated[Output]`, relation edges, and material failure boundary.

## Critic taxonomy

A critic is determined by target, standard, admissible grounds, and output.

| Critic | Examines | Required output |
| --- | --- | --- |
| Logical-validity | inference under a named logic | invalid-inference findings, missing premises, or scoped validity judgment |
| Evidence-quality | source fitness, method, recency, independence, relevance | source-quality findings and affected support relations |
| Assumption | hidden, unsupported, stale, scope-sensitive assumptions | assumptions, challenges, consequences, tests needed |
| Alternative-hypothesis | omitted explanations and discriminatory predictions | additional hypotheses and observations that distinguish them |
| Causal | confounding, reverse causation, mechanism, intervention, temporal order | causal objections, alternative mechanisms, needed tests |
| Statistical/calibration | sampling, base rates, uncertainty, scoring, confidence | statistical findings, justified corrections, calibration gaps |
| Counterexample | universal claims, invariants, claimed coverage | admissible witnesses or bounded “none found” search report |
| Adversarial/security | attack surface under an explicit threat model | attacks/exploit traces, affected claims, severity, mitigations |
| Domain-constraint | named domain rules/expert standards | rule-specific violations, applicability, repair requirements |
| Decision/policy | objectives, authority, values, constraints, effects | objections, trade-offs, stakeholders, procedural defects |

A critic result must not be only `String`, `Bool`, or `List[String]`. At
minimum it identifies target, critic kind, standard, finding kind, grounds,
scope, severity, and disposition. “No issue found” records a bounded search
under a method; it is not proof that no issue exists.

A **critique** is the structured assessment; an **objection** is one reason
against acceptance; a **defeater** changes the warrant of a support/inference
relation; and a **counterexample** is a concrete violating witness.

## Specificity gate

Stop generation for review when an important boundary uses:

- `Input`, `Output`, `Data`, `Item`, `Payload`, `Context`, `ResultData`,
  `ReasoningResult`, or `CritiqueResult` without domain qualification;
- `String` where consumers distinguish domain alternatives;
- `List[String]` for hypotheses, evidence, findings, objections, decisions, or
  recommendations;
- a numeric score without criterion, scale, grounds, and uncertainty;
- evidence without attributable source object and target proposition;
- a ranked result without candidates, criteria, grounds, ties, and method;
- a critic without target, standard, and typed findings; or
- a decision without authority, alternatives, constraints, and rationale.

Generic names are acceptable only at genuinely generic library boundaries
where type parameters retain the concrete domain type.

## Review questions

1. What real-world or epistemic object does the value denote?
2. Which target-project artifacts and consumers justify every field?
3. Is this wording, asserted content, observation, or evidence-for-a-claim?
4. What uncertainty, disagreement, attribution, and provenance must survive?
5. Which exact operation transforms the inputs into this output?
6. Which rule makes a rank, critique, validation, or decision reproducible?
7. What stronger inference might a downstream user mistakenly make, and how
   does the type prevent it?

See `semantic-taxonomy.json` for the machine-readable catalogue,
`type-taxonomy.md` for Prism type families, and `layers.md` for placement.
