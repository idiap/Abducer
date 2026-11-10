<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Results Elaboration Plan

- Source: `/Users/afreitas/Downloads/finite_wilson_os_schur_feshbach_paper_restructured.tex`
- Title: A Finite Schur--Feshbach Consistency Test for Normalized Reflected Wilson Gram Blocks
- Slots: 8
- Markers: 19
- Independent from discovery workflows: `True`

## Claim Boundary

Finite Schur-Feshbach consistency test for normalized reflected Wilson Gram blocks near a rank-one collision limit.

Non-claims:
- does not construct four-dimensional Yang-Mills theory
- does not prove OS reconstruction for a continuum gauge field
- does not prove a mass gap

## Expansion Slots

### Regulator and observable theorem

- Label: `slot:regulator-observable`
- Section: Regulator and observable data
- Work class: `proof_completion`
- Priority: 90
- Expected artifact: A regulator theorem naming the finite lattice, gauge group, action, reflection map, positive-time algebra, Wilson collar observables, and the resulting reflected Gram block.
- Acceptance criterion: A reader can construct q_{a,eps} from the stated finite regulated Wilson data and verify reflection positivity without importing unstated continuum assumptions.

### Same-theory quotient theorem

- Label: `slot:same-theory-quotient`
- Section: Regulator and observable data
- Work class: `same_theory_transfer`
- Priority: 95
- Expected artifact: A theorem or proposition replacing the schematic quotient with a positivity-preserving same-theory construction.
- Acceptance criterion: The normalized block is proved to be a reflected Gram block, diagonal/block congruence, or positive-kernel factorization inside the same regulated theory.

### Boundary-OPE coefficient theorem

- Label: `slot:HK-theorem`
- Section: Coefficient extraction slots
- Work class: `coefficient_extraction`
- Priority: 92
- Expected artifact: A coefficient theorem giving explicit or bounded H_a and K_a with an O_a(eps^3) or stated replacement remainder.
- Acceptance criterion: H_a and K_a are derived from q_{a,eps} in the chosen regulator, converted from log-coefficients when needed, and accompanied by an explicit operator-norm remainder.

### Nontrivial finite outcome

- Label: `slot:nontrivial-outcome`
- Section: Coefficient extraction slots
- Work class: `finite_application`
- Priority: 88
- Expected artifact: A finite sign/margin/obstruction result obtained by applying the Schur-Feshbach theorem to computed H_a,K_a.
- Acceptance criterion: For one named Wilson block, the Schur-Feshbach test produces a strict margin, a null-sector scalar, a negative diagnostic vector, or a degeneracy certificate.

### Endpoint color and combinatorial factor

- Label: `slot:color-factor`
- Section: Endpoint and remainder slots
- Work class: `coefficient_extraction`
- Priority: 84
- Expected artifact: A regulator-specific derivation of C_col^(G,R,reg) with all representation and path-ordering conventions exposed.
- Acceptance criterion: C_col^(G,R,reg) is derived from a named finite group/source integral with trace, representation, orientation, and path-ordering conventions fixed.

### Uniform endpoint and tail theorem

- Label: `slot:uniform-remainder`
- Section: Endpoint and remainder slots
- Work class: `coefficient_extraction`
- Priority: 82
- Expected artifact: A uniform endpoint/tail estimate with source domain, constants, and limit regime.
- Acceptance criterion: The endpoint remainder and tail terms are bounded uniformly over the named finite block in the exact limit regime used by the application.

### Prior-art boundary

- Label: `slot:prior-art`
- Section: Endpoint and remainder slots
- Work class: `prior_art_boundary`
- Priority: 74
- Expected artifact: A prior-art boundary paragraph/table that limits novelty to the proved finite packaging and coefficient calculation.
- Acceptance criterion: Novelty language cites prior art and excludes claims not proved in the draft.

### Three-hairpin coefficient table

- Label: `slot:three-hairpin-table`
- Section: Three-hairpin block as an application template
- Work class: `finite_application`
- Priority: 80
- Expected artifact: A reproducible coefficient table for the three-hairpin block, including cancellation and corrected second-order survivors.
- Acceptance criterion: The three-hairpin section contains a reproducible pair-indexed coefficient table and the associated Schur-corrected scalar or explicit demotion to template status.

## Ordered Self-Contained TODOs

### todo-001: Same-theory quotient theorem

