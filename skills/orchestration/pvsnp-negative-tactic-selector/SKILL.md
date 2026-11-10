---
name: pvsnp-negative-tactic-selector
description: Select proof-by-contradiction, impossibility/no-go theorem, falsifier search, constructive bridge, backtrack, quarantine, or stop tactics for P vs NP discovery branches. Use when a P vs NP branch needs controlled negative reasoning, route-specific barrier handling, publishable stepping-stone triage, or a decision about whether to persist, pivot, or turn a stable obstruction into a theorem-shaped no-go result.
---

# P vs NP Negative Tactic Selector

## Role

Use this orchestration skill before P vs NP contradiction, falsifier, or no-go work. Its job is not to be pessimistic. Its job is to decide the correct logic form for the next branch move.

The selector must preserve the exact target: `P != NP` or the nonuniform target `NP not subset P/poly`, with named source object, target class, circuit/proof model, quantifier order, advice status, oracle/algebraic status, and reduction interface.

## Decision Procedure

1. **Localize the pressure.**
   Name the active difficulty as one of: transfer loss, all-exponent quantifier loss, padding/projection debt, advice leakage, natural-property pressure, relativization/algebrization signature, proof-complexity transfer gap, MCSP/MKtP carrier gap, or restricted-model proxy drift.

2. **Ask whether the pressure is computable.**
   If the branch has parameters such as `beta`, `q`, padding exponent, query length, constructivity, largeness, advice bits, oracle access, verifier overhead, or source lower-bound exponent, send it through symbolic or qualitative audit before a broad no-go claim.

3. **Choose proof by contradiction when the negation is structured.**
   Use reductio only when the negated subclaim generates a carrier such as small SAT circuits, a low-support sketch, short proof family, easy MCSP row, oracle-respecting simulation, advice selector, or transfer inequality that conflicts with a named theorem or accepted branch invariant.

4. **Choose impossibility/no-go theorem formation when the route family stabilizes.**
   Use this when repeated repairs expose the same method class with stable parameters and escape conditions. The theorem must have hypotheses, conclusion, proof skeleton, examples covered, examples not covered, and non-claim boundary.

5. **Choose falsifier search when a finite or symbolic failure mode is visible.**
   Search for advice leakage, easy restricted-model witnesses, bounded exponent windows, Gaussian-elimination shortcuts, large constructive useful properties, sparse valid-length traps, or easy truth-table families.

6. **Stay constructive when a genuine escape remains.**
   Do not demote a branch that still has a target-preserving escape condition such as `beta=0`, subpolynomial target queries, genuinely nonblackbox SAT-circuit use, non-large/nonconstructive property, advice-free row-hard certificate, or a typed restricted-to-unrestricted compiler.

7. **Backtrack or quarantine only with route-specific evidence.**
   Quarantine when two sharpened attempts cannot name the source object, target class, transfer inequality, conflict target, barrier status, and escape condition. Do not quarantine merely because the route is hard.

## Epistemic Discipline

Every selected tactic must state its epistemic status: constructive escape still open, proof-obligation exposed, contradiction carrier validated, no-go theorem candidate, falsifier candidate, blocked, quarantined, or stop-ready. Do not treat a negative tactic as a proof of `P != NP`. It is a branch-control judgment over a local method class or subclaim.

Evidence must cite source artifacts, branch ids, cycle ids, transfer inequalities, barrier hypotheses, symbolic audits, or prior-art checks. If the evidence only says that P vs NP is hard, the tactic is underspecified. If a route is demoted, preserve the disconfirming calculation or demotion reason so later cycles do not rediscover the same failed pressure.

## Route Family Matrix

- **Black-box substitution or hardness magnification.**
  Prefer contradiction if a branch asserts all-exponent transfer despite positive target-query exponent `beta`; derive the transferred upper bound `N^{q+beta c+o(1)}` from `SAT in SIZE(n^c)`. Prefer no-go theorem if several carriers share the same positive-`beta` interface. Preserve escapes: `beta=0`, subpolynomial queries, or nonblackbox circuit use.

