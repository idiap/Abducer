---
name: dynamic-symbolic-simulation-experimenter
description: Support a mature theory-driven discovery programme by designing, executing, inspecting, and packaging reproducible symbolic, finite-model, numerical-simulation, parameter-sweep, or hybrid probes for a precise theoretical question. Use only when reflective conceptual work has produced a formal consequence, countermodel question, calibration need, or discriminating ambiguity that computation can resolve; do not use experiments as the primary generator or selector of concepts.
---

# Dynamic Symbolic Simulation Experimenter

## Role

Serve theory formation with the smallest reproducible computation that can
clarify a mature theoretical question. Dynamically derive the probe from the
conceptual programme's objects, mechanisms, consequences, and support request;
do not select a canned target-specific report by keyword.

This is a secondary support skill. It does not choose the ontology, define
conceptual worth, or make simulation a mandatory stage of discovery. Return all
results to `reflective-conceptual-discovery` for theoretical interpretation.

Read [references/experiment-contract.md](references/experiment-contract.md)
before designing or running an experiment.

## Entry Gate

Require:

- a stable target, run, branch, theory-programme, conceptual-system, theoretical
  question, and experiment ID;
- an explicit probe role: `formal_support`, `counterexample`, `calibration`,
  `constraint`, or `discrimination`;
- why reflection, conceptual synthesis, or analytic derivation alone cannot
  currently settle the question;
- preregistered outcome implications for every live hypothesis or consequence;
  for `discrimination`, at least two competing predictions over the same
  observable, including a null when useful;
- typed objects, domains, quantifiers, assumptions, invariants, controls, and
  observables;
- the decision that each possible result would change;
- a bounded compute budget and explicit non-claim boundary.

If a proposed discrimination has no distinguishable predictions, return a
preflight `not_identifiable` triage and a reflective-conceptual handoff. If the
theoretical question is not mature enough to supply the required objects and
consequences, return `immature_question`.
If the question is mature but a computation would not change the theory
programme, return `no_probe_needed`. None of these triage decisions is an
execution failure.
If variables or controls are untyped, invoke
`qualitative-variable-isolator` before continuing.

## Theory-First Subordination

- Commission a probe from a theory programme; never generate a theory merely
  because an executable model is available.
- Prefer continued reflection, formal definition, or analytic derivation when
  those can resolve the ambiguity more directly.
- Treat symbolic reasoning used to invent definitions, invariants,
  representations, or formal languages as formative theory work owned by the
  conceptual loop; this skill owns diagnostic symbolic execution.
- Treat simulations as model-scoped support. They may calibrate, constrain,
  illustrate, support, or disconfirm a mechanism in a declared regime, but they
  cannot select the foundational ontology or establish an unbounded theorem.

## Mathematical Invariants

- Mathematical objects: live propositions or mechanisms, their typed carriers,
  variables, observables, controls, regimes, assumptions, predictions, and
  transfer maps.
- Preserved invariants: target and branch identity, quantifier order, domain
  membership, units or scaling, held-fixed controls, solver assumptions,
  preregistered decision rules, and the declared model-to-target boundary.
- Broken invariants: hidden parameter coupling, changed observable, target proxy
  substitution, unrecorded approximation, post-hoc threshold, invalid witness,
  or a finite/model result presented as an unbounded theorem.
- Boundary regimes and counterexamples are first-class results; state when a
  claimed mechanism disappears, reverses, or becomes unidentified.

## Choose The Experiment Mode

Select the cheapest adequate mode or ordered sequence of modes:

1. `exact_symbolic`: algebraic reduction, exact rational arithmetic,
   satisfiability, finite enumeration, recurrence solving, invariant checking,
   or a proof assistant over the actual proposition;
2. `bounded_model`: exhaustive or adversarial search over a declared finite
   carrier to find witnesses or countermodels;
3. `numerical_simulation`: controlled integration, sampling, optimization, or
   finite-volume approximation with tolerances and uncertainty estimates;