- Source marker: `slot:same-theory-quotient`
- Target section: Regulator and observable data
- Work class: `same_theory_transfer`
- Priority: 95
- Mathematical object: normalized reflected Wilson Gram block q and its same-theory positivity-preserving realization
- Depends on: slot:regulator-observable
- Required inputs: regulated Wilson observable algebra, normalization map, positivity-preserving representation, counterexample check for entrywise division
- Subtasks:
  - Write the current quotient formula entrywise and classify every normalization factor as one-body, block, or pair-dependent.
  - For one-body factors, prove the equivalent diagonal congruence.
  - For pair-dependent factors, either construct a positive-kernel factorization or prove the normalized observables whose reflected Gram block is q.
  - Run a finite counterexample check showing why unsupported entrywise division cannot be assumed positivity-preserving.
  - Replace the slot with the strongest valid theorem: congruence, factorization, direct Gram realization, or explicit demotion.
- Action: Prove or falsify the same-theory transfer certificate for the normalization used in the draft.
- Expected artifact: A theorem or proposition replacing the schematic quotient with a positivity-preserving same-theory construction.
- Acceptance criterion: The normalized block is proved to be a reflected Gram block, diagonal/block congruence, or positive-kernel factorization inside the same regulated theory.
- Limitation addressed: The draft warns that entrywise normalization is schematic; this TODO prevents the paper from smuggling positivity through an unsupported quotient.
- Paper insertion target: Replace the quotient slot with a theorem/proposition and add a short warning paragraph for quotient forms that fail the certificate.
- Validation handoff: Run a positivity-preservation audit with `bridge-object-equivalence-checker` and `results-expansion-validator`.
- Stop/quarantine condition: Demote the Wilson application if normalization remains pair-dependent entrywise division and no same-theory Gram realization, congruence, or positive-kernel factorization is proved.
- Skills: results-extension-need-extractor, bridge-object-equivalence-checker, finite-theorem-section-packager, results-expansion-validator
- Narrative consequence: This protects the explanatory narrative from implying that entrywise normalization automatically preserves OS positivity.

### todo-002: Boundary-OPE coefficient theorem

- Source marker: `slot:HK-theorem`
- Target section: Coefficient extraction slots
- Work class: `coefficient_extraction`
- Priority: 92
- Mathematical object: coefficient matrices H_a and K_a in the rank-one Wilson block expansion
- Depends on: slot:regulator-observable, slot:same-theory-quotient
- Required inputs: fixed regulator, observable family, coefficient definitions, uniform remainder regime
- Subtasks:
  - Freeze the regulator, Wilson family, collar parameter, and coefficient convention.
  - Define H_a and K_a from the actual normalized block q_{a,eps}, not from an informal log expression alone.
  - If logarithmic coefficients are used, apply the finite log-to-matrix conversion from the appendix.
  - State whether the formulas are exact at fixed lattice spacing, asymptotic in a heat-kernel parameter, or interval-bounded.
  - Give an explicit operator-norm remainder and the regime in which it is valid.
- Action: Derive the requested coefficient, prefactor, incidence, or uniform remainder in the named regulator and expose all validity conditions.
- Expected artifact: A coefficient theorem giving explicit or bounded H_a and K_a with an O_a(eps^3) or stated replacement remainder.
- Acceptance criterion: H_a and K_a are derived from q_{a,eps} in the chosen regulator, converted from log-coefficients when needed, and accompanied by an explicit operator-norm remainder.
- Limitation addressed: The draft needs H_a and K_a as matrix coefficients, not just qualitative OPE language; this TODO demands a same-regulator derivation and remainder.
- Paper insertion target: Replace the coefficient slot with a theorem and move derivational details to an appendix if they are too long for the main text.
- Validation handoff: Run symbolic/numeric reproducibility check where applicable and `results-expansion-validator`.
- Stop/quarantine condition: Stop coefficient expansion if H_a,K_a cannot be derived from the same q_{a,eps}; do not substitute informal OPE language for matrix coefficients.
- Skills: results-extension-need-extractor, endpoint-worked-calculation-packager, results-narrative-integrator, results-expansion-validator
- Narrative consequence: This supplies the bridge from abstract H,K theorem to actual Wilson coefficient data.

### todo-003: Regulator and observable theorem

- Source marker: `slot:regulator-observable`
- Target section: Regulator and observable data
- Work class: `proof_completion`
- Priority: 90
- Mathematical object: regulated Wilson observable family and finite reflected Gram matrix
- Depends on: none
- Required inputs: precise theorem statement, definitions and validity regime, proof dependencies, claim-boundary audit
- Subtasks:
  - Choose exactly one regulated setting, preferably the heat-kernel plaquette action if endpoint cumulants are part of the expansion.
  - State the finite lattice, reflection plane, positive-time edge convention, collar support convention, group G, representation R, and Wilson observable family.
  - Prove or cite reflection positivity for the chosen finite measure and reflection plane.
  - Prove each Wilson observable lies in the positive-time gauge-invariant algebra.
  - Write the theorem so it can be cited before any quotient or coefficient calculation.
