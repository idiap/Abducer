---
name: routea-margin-endpoint-certifier
description: Attack Route A modules G4, E1, and E2 by seeking strict reduced-margin certificates and regulator-derived endpoint estimates with two-sided error bounds. Use when the paper needs lower bounds for sigma_k,tau_k, endpoint color/incidence derivations, cumulant/tail estimates, or a decision between positive, negative, and inconclusive finite certificates.
---

# Route A Margin And Endpoint Certifier

## Mathematical Targets

For G4, prove or certify nonvanishing reduced margins such as
\[
\inf_{k\ge k_0}\sigma_k>0,\qquad
\inf_{k\ge k_0}\tau_k>0.
\]

For E1/E2, derive an endpoint estimator from the same \(SU(2)\) heat-kernel regulator and prove a two-sided error bound
\[
|R_{\mathrm{end}}-\widehat R_{\mathrm{end}}|\le \Delta_{\mathrm{end}}.
\]

## Attack Procedure

1. Identify whether G1-G3 are available. If not, restrict work to finite source-collision margins or endpoint bookkeeping.
2. For G4, decide the evidence route: character expansion, transfer matrix, symmetry exclusion, certified finite computation, or demotion.
3. For E1, derive endpoint boxes, source variables, singlet projections, color factor, and incidence weights from the actual paths.
4. For E2, bound fourth source cumulants, sixth-derivative stencil error, endpoint/corner/inter-box/tail terms.
5. Classify the certificate:
   - positive if \(M_G+\widehat R_{\mathrm{end}}-\Delta_{\mathrm{end}}>0\);
   - negative if \(M_G+\widehat R_{\mathrm{end}}+\Delta_{\mathrm{end}}<0\);
   - inconclusive otherwise.
6. Patch only mathematically justified paper claims.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: margin quantities, lower-bound route, endpoint derivation, two-sided error estimate, certificate classification, unresolved analytic burden, and paper theorem/demotion text.

## Failure/Demotion

Demote if the argument uses nonnegativity as strict positivity, derives endpoint signs from an ansatz, uses one-sided bounds as negative certificates, or depends on a gap/decay estimate not yet proved.
