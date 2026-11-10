---
name: pvsnp-gedanken-complexity-lab
description: Design concrete P vs NP Gedanken experiments and extract essential conclusions. Use when a P vs NP branch, bridge candidate, pressure report, or marathon cycle needs a small complexity-theoretic situation that elicits fundamental intuition about oracle substitution, beta/exponent windows, MCSP or MKtP certificates, proof-complexity carriers, natural-proof pressure, advice leakage, padding/projection debt, all-exponent quantifiers, or no-go route boundaries.
---

# P vs NP Gedanken Complexity Lab

## Conceptual Role

Use this skill to build the P vs NP equivalent of a Gedanken experiment: a concrete, controlled complexity-theoretic world that makes a hidden mechanism visible. The output is not a metaphor and not a proof. It is a test bench for intuition that later cycles can turn into a derivation, exact symbolic audit, no-go theorem, literature check, or queue decision.

The skill must always extract essential conclusions. The point of the imagined case is to learn what survives, what fails, what condition is decisive, and what exact next action should follow.

## Procedure

1. **Start from a live pressure or bridge.**
   Use a branch blocker, bridge candidate, queue item, symbolic audit, or pressure report. Do not design a generic SAT example. Name the active pressure: `black_box_substitution_cap`, `meta_complexity_carrier_debt`, `naturalness_density_pressure`, `proof_complexity_transfer_gap`, `padding_projection_debt`, `advice_uniformity_leakage`, or `all_exponent_quantifier_gap`.

2. **Choose the minimal world.**
   Use one of these carriers when appropriate:
   - SAT-oracle circuit with `q` queries of length `N^beta`;
   - finite truth-table carrier with explicit or advised selector;
   - searchable MCSP/MKtP certificate system `(V,D)`;
   - sparse truth-table property with largeness/constructivity/usefulness toggles;
   - proof-system tautology `LB(u,s)` with verifier and proof-length knobs;
   - padding/projection family `N=n^k`;
   - method-class world for an impossibility theorem.

3. **Isolate variables and held-fixed conditions.**
   Name `n`, `N`, `c`, `epsilon`, `q`, `beta`, `kappa`, certificate length, verifier time, density, constructivity, advice bits, proof length, valid-length coverage, and target class. Mark which variable is varied and which assumptions stay fixed.

4. **Specify the controlled contrast.**
   Compare two nearby worlds that differ in exactly one decisive condition, such as `beta>0` versus `beta=0`, advised hard string versus searchable certificate, dense constructive property versus sparse property, fixed exponent versus all-exponent family, or semantic lower bound versus proof-system lower bound.

5. **Predict the observation and counterfactual variant.**
   State what should happen, what would disconfirm it, and which variant should change the conclusion. If no variant changes anything important, the experiment is too vague.

6. **Extract essential conclusions.**
   For each experiment, write the decisive intuition, formal lesson, route-control consequence, and exact next computation, derivation, no-go theorem, or quarantine condition.

7. **Emit a valid packet.**
   Produce a packet compatible with `agentic/spec/gedanken_experiment_packet.schema.json`, including transfer scope, follow-up tasks, graph update action, and validation command.

## P vs NP Experiment Families

- **Black-box substitution microscope.** Minimal world: source carrier `L_N`, oracle circuit overhead `q`, target query length `N^beta`, hypothetical SAT circuits `m^c`. Essential conclusion: positive `beta` converts a fixed source margin into a bounded exponent window; a direct proof route must remove or transform the `beta*c` term.
- **Searchable certificate contrast.** Minimal world: a verifier-decoder pair `(V,D)` for high MCSP/MKtP truth tables. Contrast advised hard strings with uniformly searchable certificates. Essential conclusion: the branch lives or dies on compact sound certificates with bounded gap coverage and no advice leakage.
- **Sparse non-natural property switch.** Minimal world: a truth-table property with toggles for density, constructivity, usefulness, and PRF-compatible circuit class. Essential conclusion: saying "non-natural" is empty unless the exact failed natural-proof premise and surviving usefulness implication are named.
- **All-exponent quantifier lift.** Minimal world: a family indexed by target exponent `c`. Essential conclusion: fixed-window progress is not `NP not subset P/poly`; the route needs a cofinal parameter family or should become a no-go theorem.
- **Proof-complexity certificate bench.** Minimal world: lower-bound tautologies `LB(u,s)` in a named proof system. Essential conclusion: proof objects help only if they verify semantic circuit lower bounds without demanding proof lower bounds as hard as the target.

## Mathematical Invariants

- Mathematical object: thought-experiment carrier, variables, controlled contrast, target class, proof obligation, disconfirming observation, extracted conclusion, and transfer certificate.
- Preserved invariants: source/target model identity, input-length map, quantifier order, uniform/nonuniform status, advice accounting, barrier status, and target/proxy distinction.
- Broken invariants: finite toy enumeration presented as lower-bound evidence, fixed-exponent intuition promoted to all-polynomial separation, advised selection mistaken for uniform construction, or a natural-proof escape asserted without density/constructivity/usefulness checks.
- Edge case or counterexample: include a variant that flips `beta`, advice, density, certificate length, proof length, padding exponent, or valid-length coverage.

## Epistemic Discipline

Assign epistemic status: `conceptual_probe`, `conjectural`, `validated_probe`, `proof_obligation`, `invalidated`, or `explicit_unknown`. Cite bridge IDs, cycle IDs, KB IDs, symbolic audits, pressure reports, or explicit unknowns. Do not treat an imagined observation as evidence until a follow-up derivation or computation supports it.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when execution can ground the packet. Use `scripts/build_pvsnp_gedanken_packets.py` or the general `agentic/scripts/build_gedanken_experiment_packets.py --target p-vs-np-target`, inspect the generated JSON and Markdown, then interpret the essential conclusions.

Example:

```bash
python skills/reasoning/pvsnp-gedanken-complexity-lab/scripts/build_pvsnp_gedanken_packets.py
python agentic/scripts/validate_pvsnp_gedanken_conclusions.py
python agentic/scripts/validate_gedanken_experiment_packets.py
```

## Output Contract

Return:

1. `Pressure Or Bridge Source`: bridge ID, cycle ID, or pressure type.
2. `Concrete Situation`: minimal world, carrier, controlled contrast, and why it is informative.
3. `Variables And Controls`: varied variable, held-fixed assumptions, validity regime.
4. `Expected Observation`: pattern, what it teaches, and disconfirming observation.
5. `Variant`: single-condition counterfactual and predicted change.
6. `Essential Conclusions`: decisive intuition, formal lesson, route-control consequence, and next action.
7. `Transfer Scope`: what transfers, what does not, and certificate needed.
8. `Follow-Up`: derive, compute, falsify, formalize, update graph, rank next experiment, backtrack, or quarantine.

## Failure/Demotion

Demote if the experiment is only an analogy, if it lacks a branch-specific variable, if the conclusion is not actionable, if no variant changes the result, or if it cannot name a transfer certificate. Quarantine if it solves a different problem or promotes intuition as proof.

## Validation Handoff

Validate with `agentic/scripts/validate_pvsnp_gedanken_conclusions.py` and `agentic/scripts/validate_gedanken_experiment_packets.py`. Hand exponent-shaped conclusions to `pvsnp-symbolic-complexity-auditor`, no-go conclusions to `pvsnp-impossibility-theorem-forger`, and bridge revisions to `pvsnp-pressure-bridge-forger`.