- Action: Replace the slot with a theorem/proposition/lemma package including definitions, assumptions, proof route, and non-claims.
- Expected artifact: A regulator theorem naming the finite lattice, gauge group, action, reflection map, positive-time algebra, Wilson collar observables, and the resulting reflected Gram block.
- Acceptance criterion: A reader can construct q_{a,eps} from the stated finite regulated Wilson data and verify reflection positivity without importing unstated continuum assumptions.
- Limitation addressed: The draft currently names QFT data schematically; this TODO forces a concrete finite regulated setting before any quotient or coefficient theorem is allowed to rely on it.
- Paper insertion target: Replace the regulator slot with a proposition immediately before the same-theory quotient discussion.
- Validation handoff: Run proof-gap review and `results-expansion-validator`.
- Stop/quarantine condition: Quarantine the Wilson-block application if the finite regulator, reflection plane, positive-time algebra, and Wilson observable support convention cannot be fixed in one setting.
- Skills: results-extension-need-extractor, finite-theorem-section-packager, results-expansion-validator
- Narrative consequence: This clarifies how the expansion changes the paper body, appendix, or claim boundary.

### todo-004: Nontrivial finite outcome

- Source marker: `slot:nontrivial-outcome`
- Target section: Coefficient extraction slots
- Work class: `finite_application`
- Priority: 88
- Mathematical object: finite Schur-Feshbach reduced forms PHP and P(K-n^{-1}Hee^*H)P
- Depends on: slot:HK-theorem
- Required inputs: finite Wilson geometry, reflected Gram block, computed H and K, Schur-corrected null-sector test
- Subtasks:
  - Select the first concrete finite Wilson block to test, with n, observable labels, and geometry fixed.
  - Compute PHP on a basis of one^perp and determine whether it is strictly positive or has a null sector.
  - If a null sector exists, compute P(K-n^{-1}Hee^*H)P on that sector.
  - Report a lower bound, negative diagnostic vector, or degeneracy certificate.
  - Update the abstract/introduction only if this produces a genuine finite application result.
- Action: Compute the finite Schur-Feshbach test for the concrete block and report margin, null-sector result, obstruction vector, or degeneracy.
- Expected artifact: A finite sign/margin/obstruction result obtained by applying the Schur-Feshbach theorem to computed H_a,K_a.
- Acceptance criterion: For one named Wilson block, the Schur-Feshbach test produces a strict margin, a null-sector scalar, a negative diagnostic vector, or a degeneracy certificate.
- Limitation addressed: The draft has a finite theorem but needs one concrete Wilson-block consequence; this TODO blocks narrative promotion unless a sign, margin, vector, or degeneracy is computed.
- Paper insertion target: Insert the resulting finite sign or degeneracy statement as the first concrete application after the coefficient theorem.
- Validation handoff: Run an independent finite-matrix/sign check and `results-expansion-validator`.
- Stop/quarantine condition: Demote to application template if no strict margin, null-sector scalar, negative vector, or degeneracy certificate is produced for a named finite block.
- Skills: results-extension-need-extractor, endpoint-worked-calculation-packager, finite-theorem-section-packager, results-narrative-integrator, results-expansion-validator
- Narrative consequence: This is the manuscript's result-bearing upgrade from finite theorem note to worked Wilson-block application.

### todo-005: Endpoint color and combinatorial factor

- Source marker: `slot:color-factor`
- Target section: Endpoint and remainder slots
- Work class: `coefficient_extraction`
- Priority: 84
- Mathematical object: endpoint color/combinatorial prefactor C_col^(G,R,reg)
- Depends on: slot:regulator-observable, slot:HK-theorem
- Required inputs: fixed regulator, observable family, coefficient definitions, uniform remainder regime, gauge group, representation normalization, path ordering convention, plaquette-sheet convention
- Subtasks:
  - Define the endpoint source partition function or finite group integral Z_v in the chosen regulator.
  - Derive the fourth-source prefactor from the Wilson/path-ordered expansion.
  - Track representation normalization, trace convention, plaquette-sheet orientation, and heat-kernel or Wilson-action parameter.
  - State C_col^(G,R,reg) with all dependencies visible.
  - Mark endpoint algebra as conditional until this prefactor is inserted into the same-theory calculation.
