<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Empirical Evidence Requests

- Target: `yang-mills-existence-and-mass-gap-target`
- Source: `agentic/reports/yang_mills_bridge_lemma_packets/latest.json`
- Requests: 4

## empirical-evidence.74577176e712

- Mode: `empirical_probe`
- Proximity: `continuum-extrapolated-regulated-evidence`
- Linked step: Attach one non-Gaussian gauge-invariant observable witness to rule out triviality.
- Observable or quantity: Wilson-loop area law, string tension, or connected gauge-invariant cumulants

### Empirical Question

Do lattice Yang-Mills simulations or continuum-extrapolated analyses show gauge-invariant Wilson-loop area-law behavior, string tension, or connected cumulants that can guide a same-theory nontriviality witness?

### Search Plan
- Search for lattice Yang-Mills Wilson-loop/string-tension studies with continuum extrapolation or controlled scaling.
- Extract which gauge group, dimension, action, observable normalization, and cutoff/volume controls are used.
- Record whether the observable could become a same-theory nontriviality witness after OS/continuum reconstruction.

### Support Criteria
- Evidence concerns four-dimensional compact simple gauge Yang-Mills or a clearly marked regulated approximation.
- The observable is gauge invariant and connected to a continuum-extrapolated scale.
- The result suggests a nonzero interacting gauge-invariant witness rather than a Gaussian/free collapse.

### Refutation Criteria
- Evidence is only fixed cutoff, finite volume, or non-gauge-invariant.
- The measured signal disappears under continuum extrapolation.
- The source concerns a different theory without an explicit transfer argument.

Transfer gap: A theorem must still show that the selected observable belongs to the same limiting Schwinger family used for OS reconstruction and that its connected cumulant survives cutoff removal.

Proof boundary: Proof boundary: Wilson-loop or string-tension evidence can select and prioritize a nontriviality witness, but it is not proof of continuum nontriviality.

Integration action: If supportive, add a nontriviality-witness evidence task and keep it behind the RG-to-OS same-theory gate.

## empirical-evidence.c4be5d826738

- Mode: `empirical_probe`
- Proximity: `continuum-extrapolated-regulated-evidence`
- Linked step: Prove decay constants stay bounded below through cutoff removal.
- Observable or quantity: Gauge-invariant glueball correlator decay, mass ratios, and spectral scale estimates

### Empirical Question

Do lattice glueball correlator or mass-spectrum studies provide continuum-extrapolated evidence for positive gauge-invariant mass scales compatible with Euclidean correlator decay?

### Search Plan
- Search for glueball spectrum and Euclidean correlator decay studies in four-dimensional pure Yang-Mills lattice gauge theory.
- Extract continuum extrapolation, finite-size scaling, gauge group, observable family, and mass-scale uncertainty.
- Record whether the evidence supports a candidate observable family for the decay-to-gap bridge.

### Support Criteria
- The study estimates a positive mass scale from gauge-invariant correlators.
- The source reports continuum extrapolation or scaling checks.
- The observable family is close to the one needed for OS spectral reconstruction.

### Refutation Criteria
- Mass estimates vanish or become unstable under continuum extrapolation.
- The observable is gauge-fixed or not gauge invariant without a transfer argument.
- Only strong-coupling or fixed-lattice-spacing evidence is available.

Transfer gap: A proof must still turn the regulated correlator evidence into a cutoff-uniform bound for the same continuum Schwinger functions and show the observable family is spectrally determining in P_perp H_YM.

Proof boundary: Proof boundary: positive lattice glueball masses guide the decay route, but they are not proof of E_H((0,m0))P_perp=0.

Integration action: If supportive, prioritize the cutoff-uniform decay and observable-density proof obligations.

## empirical-evidence.476e50f9a041

- Mode: `source_import`
- Proximity: `regulated-approximation`
- Linked step: Prove the limiting topology preserves OS positivity for the gauge-invariant observable sector.
- Observable or quantity: Reflection-positive lattice action, transfer matrix, and Schwinger-function positivity tests

### Empirical Question

Which reflection-positive lattice gauge actions, transfer-matrix constructions, or numerical practice constraints are close enough to inform the OS-positivity preservation obligation?

### Search Plan
- Search for reflection positivity and transfer-matrix results for lattice gauge theories.
- Separate rigorous source theorems from empirical/numerical practice.
- Extract conditions on action, gauge group, observable algebra, and limiting topology.

### Support Criteria
- The source states reflection positivity for gauge-invariant lattice observables.
- The construction is compatible with compact simple gauge groups.
- The result identifies what topology or algebra is needed for a limiting OS argument.

### Refutation Criteria
- The action used by the target route is not reflection positive.
- The transfer matrix applies only after gauge fixing that changes observables.
- No limiting closedness result can be stated.

Transfer gap: A closure theorem is still needed before regulated reflection positivity implies OS positivity of the continuum Schwinger functions.

Proof boundary: Proof boundary: reflection-positive lattice practice can supply source conditions, but the continuum OS theorem remains a mathematical proof obligation.

Integration action: If supportive, import theorem statements and sharpen the OS-positivity-failure reductio conflict target.

## empirical-evidence.319435953ed2

- Mode: `negative_evidence`
- Proximity: `continuum-extrapolated-regulated-evidence`
- Linked step: Transport the cutoff-uniform decay estimate to the continuum without changing the object.
- Observable or quantity: Cutoff dependence of correlator decay rates and finite-size scaling of mass estimates

### Empirical Question

Are there lattice, numerical, or prior-art warnings that apparent mass scales or correlator decay constants degenerate under continuum extrapolation, finite-size scaling, or observable-sector changes?

### Search Plan
- Search specifically for failures, systematic uncertainties, and continuum-extrapolation caveats in mass-gap-related lattice studies.
- Record whether finite-size effects, topology freezing, gauge fixing, or scale setting could invalidate a naive decay-to-gap inference.
- Use findings as demotion tests for the no-gap spectral reductio and decay-to-gap bridge.

### Support Criteria
- Evidence identifies concrete conditions required to keep decay constants stable.
- Known failure modes can be translated into proof obligations or demotion triggers.
- The evidence refines the search without replacing the theorem.

### Refutation Criteria
- The evidence shows all close decay estimates are fixed-cutoff artifacts.
- Continuum extrapolation destroys the positive lower bound.
- Observable-sector changes make the spectral interpretation invalid.

Transfer gap: Even negative empirical evidence must be translated into mathematical boundary regimes before it can refute a proof route.

Proof boundary: Proof boundary: numerical instability can demote or reprioritize a route; it is not proof against the mathematical target by itself.

Integration action: If negative evidence is strong, pivot toward construction/nontriviality or revise the observable family.
