<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Visual Conceptualization Packet

Target: `yang-mills-existence-and-mass-gap-target`
Run: `yang-mills-smoke-marathon`
Cycles: `['cycle-0348', 'cycle-0349', 'cycle-0350', 'cycle-0351', 'cycle-0352']`
Conceptualizations: `6`
Quarantined or rejected: `1`

## Core Diagnosis

Visual metaphors are used as property-preservation probes and hypothesis generators, not as proof evidence.

## Route Consequences

- artifact_sprint
- falsifier_sprint
- quarantine
- reframe

## Wilson loop observable

Concept id: `ym.visual.wilson-holonomy-thread`
Status: `hypothesis_seed`
Physical carrier: `Wilson loop / gauge-invariant holonomy observable`

A gauge-invariant Wilson loop records holonomy around a closed contour and can carry same-theory nontriviality through Euclidean observables.

Metaphor family: `fiber`
Metaphor: **Closed threads woven through a gauge fabric**

A closed thread can be pulled through local gauge coordinate changes while the traced holonomy carried by the loop remains the inspectable object.

### Preserved And Distorted Properties

- `invariant` `preserved`: Trace/closed-loop holonomy is gauge invariant. -> The color of a closed thread is unchanged by local frame relabeling.. Closure blocks endpoint gauge-frame dependence.
- `symmetry` `preserved`: Gauge transformations act locally but observables must be invariant. -> The fabric frame can twist without changing the closed thread's recorded color.. The metaphor keeps gauge redundancy distinct from observable content.
- `locality_globality` `preserved`: The loop is nonlocal but built from local link transport. -> A thread accumulates local twists into one closed global trace.. The analogy preserves local-to-global accumulation.
- `order_monotonicity` `absent`: No monotone order is inherent without an area-law or correlation inequality. -> Thread length alone does not order physical strength.. This prevents the image from inventing monotonicity.
- `positivity_sign` `partially_preserved`: Reflection positivity is not automatic for every compressed Wilson construction. -> A visible thread may still fail a mirror-overlap sign test.. The image warns that carrier identity does not settle positivity.
- `limiting_behavior` `partially_preserved`: The observable must survive cutoff and continuum limits. -> Threads must remain identifiable as the fabric mesh is refined.. The image exposes the mesh-refinement survival question but does not prove it.
- `physical_carrier` `preserved`: Gauge-invariant Wilson observable carries the claim. -> The closed thread is the carrier, not the coordinate grid.. The image keeps the observable central.
- `proof_obligation` `preserved`: Show same-theory carrier survival and positivity transfer. -> Prove the thread survives mirror tests and mesh refinement.. The proof obligation is visible as survival under reflection and refinement.

### Distortion Ledger

- The thread image can make gauge invariance look topological only; the actual Wilson observable depends on connection and representation data.
- The image does not supply OS positivity or a mass gap.
- It can hide endpoint/source derivative bookkeeping unless paired with a table artifact.

### Hypothesis Inspiration

- `missing_artifact` Build a same-theory Wilson-carrier certificate before any transfer theorem is promoted.
  Route consequence: `artifact_sprint`
  Required artifact: same-theory carrier certificate linking finite reflected Wilson blocks to OS-positive Schwinger candidates
  Falsifier: Find a regulator change where the closed-loop carrier is replaced by a boundary-sector proxy.

Audit verdict: `usable_for_hypothesis_generation`
Allowed route consequence: `same-theory carrier certificate`

Non-claim boundary: The metaphor does not establish an area law, OS positivity, continuum existence, or a positive mass gap.

## Reflection positivity

Concept id: `ym.visual.reflection-positive-mirror-cone`
Status: `hypothesis_seed`
Physical carrier: `OS reflection-positive Schwinger/Wilson observable family`

Reflection positivity requires nonnegative pairings between reflected observables and future observables.

Metaphor family: `tension_field`
Metaphor: **A mirror that only accepts vectors inside a positive cone**

The reflected half-space is a mirror test: only observables whose reflected overlap remains in the positive cone can pass.

### Preserved And Distorted Properties