- Action: Derive the requested coefficient, prefactor, incidence, or uniform remainder in the named regulator and expose all validity conditions.
- Expected artifact: A regulator-specific derivation of C_col^(G,R,reg) with all representation and path-ordering conventions exposed.
- Acceptance criterion: C_col^(G,R,reg) is derived from a named finite group/source integral with trace, representation, orientation, and path-ordering conventions fixed.
- Limitation addressed: The draft uses placeholder endpoint constants; this TODO requires the color/combinatorial factor to be derived rather than named.
- Paper insertion target: Replace the endpoint-color slot and cross-reference it from the conditional endpoint cumulant section.
- Validation handoff: Run symbolic/numeric reproducibility check where applicable and `results-expansion-validator`.
- Stop/quarantine condition: Keep endpoint constants conditional if the color prefactor cannot be derived from the same regulator, group integral, trace convention, and path-ordering convention.
- Skills: results-extension-need-extractor, endpoint-worked-calculation-packager, results-narrative-integrator, results-expansion-validator
- Narrative consequence: This determines whether conditional endpoint algebra can be promoted from placeholder to controlled application material.

### todo-006: Uniform endpoint and tail theorem

- Source marker: `slot:uniform-remainder`
- Target section: Endpoint and remainder slots
- Work class: `coefficient_extraction`
- Priority: 82
- Mathematical object: endpoint remainder r_{a,eps}, tail term E_tail, and uniform source-derivative bounds
- Depends on: slot:regulator-observable, slot:color-factor
- Required inputs: fixed regulator, observable family, coefficient definitions, uniform remainder regime, source domain, fourth/sixth derivative bound, tail term definition
- Subtasks:
  - Define r_{a,eps}, E_tail, source domain, and limit regime before bounding them.
  - State the fourth- or sixth-derivative source estimates used for endpoint cumulant stencils.
  - Give constants uniform in the variables required by the chosen finite Wilson block.
  - Prove rho(a,eps)=o(eps^2) or state the exact replacement bound if the regime differs.
  - State how the bound enters the finite margin or obstruction inequality.
- Action: Derive the requested coefficient, prefactor, incidence, or uniform remainder in the named regulator and expose all validity conditions.
- Expected artifact: A uniform endpoint/tail estimate with source domain, constants, and limit regime.
- Acceptance criterion: The endpoint remainder and tail terms are bounded uniformly over the named finite block in the exact limit regime used by the application.
- Limitation addressed: The endpoint algebra is conditional until tails are controlled; this TODO tests whether the asymptotic estimate is strong enough for the finite positivity margin.
- Paper insertion target: Replace the uniform-remainder slot and cite it in the finite margin or obstruction inequality.
- Validation handoff: Run symbolic/numeric reproducibility check where applicable and `results-expansion-validator`.
- Stop/quarantine condition: Keep endpoint algebra out of the result claim if the remainder is not uniform in the variables used by the finite Schur-Feshbach margin.
- Skills: results-extension-need-extractor, endpoint-worked-calculation-packager, results-narrative-integrator, results-expansion-validator
- Narrative consequence: This clarifies how the expansion changes the paper body, appendix, or claim boundary.

### todo-007: Three-hairpin coefficient table

- Source marker: `slot:three-hairpin-table`
- Target section: Three-hairpin block as an application template
- Work class: `finite_application`
- Priority: 80
- Mathematical object: three-hairpin reflected Wilson coefficient table and null-sector scalar
- Depends on: slot:regulator-observable, slot:same-theory-quotient, slot:HK-theorem, slot:nontrivial-outcome
- Required inputs: finite Wilson geometry, reflected Gram block, computed H and K, Schur-corrected null-sector test, three paths, pair table, zero-sum cancellation data, endpoint/remainder columns
- Subtasks:
  - Specify the three hairpin paths combinatorially or with a figure-ready incidence description.
  - Build the pair-indexed coefficient table with one-body, mixed boundary, endpoint, and remainder columns.
  - Mark which entries vanish by zero-sum cancellation and which survive in PHP.
  - Compute which entries survive only through the Schur-corrected second-order form.
  - Attach the table to the nontrivial finite outcome or demote the section to an application template.
