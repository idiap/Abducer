---
name: routea-endpoint-error-budget-certifier
description: Certify two-sided Route A endpoint error budgets. Use after an endpoint estimator exists and the paper must decide whether it gives a positive, negative, or inconclusive finite certificate.
---

# Route A Endpoint Error-Budget Certifier

## Target

Given \(\widehat R_{\mathrm{end}}\), \(M_G\), and error terms, prove or reject
\[
|R_{\mathrm{end}}-\widehat R_{\mathrm{end}}|\le \Delta_{\mathrm{end}}.
\]

## Certificate Logic

- Positive if \(M_G+\widehat R_{\mathrm{end}}-\Delta_{\mathrm{end}}>0\).
- Negative if \(M_G+\widehat R_{\mathrm{end}}+\Delta_{\mathrm{end}}<0\).
- Inconclusive otherwise.
- Invalid if any required term has only one-sided control.

## Deterministic Support

Use `certify_routea_endpoint_error_budget.py` for interval propagation and certificate classification. Include endpoint, corner, inter-box, far-tail, truncation, and stencil terms when present.

## Generative Work

For missing terms, propose the weakest analytic bound that would close the certificate. Do not convert missing upper bounds into negative evidence.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: estimator interval, margin interval, error terms, total two-sided error, certificate class, missing constants, theorem/proposition eligibility, and paper-safe wording.

## Failure/Demotion

Demote if a lower bound is used as a negative certificate, if an error class is omitted, or if constants are hidden behind "small".