- `invariant` `preserved`: The positivity condition is invariant under admissible observable reparameterization. -> Cone membership is unchanged by coordinate labels.. The cone is the object, not a coordinate drawing.
- `symmetry` `preserved`: Reflection is an involution. -> The mirror operation flips twice to return the original side.. The involutive structure is directly represented.
- `locality_globality` `preserved`: Half-space localization matters for OS reconstruction. -> Only one side and its reflected partner participate in the mirror test.. The visual split matches time-reflection localization.
- `order_monotonicity` `partially_preserved`: Cone inclusion supports order-like reasoning. -> Moving deeper into the cone makes positivity more robust.. The image is useful only for cone inclusion, not arbitrary monotonicity.
- `positivity_sign` `preserved`: Pairings must be nonnegative. -> The mirror rejects vectors whose reflected overlap points outside the cone.. Sign is the main preserved property.
- `limiting_behavior` `partially_preserved`: Cone closure must survive limit operations. -> A vector near the cone boundary can fall out under projection or limiting motion.. The metaphor highlights endpoint fragility.
- `physical_carrier` `preserved`: OS-positive observables are the reconstruction carrier. -> The vector being tested is the observable family.. The carrier is explicit.
- `proof_obligation` `preserved`: Certify positivity after compression/source aggregation. -> Show the mirror test still accepts the compressed vector.. The exact next proof artifact is visible.

### Distortion Ledger

- A Euclidean cone image can hide the infinite-dimensional functional-analytic closure problem.
- Cone geometry may suggest convexity properties not available for every transformed object.
- It does not justify Schur/Feshbach transfer by itself.

### Hypothesis Inspiration

- `falsifier` Treat every proposed compression as a mirror-cone test before branch promotion.
  Route consequence: `falsifier_sprint`
  Required artifact: finite reflection-positivity interval certificate for the compressed Wilson block
  Falsifier: Exhibit one reflected observable pair whose compressed pairing is negative.

Audit verdict: `usable_for_hypothesis_generation`
Allowed route consequence: `reflection-positivity interval certificate`

Non-claim boundary: The mirror-cone metaphor does not prove OS reconstruction or positivity preservation under unvalidated reductions.

## Schur/Feshbach compression

Concept id: `ym.visual.schur-feshbach-shadow-bridge`
Status: `quarantine`
Physical carrier: `Compressed Wilson/OS block, carrier incomplete until certified`

A Schur/Feshbach reduction can expose an effective block, but positivity and carrier identity may be lost under projection or endpoint terms.

Metaphor family: `lens`
Metaphor: **A shadow bridge cast by a load-bearing bridge**

The shadow outlines an effective route, but it cannot carry weight unless one proves which beams and loads survived projection.

### Preserved And Distorted Properties

- `invariant` `partially_preserved`: Schur complement preserves selected spectral/algebraic information under hypotheses. -> The shadow preserves some outline of the bridge.. Only selected information is carried.
- `symmetry` `partially_preserved`: Symmetry may survive if the projection respects it. -> A symmetric bridge can cast an asymmetric shadow if the light is skewed.. Projection geometry matters.
- `locality_globality` `partially_preserved`: Local block elimination can change global coupling. -> Removing supports changes load paths across the whole bridge.. The image reveals hidden global effects.
- `order_monotonicity` `distorted`: Schur complements have conditional order properties. -> A darker shadow does not imply a stronger bridge.. The metaphor warns against invented monotonicity.
- `positivity_sign` `distorted`: Positivity can fail under endpoint or domain changes. -> A shadow cannot certify that the bridge carries positive load.. This is the central danger.
- `limiting_behavior` `partially_preserved`: Endpoint singularities and cutoffs may not commute with compression. -> The shadow changes discontinuously as the light approaches an endpoint.. The image captures endpoint fragility.
- `physical_carrier` `distorted`: The effective block may not be a same-theory observable carrier. -> The shadow is not the physical bridge.. This triggers quarantine unless certified.
- `proof_obligation` `preserved`: Supply positivity, carrier, and endpoint certificates. -> Inspect beams, loads, and endpoint shadows before crossing.. The required artifact is explicit.

### Distortion Ledger

- The metaphor is deliberately dangerous: it can make the effective object seem target-equivalent before proof.
- It does not preserve physical carrier identity without an external certificate.
- It can hide noncommuting endpoint and cutoff limits.

### Hypothesis Inspiration

- `quarantine_test` Quarantine Schur/Feshbach branches until a positivity-and-carrier certificate is computed.
  Route consequence: `quarantine`
  Required artifact: endpoint source table plus compressed-pairing positivity interval
  Falsifier: A negative compressed reflected pairing or a carrier mismatch under regulator refinement.