- Action: Compute the finite Schur-Feshbach test for the concrete block and report margin, null-sector result, obstruction vector, or degeneracy.
- Expected artifact: A reproducible coefficient table for the three-hairpin block, including cancellation and corrected second-order survivors.
- Acceptance criterion: The three-hairpin section contains a reproducible pair-indexed coefficient table and the associated Schur-corrected scalar or explicit demotion to template status.
- Limitation addressed: The application template is not yet a worked example; this TODO forces a reproducible table and Schur-corrected scalar for the three-hairpin block.
- Paper insertion target: Insert the table in the three-hairpin section and cite it from the nontrivial finite outcome.
- Validation handoff: Run an independent finite-matrix/sign check and `results-expansion-validator`.
- Stop/quarantine condition: Quarantine the three-hairpin application if the path geometry, pair table, H,K entries, or Schur-corrected scalar cannot be reproduced from the draft data.
- Skills: results-extension-need-extractor, endpoint-worked-calculation-packager, finite-theorem-section-packager, results-narrative-integrator, results-expansion-validator
- Narrative consequence: This is the manuscript's result-bearing upgrade from finite theorem note to worked Wilson-block application.

### todo-008: Prior-art boundary

- Source marker: `slot:prior-art`
- Target section: Endpoint and remainder slots
- Work class: `prior_art_boundary`
- Priority: 74
- Mathematical object: novelty boundary of the finite Schur-Feshbach Wilson/OS packaging
- Depends on: slot:regulator-observable, slot:same-theory-quotient, slot:HK-theorem, slot:nontrivial-outcome
- Required inputs: finite theorem claim, application claim, candidate references, novelty boundary language
- Subtasks:
  - List prior-art families: Schur complements, Feshbach maps, lattice reflection positivity, Wilson-loop renormalization, heat-kernel actions, constructive gauge theory.
  - For each family, state what is standard and what the present paper packages differently.
  - Separate the finite theorem novelty from any Wilson-block coefficient novelty.
  - Rewrite abstract/introduction novelty language to cite only discharged results.
  - Quarantine unsupported novelty claims into future work or remove them.
- Action: Compare the claimed contribution against named prior-art families and rewrite novelty language accordingly.
- Expected artifact: A prior-art boundary paragraph/table that limits novelty to the proved finite packaging and coefficient calculation.
- Acceptance criterion: Novelty language cites prior art and excludes claims not proved in the draft.
- Limitation addressed: The contribution boundary is fragile; this TODO prevents the manuscript from claiming novelty already covered by Schur complements, Feshbach maps, or lattice reflection positivity.
- Paper insertion target: Rewrite the introduction and discussion novelty paragraphs, not only the placeholder slot.
- Validation handoff: Run prior-art source check and claim-boundary audit.
- Stop/quarantine condition: Stop when novelty language is bounded by cited prior art and unsupported broader novelty claims are removed.
- Skills: results-extension-need-extractor, prior-art-positioning-packager, timeline-reference-manager, results-expansion-validator
- Narrative consequence: This makes the contribution claim legible and defensible to readers familiar with Schur complements, Feshbach maps, and lattice OS positivity.

## Local Workflow Hooks

- `pre_context_interpretation`
- `post_context_interpretation`
- `post_need_extraction`
- `pre_strategy_planning`
- `post_strategy_planning`
- `post_narrative_integration`
- `final_results_elaboration_validation`

Forbidden couplings:
- discovery marathon jobs
- branch schedulers
- target active pointers
- long-horizon discovery queues
- global hooks/hooks.json mutation

## TODO Review Repairs

Limitations found:
- Class-level acceptance criteria can hide the exact mathematical gate for a slot.
- Generic stop conditions can permit endless narrative elaboration without a theorem, coefficient, sign test, or citation boundary.
- Narrative consequences are useful only if they state where the manuscript changes after the result is discharged.

Repairs applied:
- Each TODO now carries a slot-specific limitation addressed.
- Each TODO now names the paper insertion target where the expansion should land.
- Acceptance and stop criteria were specialized for regulator data, same-theory normalization, H,K extraction, endpoint constants, uniform tails, finite outcomes, prior art, and the three-hairpin table.

## Narrative Integration

- Finite theorem and proof are the stable core.
- Wilson application remains conditional until regulator, observables, same-theory quotient, H,K extraction, and uniform remainders are supplied.
- Three-hairpin block is the preferred first result-bearing expansion because it can turn the theorem into a worked finite application.
- Endpoint cumulant algebra belongs as conditional scaffolding until color factors and tail estimates are derived in the same regulator.

Paper updates after discharge:
- Update abstract only when a slot is replaced by a proved theorem or reproducible calculation.
- Update introduction to distinguish finite theorem, worked Wilson application, and remaining continuum obligations.
- Move author-facing checklist material out of final body after TODOs are discharged or quarantined.
- Keep the discussion explicit about non-claims unless all continuum obligations are proved.
