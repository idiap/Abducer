---
name: routea-finite-margin-evaluator
description: Evaluate or certify finite Route A source-collision margins sigma and tau with explicit uncertainty. Use when the SU(2) Wilson-block paper needs a concrete finite lattice example without claiming cutoff-uniform or continuum nonvanishing.
---

# Route A Finite Margin Evaluator

## Target

Produce a finite certificate for \(\sigma\) and \(\tau\), the margins controlling the exact source-collision block. The certificate is finite-cutoff only. It must not be described as continuum evidence.

## Allowed Inputs

Use one of:

- same-regulator Wilson expectation intervals for \(\sigma\) and \(\tau\);
- exact finite integration results;
- character-truncated heat-kernel estimates with explicit tail bounds;
- certified quadrature intervals.

Do not use an arbitrary surrogate matrix as a Wilson margin.

## Deterministic Support

Use `evaluate_routea_finite_margins.py` to validate parameters, propagate intervals, classify the result, and write a JSON certificate.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: lattice/action/path parameters, observable provenance, sigma interval, tau interval, uncertainty sources, strict positivity verdict, non-claims, paper insertion target, and whether the result belongs in the body or appendix.

## Failure/Demotion

Demote if the result is a point estimate without uncertainty, uses a non-Wilson proxy, or implies cutoff-uniform nonvanishing.