Audit verdict: `quarantine`
Allowed route consequence: `endpoint source table plus positivity interval`

Non-claim boundary: This analogy is not usable as proof support; it is a warning device until the missing certificates exist.

## Cutoff-uniform tail bound

Concept id: `ym.visual.uniform-tail-flood-barrier`
Status: `hypothesis_seed`
Physical carrier: `Wilson/OS observable family across regulator refinement`

The T_tail contribution must be bounded uniformly across the relevant cutoff/source/volume regime.

Metaphor family: `flow`
Metaphor: **A flood barrier that must hold at every reservoir height**

A tail estimate is a barrier against uncontrolled contribution; it is useful only if it does not need rebuilding for each cutoff height.

### Preserved And Distorted Properties

- `invariant` `preserved`: The bound must be stated independent of the moving cutoff parameter. -> The barrier height must not depend on one reservoir snapshot.. Uniformity is central.
- `symmetry` `absent`: Symmetry is secondary unless used in the tail estimate. -> Barrier symmetry is not the decisive feature.. No symmetry is invented.
- `locality_globality` `preserved`: Local tail terms affect global limit claims. -> A small leak can flood the downstream basin.. The image shows local failure becoming global.
- `order_monotonicity` `partially_preserved`: Tail dominance may require monotone envelopes. -> Water level envelopes bound all future heights.. Useful only when a monotone majorant exists.
- `positivity_sign` `partially_preserved`: Tail sign can decide a positivity interval. -> Leaks can push the level below the safe mark.. Sign effect is visible but not proved.
- `limiting_behavior` `preserved`: The estimate must survive cutoff/volume/source limits. -> The barrier must hold while the reservoir size changes.. Limit-uniformity is exactly represented.
- `physical_carrier` `preserved`: The same observable family must remain controlled across refinement. -> The same channel flows through every reservoir height.. Carrier continuity is explicit.
- `proof_obligation` `preserved`: Produce a uniform tail ledger or demote the branch. -> Publish the barrier design for all water heights.. The missing artifact is obvious.

### Distortion Ledger

- The image can overstate monotonicity if the tail is oscillatory or sign-changing.
- It does not show endpoint source equivalence classes unless paired with the source table.
- It should not be used to infer continuum control before the order-of-limits ledger exists.

### Hypothesis Inspiration

- `missing_artifact` Build a cutoff-uniform T_tail ledger before any finite positivity result is treated as target-facing.
  Route consequence: `artifact_sprint`
  Required artifact: uniform tail bound ledger with cutoff/source/volume parameters and failure thresholds
  Falsifier: Find a parameter sequence where the required tail barrier height diverges.

Audit verdict: `usable_for_hypothesis_generation`
Allowed route consequence: `uniform tail bound ledger`

Non-claim boundary: The flood-barrier metaphor does not prove a uniform estimate; it only makes the required estimate non-optional.

## OS reconstruction bridge

Concept id: `ym.visual.os-reconstruction-bridge`
Status: `hypothesis_seed`
Physical carrier: `OS Hilbert object reconstructed from Schwinger/Wilson data`

OS-positive Euclidean Schwinger data can reconstruct a Hilbert-space theory with spectral interpretation under the full axiom package.

Metaphor family: `bridge`
Metaphor: **A developing bridge from Euclidean blueprints to spectral load tests**

Euclidean data are the blueprint; OS reconstruction is the certified bridge; spectral objects are load tests on the completed structure.

### Preserved And Distorted Properties

- `invariant` `partially_preserved`: Axiom-preserving reconstruction must preserve correlation content. -> The bridge must match the blueprint's load-bearing coordinates.. Only full axiom compliance preserves content.
- `symmetry` `preserved`: Euclidean invariance must transfer to the reconstructed theory. -> Blueprint symmetries must become bridge symmetries.. Symmetry transfer is explicit.
- `locality_globality` `partially_preserved`: Local Euclidean data must support global Hilbert reconstruction. -> Local plans assemble into a global bridge.. Assembly obligations remain.
- `order_monotonicity` `absent`: No simple monotonicity carries reconstruction. -> More blueprint pages do not automatically mean a stronger bridge.. The analogy avoids false monotonicity.
- `positivity_sign` `preserved`: Reflection positivity is load-bearing. -> The bridge collapses if mirror beams fail sign tests.. Positivity is central.
- `limiting_behavior` `preserved`: Continuum and infinite-volume limits must produce admissible Schwinger data. -> The bridge must survive replacing temporary supports with permanent ones.. Limit survival is explicit.
- `physical_carrier` `preserved`: The reconstructed OS Hilbert object carries spectral claims. -> The completed bridge is where spectral load tests occur.. The carrier is named.
- `proof_obligation` `preserved`: Certify full OS axiom package, not only a finite positivity proxy. -> Inspect every load-bearing span before crossing.. The route gate is clear.