- **Padding/projection or sparse valid-length carrier.**
  Prefer contradiction when a weak source lower bound is claimed to imply `NP not subset P/poly`; assume small SAT circuits and compute the padded source upper bound. Prefer no-go theorem when the route collapses to a bounded exponent window or to sparse-valid-length hardness equivalent to the target. Preserve nonprojection compression escapes.

- **Natural property or combinatorial lower-bound route.**
  Prefer contradiction when constructivity, largeness, usefulness, and cryptographic hardness are asserted together for the exact circuit class. Prefer no-go theorem when all route variants depend on large constructive useful properties. Preserve non-large, nonconstructive, semantic, or proof-system-specific escapes.

- **MCSP/MKtP or meta-complexity carrier.**
  Prefer contradiction when row hardness or certificate selection leaks advice. Prefer no-go theorem when repeated variants require advice-free row selection that the route cannot provide. Preserve explicit advice-free row-hard certificates, non-natural density control, and verifier-overhead improvements.

- **Proof-complexity transfer.**
  Prefer contradiction when a proof family admits a shortcut such as Gaussian elimination, recognition, semantic bypass, or restricted-model collapse. Prefer no-go theorem when proof length lower bounds cannot connect to SAT circuit lower bounds without an unproved semantic bridge. Preserve explicitly typed proof-system transfer theorems.

## Output Contract

Return a `negative_tactic_decision` packet with:

- `tactic_mode`: `constructive_bridge`, `proof_by_contradiction`, `impossibility_theorem`, `falsifier_search`, `backtrack`, `quarantine`, or `stop`.
- `route_family`: one of the route families above, or a more specific branch-local family.
- `reason_for_tactic`: why this logic form is justified now.
- `exact_negation_or_method_class`: the local negated subclaim or method class, not global "assume P=NP" rhetoric.
- `contradiction_carrier_or_no_go_family`: the object that carries the contradiction, falsifier, or no-go theorem.
- `conflict_target`: accepted theorem, transfer inequality, barrier premise, or validated branch invariant.
- `escape_conditions`: target-preserving variants not ruled out.
- `proof_obligations`: exact calculations, definitions, prior-art checks, or symbolic audits still needed.
- `branch_control_decision`: persist, adapt, backtrack, pivot, quarantine, or stop.
- `next_validation_handoff`: next skill, validator, calculation, or report panel.
- `paper_contribution_potential`: whether this could become a publishable stepping-stone, and what would make it good enough.

## Guardrails

- Reject global contradiction rhetoric unless the negation has a local carrier and accepted conflict target.
- Reject generic barrier labels unless the barrier hypothesis is typed for the branch.
- Preserve escape conditions explicitly; a no-go theorem is useful because it is scoped.
- Keep constructive work alive when an untested escape condition remains computable.
- Treat a scoped no-go theorem as potential scientific progress, not as failure, when it clarifies a method family and unblocks route choice.

## Handoffs

- Send parameter algebra to `pvsnp-symbolic-complexity-auditor`.
- Send variable/regime interpretation to `pvsnp-qualitative-complexity-reasoner`.
- Send theorem-shaped no-go candidates to `pvsnp-impossibility-theorem-forger` and `contradiction-route-auditor`.
- Send publishable stepping-stone candidates to `scientific-contribution-detector` and `paper-contribution-readiness-judge`.
- Send queue decisions to `next-experiment-queue-ranker` and the discovery marathon scheduler.

## Codex Exec Protocol

When used in the local workflow, run the deterministic packet builder and validator before interpreting the tactic generatively:

```bash
python agentic/scripts/build_pvsnp_negative_tactic_packet.py
python agentic/scripts/validate_pvsnp_negative_tactics.py
```

Then inspect `agentic/reports/pvsnp_negative_tactics/latest.json` and use Codex execution results to decide whether the next branch should compute a transfer, prove a scoped impossibility theorem, search for a falsifier, backtrack, quarantine, or continue constructively. The generative step should explain the artifact, not bypass it.
