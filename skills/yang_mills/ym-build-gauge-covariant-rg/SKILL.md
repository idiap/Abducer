---
name: ym-build-gauge-covariant-rg
description: Design and audit renormalization-group transformations for constructive Yang--Mills theory that respect gauge-invariant observables and track locality, positivity, running couplings, and reconstruction data. Use when a proof needs a typed scale transformation rather than a formal perturbative beta function alone.
---

## Abducer Integration Guards

- Activate this skill only for `yang-mills-existence-and-mass-gap-target` or an explicitly marked Yang-Mills calibration task.
- Treat imported representational-dynamics artifacts as restricted, finite, conditional, or support evidence unless a later proof discharges their frontier hypotheses.
- Emit claim level, non-claims, hard gate, hypotheses, falsifier, and demotion trigger before any promotion.
- Compose with the target-neutral proof-depth skills: pressure formalization, hard-gate selection, nontriviality audit, anti-definitionality audit, same-domain transfer certification, and declarative learning extraction.
- State efficient representation requirements: preserved observables, morphisms or recovery maps, invariants, error budgets, equivalence policy, locality or cutoff budget, transfer interface, and falsifiers.
- Do not let a transfer theorem pass if the target property is built into the bridge definition; require independently stated source and target objects plus a consequence delta.
- Preserve the four-cycle, recursion-depth-one publication-consolidation limit for local subgoals.
- Source provenance: `agentic/external/yang_mills_representational_dynamics/2026-07-20/skill_bundle/11_vscode_codex_skill_bundle/.agents/skills/ym-build-gauge-covariant-rg/SKILL.md`.

## Mathematical Invariants

Preserve the Yang--Mills mathematical object: compact simple gauge group, pure gauge content, gauge-invariant observable algebra, regulator/cutoff/volume/coupling regime, reflection positivity, locality, OS reconstruction route, continuum limit order, and Hamiltonian spectral target. Any representation, morphism, RG step, or restricted model must state which invariants are preserved, which error budgets are allowed, and which edge case or counterexample would break transfer.

## Epistemic Discipline

Every output must state epistemic status, claim level, evidence citation, source artifacts, explicit unknowns, and validation handoff. Treat physical relevance, literature-gap warrant, and frontier comparison as hard gates; unsupported implications stay conditional, blocked, or `requires_prior_art`.

## Failure/Demotion

Demote or quarantine if the skill assumes a mass gap, clustering, confinement, continuum existence, regulator independence, positivity, locality, observable density, or theory identity instead of proving it. Disconfirming evidence, prior-art collision, target-equivalent bridge definitions, or missing counterexample tests block promotion to a major YM publication pathway.

# Build Gauge-Covariant RG

## Goal

Construct a scale-change map together with certificates for the physical structures it preserves, approximates, or deliberately forgets. Regard the effective action, observable transport, and state transport as one coupled object.

## Construction Workflow

1. Specify the fine and coarse configuration spaces, gauge groups, boundary conditions, and physical observable algebras.
2. Define the blocking kernel or conditional expectation and prove gauge covariance or formulate it directly on gauge orbits.
3. Derive the coarse effective measure and the dual transport of observables. Do not track the action while leaving observables implicit.
4. Parameterize relevant, marginal, irrelevant, and nonlocal terms with explicit norms and scale factors.
5. Track the running coupling in a declared scheme; separate perturbative control from nonperturbative estimates.
6. Prove locality or quasilocality bounds for the effective interaction uniformly in volume.
7. Track reflection positivity. If a block map does not preserve it, supply a later recovery theorem or mark the OS bridge broken.
8. State reconstruction or comparison maps and quantitative errors for every lossy step.
9. Prove composition laws and error accumulation across many RG steps.

## Minimum Certificate

Every RG morphism must report:

- gauge covariance or orbit-space well-definedness;
- state and observable transport;
- normalization of physical length and energy;
- locality or quasilocality norm;
- positivity status;
- volume dependence;
- coupling flow and remainder bounds;
- reconstruction data and approximation error.

## Failure Modes

- Gauge fixing that ignores Gribov or global orbit information.
- A perturbative flow with no control of the full measure.
- Local estimates restricted to a small-field chart without an exceptional-set theorem.
- Scale-by-scale constants whose product diverges.
- Loss of reflection positivity with no recovery argument.
- Blocking that erases the observables needed for spectral completeness.

## Output Contract

Return the typed RG map, its preservation certificate, effective-interaction norms, recursion inequalities, parameter registry, and unresolved obligations. Label any basin-entry conclusion conditional until large fields, topology, and volume-uniform iteration are controlled.