### Distortion Ledger

- Bridge imagery can make reconstruction look automatic once positivity is present.
- It may understate regularity, clustering, and continuum existence obligations.
- It does not prove a spectral gap unless a spectral carrier and gap estimate are supplied.

### Hypothesis Inspiration

- `route_mutation` Split the YM route into separate blueprint, bridge, and load-test artifacts.
  Route consequence: `reframe`
  Required artifact: OS reconstruction obligation ledger separating positivity, regularity, clustering, and spectral gap gates
  Falsifier: A finite positivity certificate with no corresponding OS axiom ledger.

Audit verdict: `usable_for_hypothesis_generation`
Allowed route consequence: `OS reconstruction obligation ledger`

Non-claim boundary: The metaphor does not establish OS reconstruction from the current finite packets.

## Mass gap spectral carrier

Concept id: `ym.visual.mass-gap-resonance-chamber`
Status: `hypothesis_seed`
Physical carrier: `Spectral object in the OS/Wightman/Hamiltonian theory`

A mass gap is a positive lower spectral separation above the vacuum sector in the reconstructed theory.

Metaphor family: `resonance`
Metaphor: **A resonance chamber with no low audible mode above the ground tone**

The vacuum is the ground tone; a mass gap means the next allowed resonance is separated by a real silent interval.

### Preserved And Distorted Properties

- `invariant` `preserved`: Spectral separation is invariant under unitary equivalence of the reconstructed theory. -> The silent interval survives relabeling of the chamber coordinates.. The gap is not a coordinate artifact.
- `symmetry` `partially_preserved`: Physical symmetries constrain the spectrum. -> Chamber symmetry constrains allowed resonant modes.. The analogy captures constraint but not full representation theory.
- `locality_globality` `preserved`: Mass gap is global spectral information tied to large-scale correlation behavior. -> A chamber-wide silence cannot be heard from one local panel alone.. The image distinguishes local checks from global spectrum.
- `order_monotonicity` `preserved`: Spectral lower bounds are order statements after reconstruction. -> The first audible mode sits above a threshold.. The ordering of modes is represented.
- `positivity_sign` `partially_preserved`: Hilbert-space positivity is prerequisite for spectral interpretation. -> A chamber with negative load-bearing material has no trustworthy resonance test.. Positivity is prerequisite, not the gap itself.
- `limiting_behavior` `preserved`: The gap must survive continuum and infinite-volume limits. -> The silent interval must remain as temporary walls are removed.. Limit survival is central.
- `physical_carrier` `preserved`: The spectral object carries the mass claim. -> The chamber, not the blueprint, carries resonances.. Carrier identity is explicit.
- `proof_obligation` `preserved`: Prove reconstruction plus a positive spectral lower bound. -> Build the chamber and measure the first resonance threshold.. The route cannot skip reconstruction.

### Distortion Ledger

- Resonance imagery can suggest a discrete finite spectrum; YM requires the correct infinite-volume spectral statement.
- It can hide the difference between exponential decay heuristics and a proven spectral gap.
- It does not justify transferring a finite matrix gap to continuum YM.

### Hypothesis Inspiration

- `falsifier` Add an order-of-limits falsifier for any route that infers a spectral gap before reconstruction.
  Route consequence: `falsifier_sprint`
  Required artifact: order-of-limits ledger connecting finite Wilson data, OS reconstruction, and spectral lower bound
  Falsifier: A limit order where the finite gap or decay witness disappears before the spectral object is constructed.

Audit verdict: `usable_for_hypothesis_generation`
Allowed route consequence: `order-of-limits spectral falsifier`

Non-claim boundary: The resonance image is not evidence for a positive mass gap; it only locates the target property and its carrier.

## Evidence

- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/run_state.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0348.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0349.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0350.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0351.json
- agentic/runs/discovery_marathons/yang-mills-smoke-marathon/cycles/cycle-0352.json

Validation handoff: `agentic/scripts/validate_visual_conceptualization_packet.py`
