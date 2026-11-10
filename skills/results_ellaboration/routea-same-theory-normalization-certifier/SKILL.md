---
name: routea-same-theory-normalization-certifier
description: Attack Route A module G2 by certifying that geometric-collar normalization is same-theory and positivity preserving. Use when perimeter, cusp, endpoint, boundary, or overlap factors must be classified as observable rescaling, congruence, block normalization, positive-kernel Schur factor, or inadmissible pair-dependent quotient.
---

# Route A Same-Theory Normalization Certifier

## Mathematical Target

Given a candidate geometric-collar reflected Gram block \(N_{k,\delta}\), determine whether its normalized block \(q_{k,\delta}\) is still realized inside the same regulated Yang--Mills theory.

Allowed mechanisms:

- diagonal congruence \(q=DND^*\);
- direct normalized observables \(F_i/\sqrt{N_{ii}}\);
- block congruence by an invertible observable change of basis;
- Schur product by a proved positive kernel with a reflected-Gram realization.

Forbidden mechanism:

- pair-dependent entrywise division \(N_{ij}/B_{ij}\) without a positivity-preserving certificate.

## Attack Procedure

1. List all normalization factors created by the collar geometry: perimeter, cusp, endpoint, boundary, overlap, and source factors.
2. Classify each factor as one-body, block, or pair-dependent.
3. For one-body factors, write the explicit diagonal matrix \(D_{k,\delta}\).
4. For pair-dependent factors, attempt a positive-kernel factorization; if none is available, demote the geometric application.
5. Check that normalized entries remain reflected expectations of observables in the same finite theory.
6. Produce a proposition or a clear demotion paragraph for the paper.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: factor inventory, factor classification, congruence proof, positive-kernel proof or failure, same-theory realization statement, and paper-ready proposition/demotion.

## Failure/Demotion

Demote if the normalization silently changes theory, assumes entrywise quotients preserve PSD, or lacks an observable-level realization.