4. `parameter_sweep`: regime, sensitivity, threshold, or bifurcation mapping;
5. `hybrid`: two or more declared stages—for example bounded enumeration
   followed by exact witness verification, or symbolic constraint derivation
   followed by numerical evaluation—with every evidence class reported
   separately.

Prefer analytic or exact methods when feasible. Use domain-specific auditors,
including `pvsnp-symbolic-complexity-auditor` or
`routea-symbolic-cas-auditor`, only when their mathematical contract exactly
matches the live experiment. A script's availability is not a reason to distort
the question to fit it.

## Workflow

### 1. Compile outcome implications and rival predictions

Translate every live hypothesis or formal consequence into observable outcome
implications over the same carrier, regime, controls, and measurement rule. For
discrimination, compare rival predictions explicitly. Define in advance which
result favors, weakens, falsifies, constrains, or fails to distinguish each live
item. Do not invent the decision rule after seeing results. Preregister mutually
exclusive, collectively exhaustive outcome regions; include an explicit
`inconclusive` catch-all when exhaustive substantive regions cannot be proven.

### 2. Specify the mathematical model

State equations, initial and boundary conditions, constraints, units or scaling,
parameter domains, quantifier order, random variables, observables, and transfer
assumptions. Record which target invariants the model preserves and which it
deliberately breaks.

Use `efficient-representation-requirements-elicitor`,
`physics-regime-map-builder`, `monotonicity-sensitivity-prober`, or
`scale-asymptotic-reasoner` when the representation or regime needs refinement.
Use `qualitative-toy-model-builder` when the smallest faithful carrier is not
yet known.

### 3. Build a replayable run

Create a branch-scoped experiment directory rather than a shared `latest` file.
Persist the specification, executable source or exact command, environment and
dependency versions, inputs, seed policy, budget, tolerances, and canonical
input digest before execution. Keep generated outputs separate from the source
specification.

For stochastic runs, use declared seeds and enough independent repetitions to
meet a preregistered precision, power, or sequential-stopping rule. State the
estimand, sampling unit, independence assumptions, RNG algorithm and seed
derivation, censoring and missing-run policy, uncertainty method, and
multiple-comparison policy. Check burn-in, convergence, discretization, and
integrator bias when they apply. For deterministic runs, record exact arithmetic
and solver settings. For proof assistants, compile the actual conjecture or negation; a
generic enumerator that merely emits theorem-shaped strings is ideation, not a
certificate.

For bounded exact search, declare the carrier ordering, parameter bounds,
enumerator completeness, symmetry reduction, minimality order, and an exact
witness verifier. Report `no_witness_in_declared_carrier` separately from proof
of nonexistence. Claims such as “smallest counterexample” require exhaustive
verification of every preceding case in the declared ordering.

### 4. Execute and inspect

Run the bounded experiment, capture exit status, stdout, stderr, runtime,
resource use when relevant, result files, and output digest. Inspect the actual
outputs before interpretation. If execution is unavailable or exceeds budget,
return `execution_status: not_executed` or
`execution_status: resource_limited`, not simulated evidence.

### 5. Run controls and adversarial variants

Include when applicable:

- the baseline;
- a mechanism-knockout or null variant;
- at least one boundary or negative-control case;
- sensitivity to important parameters, tolerances, seeds, discretization, or
  solver choices;
- a known-answer calibration when available.

Mark any inapplicable control explicitly with a mathematical rationale. Do not
invent a meaningless knockout or sensitivity analysis merely to fill a field.

Use `counterexample-hunter`, `counterfactual-route-prober`,
`proof-creative-variant-prober`, or the Gedanken skills to design adversarial
variants. Keep their conceptual outputs distinct from executed evidence.

### 6. Interpret against preregistered predictions

Record execution, validity, identifiability, applicability, and scientific
results on separate axes. Scientific results may contain more than one item,
especially for hybrid experiments. Use these result kinds:

- `certificate`: replayable exact proof, unsat core, or verified identity;
- `counterexample`: concrete witness falsifying a universal or route claim;
- `mechanism_supported_in_model`: controls discriminate in the bounded model;
- `mechanism_disconfirmed_in_model`: predicted discrimination fails or reverses;
- `region_narrowed`: valid constraints shrink a parameter or regime set;
- `inconclusive`: rivals make the same prediction or uncertainty dominates.

Represent model, execution, control, or provenance failure with
`validity_status: invalid`, not as a scientific result.

Numeric agreement and finite enumeration do not prove an unbounded theorem.
Symbolic simplification is valid only under its recorded assumptions. Report
model evidence, transfer evidence, and theorem evidence separately.

### 7. Emit an evidence handoff

For a commissioned probe, return the experiment packet and execution receipt defined in
[references/experiment-contract.md](references/experiment-contract.md). Link
each conclusion to a result or certificate ID and state the exact hypothesis
or conceptual-system revision the reflective loop should consider. This skill
does not perform the durable theory or branch transition.

When wrapping a specialist skill, the specialist owns carrier design and domain
interpretation. This skill owns preregistration, executable-run provenance,
artifact normalization, and evidence packaging. Specialist branch dispositions
remain recommendations to the concept-discovery reducer.

## Output Contract

Return the probe triage defined in
[references/experiment-contract.md](references/experiment-contract.md). Only a
`commissioned` decision creates an immutable experiment specification and one
receipt per execution attempt. For commissioned work, include typed artifact
records, digest semantics, stage results, exact verifier or statistical
analysis, controls and waivers, uncertainty and sensitivity, prediction
comparison, transfer boundary, affected hypothesis IDs, permitted
theory-assimilation recommendations, forbidden claims, and explicit unknowns.
Include executed commands and artifact paths when a run occurs; otherwise
report `not_executed` or `resource_limited` on the execution axis and any
post-run non-identifiability on the identifiability axis. Preflight
`not_identifiable`, `no_probe_needed`, and `immature_question` are valid
theory-support triage decisions and require neither an experiment specification
nor a synthetic execution receipt.

## Epistemic Discipline

Assign an epistemic status on each independent axis. Distinguish designed,
executed, valid, invalid, current, stale, certificate,
counterexample, supported-in-model, disconfirmed-in-model, region-narrowed,
inconclusive, and explicit-unknown statuses. Cite specification, receipt,
result, verifier, evidence, and artifact IDs for every interpretation. Preserve
a historically valid result when later concept revision makes it stale or
inapplicable; do not rewrite it as invalid.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md`. Execute only the preregistered,
bounded command or solver configuration; capture the command, environment,
outputs, and status in the receipt; inspect artifacts before interpreting them;
and run the declared verifier or analysis. A designed computation or a solver
failure is not experiment evidence.

## Reuse Before Invention

Compose existing skills where they already solve a subproblem:

- typing and regimes: `qualitative-variable-isolator`,
  `physics-regime-map-builder`, `scale-asymptotic-reasoner`;
- small carriers: `qualitative-toy-model-builder`;
- adversarial design: `counterexample-hunter`,
  `counterfactual-route-prober`, `proof-creative-variant-prober`;
- target-specific exact checks: `pvsnp-symbolic-complexity-auditor`,
  `routea-symbolic-cas-auditor`;
- follow-up selection: `next-experiment-queue-ranker`.

Introduce new code only for the live model, solver adapter, or experiment family
that these skills cannot express. Keep that code generic when the same contract
applies across targets.

## Failure/Demotion

Invalidate the result on stale state, mismatched target or branch identity,
unrecorded assumptions, hidden parameter coupling, absent controls, digest
mismatch, post-hoc decision rules, unreplayable output, or proxy-target drift.
Preserve null and negative results as evidence. Never label a failed execution
as a falsified hypothesis.

## Validation Handoff

End with the experiment status, receipt and artifact paths, hypothesis IDs
and conceptual-system IDs affected, transfer boundary, independent validator or
critic required, and the exact reflective-assimilation question. Recommend
another experiment only when theory still requests one.
