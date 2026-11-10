<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Open-Module Results Elaboration Plan

- Source: `/Users/afreitas/projects/abducer/abducer/agentic/reports/results_ellaboration/a-finite-schur-feshbach-test-for-reflected-wilson-blocks-an-explicit-four-dimens/finite_wilson_os_routeA_SU2_attack_integrated.tex`
- Title: A Finite Schur--Feshbach Test for Reflected Wilson Blocks: An Explicit Four-Dimensional SU(2) Heat-Kernel Lattice Realization
- Open modules: 0
- Independent from discovery workflows: `True`

## Claim Boundary

Finite-cutoff SU(2) heat-kernel Route A realization of a reflected Wilson-block Schur-Feshbach test, with geometric collar, endpoint, continuum, and gap steps isolated as open modules.

Non-claims:
- does not prove a continuum Yang-Mills measure
- does not prove full OS reconstruction
- does not prove a mass gap
- does not prove geometric collar collapse from the source-collision model

## Extracted Open Modules

## Ordered Self-Contained TODOs

### todo-001: Integrate and certify the supplied three-hairpin verification script

- Source marker: `deterministic:finite-route-a-algebra`
- Target section: Coefficient extraction and the finite certificate
- Work class: `deterministic_symbolic_validation`
- Priority: 98
- Mathematical object: N_eps, D_eps, q_eps, H,K,A,C, det(q_eps), z^T PKP z, z^T correction z, z^T C z, and reduced u/v margins
- Depends on: none
- Required inputs: verify_three_hairpin_block.py, eq:N-exact, eq:D-normalization, eq:q-exact, eq:alpha-beta, eq:H-explicit, eq:K-explicit, thm:evaluated-gate
- Subtasks:
  - Import the supplied `verify_three_hairpin_block.py` logic into the result-elaboration workflow rather than leaving it in Downloads.
  - Verify symbolically that N_eps=11^T+eps sigma bb^T+eps^2 tau cc^T and q_eps=D_eps N_eps D_eps.
  - Differentiate q_eps at eps=0 to recover the displayed H and K matrices.
  - Verify A=PHP=sigma bb^T and C=P(K-1/3 Hee^T H)P=-sigma^2 bb^T+(tau/9)zz^T.
  - Verify det(q_eps)=4 eps^3 sigma tau / ((1+eps sigma)^2(1+eps^2 tau)).
  - Verify z^T PKP z=sigma^2+4 tau, z^T(1/3 PHee^T HP)z=sigma^2, and z^T C z=4 tau.
  - Verify u^T A u=2 sigma, v^T C v=2 tau/3, and u^T C v=0.
  - Emit JSON and Markdown certificates that the paper can cite from the reproducibility protocol.
  - Write any discrepancy as a paper correction TODO, not as a hidden assumption.
- Deterministic regime:
  - sympy exact algebra
  - TeX equation reference audit
  - pdflatex
- Generative regime:
  - interpret whether the exact source block is scientifically strong enough or needs geometric collar replacement
  - decide how the certificate should be narrated: as proof support for finite Route A, not as evidence for G1-G4
- Critical self-refinement:
  - Does the symbolic check verify only the source-collision model, or is it being overread as geometric collar evidence?
  - Does the determinant strictness depend only on sigma,tau > 0?
  - Does the paper make the spurious sigma^2 cancellation visible enough for readers to understand why Schur-Feshbach matters?
- Expected artifact: A repo-local `routea_three_hairpin_certificate.json` and Markdown certificate verifying all displayed finite algebra.
- Acceptance criterion: The supplied script's symbolic identities pass in the repo workflow and the certificate explicitly records every scalar identity used in the Route A narrative.
- Paper insertion target: Cite the certificate in the finite evaluation and reproducibility protocol, and add one sentence explaining that it certifies only the finite source-collision block.
- Validation handoff: Run `verify_routea_three_hairpin_block.py`, then `results-critical-self-refiner`.
- Stop/quarantine condition: Do not proceed to open-module proof planning if the current finite algebra is inconsistent.
- Skills: results-open-module-decomposer, results-critical-self-refiner, results-expansion-validator
- Narrative consequence: This protects the claim that Route A has an exact finite-cutoff block rather than a schematic one.

### todo-002: Compile and audit manuscript integrity before expansion

- Source marker: `deterministic:manuscript-integrity`
- Target section: whole draft
- Work class: `deterministic_manuscript_validation`
- Priority: 97
- Mathematical object: TeX labels, references, citations, theorem numbering, and open-module environments
- Depends on: none
- Required inputs: full TeX draft
- Subtasks:
  - Run label/reference audit and identify duplicate or missing labels.
  - Compile the TeX to PDF.
  - Check that all open modules are visible in the final PDF.
  - Check that claims through Corollary implemented-route-a remain finite-cutoff claims.
  - Record warnings that affect scientific readability.
- Deterministic regime:
  - regex label/ref audit
  - pdflatex
  - openmodule count
- Generative regime:
  - interpret whether warnings indicate a conceptual overclaim or only formatting debt
- Critical self-refinement:
  - Does the paper hide any open module in prose rather than stating it?
  - Does the abstract claim more than the sections prove?
- Expected artifact: A compile/log and claim-boundary audit.
- Acceptance criterion: The manuscript compiles, references resolve, and claim boundaries remain consistent with the open modules.
- Paper insertion target: Apply corrections globally before expanding any module.
- Validation handoff: Run TeX compile and `results-expansion-validator`.
- Stop/quarantine condition: Do not expand results on top of an uncompilable or internally inconsistent draft.
- Skills: results-critical-self-refiner, results-expansion-validator
- Narrative consequence: This ensures the finite Route A contribution is inspectable before future-module ambition is added.

## Critical Self-Refinement Summary

Limitations found:
- The older slot workflow misses Route A because this draft uses openmodule environments.
- The paper already has a finite result, so TODOs must not ask to re-prove what is already implemented.
- Open modules mix deterministic validation, generative proof design, and manuscript narrative updates unless explicitly separated.

Repairs applied:
- Open modules are parsed as first-class result-extension obligations.
- Every TODO now has deterministic_regime, generative_regime, and critical_self_refinement fields.
- Every TODO names how successful results feed back into the paper and how failure remains as a bounded open module.

## Narrative Integration

- The finite SU(2) heat-kernel source-collision block is the claimable core.
- The immediate paper-strengthening task is to integrate the supplied three-hairpin verification script as a citable certificate for the exact finite algebra.
- The next scientific step is not more source-amplitude algebra but a geometric collar family G1-G4.
- Endpoint and spectral modules are downstream; they should not be promoted until the geometric/cutoff modules discharge.

Paper updates after discharge:
- If the verification script passes, cite `routea_three_hairpin_certificate.json` in the reproducibility protocol and state that it verifies the finite source-collision algebra only.
- If G1-G4 discharge, revise the abstract from source-collision realization to geometric-collar realization.
- If E1-E2 discharge, add endpoint theorem language with two-sided certificate logic.
- Keep M1-M2 as open modules unless continuum reconstruction and spectral estimates are actually proved.
