---
name: ym-define-relational-rigidity
description: Define and audit regulator-independent infrared rigidity witnesses for constructive Yang--Mills work. Use when translating cutoff correlation decay, transfer-operator estimates, or RG contraction into a candidate physical mass-gap statement, especially when cutoff, volume, observable, normalization, and uniformity quantifiers must be made explicit.
---

## Abducer Integration Guards

- Activate this skill only for `yang-mills-existence-and-mass-gap-target` or an explicitly marked Yang-Mills calibration task.
- Treat imported representational-dynamics artifacts as restricted, finite, conditional, or support evidence unless a later proof discharges their frontier hypotheses.
- Emit claim level, non-claims, hard gate, hypotheses, falsifier, and demotion trigger before any promotion.
- Compose with the target-neutral proof-depth skills: pressure formalization, hard-gate selection, nontriviality audit, anti-definitionality audit, same-domain transfer certification, and declarative learning extraction.
- State efficient representation requirements: preserved observables, morphisms or recovery maps, invariants, error budgets, equivalence policy, locality or cutoff budget, transfer interface, and falsifiers.
- Do not let a transfer theorem pass if the target property is built into the bridge definition; require independently stated source and target objects plus a consequence delta.
- Preserve the four-cycle, recursion-depth-one publication-consolidation limit for local subgoals.
- Source provenance: `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-define-relational-rigidity/SKILL.md`.

## Mathematical Invariants

Preserve the Yang--Mills mathematical object: compact simple gauge group, pure gauge content, gauge-invariant observable algebra, regulator/cutoff/volume/coupling regime, reflection positivity, locality, OS reconstruction route, continuum limit order, and Hamiltonian spectral target. Any representation, morphism, RG step, or restricted model must state which invariants are preserved, which error budgets are allowed, and which edge case or counterexample would break transfer.

## Epistemic Discipline

Every output must state epistemic status, claim level, evidence citation, source artifacts, explicit unknowns, and validation handoff. Treat physical relevance, literature-gap warrant, and frontier comparison as hard gates; unsupported implications stay conditional, blocked, or `requires_prior_art`.

## Failure/Demotion

Demote or quarantine if the skill assumes a mass gap, clustering, confinement, continuum existence, regulator independence, positivity, locality, observable density, or theory identity instead of proving it. Disconfirming evidence, prior-art collision, target-equivalent bridge definitions, or missing counterexample tests block promotion to a major YM publication pathway.

# Define Relational Rigidity

## Objective

Formulate a noncircular property that can be verified at regulated scales and transferred across representations without already assuming a continuum mass gap. Treat rigidity as a family of quantitative relations among physical observables, states, scales, and representation maps.

## Required Inputs

- A regulator family indexed by cutoff `a`, volume `L`, and bare or running parameters.
- A specified gauge-invariant observable class and its physical normalization.
- The relevant physical distance or Euclidean time variable.
- The representation maps that compare scales or regulators.
- A declared target: clustering, transfer-spectrum exclusion, or Hamiltonian spectral exclusion.

## Workflow

1. Write every quantifier in the order actually needed: observable, cutoff, volume, separation, and limiting sequence.
2. Express decay rates in physical units. Never infer a continuum gap from a positive number measured only in lattice units.
3. Separate temporal correlation estimates, spatial clustering, transfer-operator estimates, and auxiliary stochastic mixing estimates.
4. State which observables separate the reconstructed physical Hilbert space. If they do not, label the witness sectorial.
5. Require constants and prefactors to be uniform in volume and sufficiently small cutoff after renormalized normalization.
6. Record stability under the approved representation morphisms, including accumulated approximation errors.
7. Test the definition against the false-positive bank before using it in a theorem.

## Canonical Witness

A useful template is uniform physical relational rigidity: there exist physical constants `m>0`, `a_0>0`, and controlled seminorms `N_a` such that for all `a<a_0`, all sufficiently large volumes, and all centered observables in a state-separating class,

`|<A tau_t(B)>_c| <= C N_a(A) N_a(B) exp(-m t) + epsilon_a(A,B,t)`,

where `t` is physical Euclidean time, the prefactor is uniform in volume, and the error vanishes in the declared continuum topology. Specify whether the estimate is pointwise, distributional, or smeared.

## False-Positive Tests

- **Finite-volume discreteness:** a finite box has a discrete spectrum even when the infinite-volume theory is gapless.
- **Lattice-unit collapse:** a cutoff gap `delta_a` with `delta_a/a -> 0` does not produce a positive physical gap.
- **Incomplete observables:** exponential decay in one sector can hide a gapless orthogonal sector.
- **Stochastic confusion:** a Poincare or log-Sobolev gap for a sampling dynamics is not automatically the quantum Hamiltonian gap.
- **Circular clustering:** a basin or rigidity definition that assumes the desired physical exponential clustering proves nothing new.
- **Uncontrolled prefactors:** exponentially growing constants can destroy the claimed decay after limits.

## Output Contract

Return:

- the exact rigidity predicate with all parameters and quantifiers;
- the observable-completeness requirement;
- physical-unit normalization;
- allowed morphisms and error budgets;
- the false-positive tests passed or failed;
- the strongest justified claim level.

Do not call the witness a Yang--Mills mass gap until continuum existence, Osterwalder--Schrader reconstruction, and physical-state completeness have also been established.
