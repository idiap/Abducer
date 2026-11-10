---
name: routea-symbolic-cas-auditor
description: Perform exact symbolic and CAS-assisted audits for the Route A SU(2) reflected Wilson-block paper. Use when the finite Schur--Feshbach source-collision theorem, geometric-collar coefficient extraction, same-theory normalization, endpoint incidence algebra, finite margin certificates, or manuscript result integration needs exact matrix algebra, symbolic expansion checks, determinant/eigenvalue certificates, two-sided endpoint inequality logic, or CAS-backed proof-obligation extraction without invoking discovery-marathon workflows.
---

# Route A Symbolic CAS Auditor

## Conceptual Role

Use this skill for the active Route A finite Wilson-block paper when the question is not "what should we explore next?" but "which exact symbolic facts are available for the manuscript, and which claims remain open?"

For this paper, symbolic/CAS reasoning should be present in these regimes:

1. **Rank-one Schur--Feshbach algebra.** Verify \(H,K,A,C\), the Schur correction, determinant, reduced eigenvalues, kernel restrictions, and strict finite margins.
2. **Source-collision coefficient audit.** Confirm that the source-amplitude block gives the advertised \(\sigma,\tau\) formulas and does not get reused as a geometric-collar coefficient theorem.
3. **Same-theory normalization gates.** Check finite PSD, entrywise inverse PSD, Schur-product admissibility, congruence admissibility, and counterexamples to pair-dependent quotient claims.
4. **Geometric-collar coefficient obligations.** Symbolically separate one-body terms, genuine pair terms, and rank-one Schur corrections for a future \(q_{k,\delta}\), while requiring the coefficients to come from the same normalized Wilson block.
5. **Endpoint/null-channel incidence algebra.** Verify off-diagonal null-vector identities, endpoint weight patterns, and the two-sided certificate inequalities before any sign claim is placed in the paper.
6. **TeX-safe result integration.** Convert exact symbolic outputs into theorem, proposition, lemma, certificate, or demotion language without leaking workflow or CAS-process jargon into the manuscript.

## Workflow

1. **Identify the symbolic target.**
   Classify the task as `source_collision_certificate`, `normalization_gate`, `geometric_coefficient_gate`, `finite_margin_certificate`, `endpoint_incidence`, `endpoint_error_budget`, or `manuscript_integration`.

2. **State the mathematical carrier.**
   Name the matrix family, variables, projection, null vector, Wilson observables, finite lattice/regulator status, and the exact claim boundary.

3. **Run the narrow symbolic audit.**
   Prefer the bundled script:
   ```bash
   .venv-pmp/bin/python skills/results_ellaboration/routea-symbolic-cas-auditor/scripts/audit_routea_symbolic_cas.py
   ```
   Use the existing workflow scripts for adjacent checks: `verify_routea_three_hairpin_block.py`, `check_schur_factor_candidates.py`, `evaluate_routea_finite_margins.py`, `derive_routea_endpoint_incidence.py`, and `certify_routea_endpoint_error_budget.py`.

4. **Inspect the artifact.**
   Read the emitted JSON before interpreting it. Confirm whether each item is `exact_symbolic_certificate`, `finite_counterexample`, `conditional_gate`, `proof_obligation`, `blocked`, or `demoted`.

5. **Generate paper-safe interpretation.**
   Translate the symbolic result into the manuscript claim form:
   theorem for exact Schur algebra; proposition for normalization gates; lemma for endpoint identity; certificate for finite margins; demotion remark when a symbolic check blocks promotion.

6. **Handoff locally.**
   Send coefficient obligations to `routea-geometric-coefficient-extractor`, normalization failures to `routea-same-theory-normalization-certifier`, endpoint algebra to `routea-endpoint-local-integral-calculator` or `routea-endpoint-error-budget-certifier`, and validated prose to `routea-paper-result-integrator`. Do not route into discovery marathons.

## Mathematical Invariants

- Mathematical object: finite reflected Gram block, normalized quotient block, projection \(P\), rank-one vector \(e\), coefficient matrices \(H,K,A,C\), null vector \(z\), endpoint incidence tensor, finite margin intervals, and same-theory normalization factor.
- Preserved invariants: finite regulator, same Wilson observable algebra, reflection-positive Gram interpretation, source-collision versus geometric-collar distinction, diagonal congruence versus pair-dependent quotient distinction, two-sided error status, and body/appendix claim boundary.
- Broken invariants: importing source-collision \(H,K\) into geometric-collar claims, treating entrywise division as positivity preserving, reading nonnegativity as strict margin, using one-sided endpoint estimates as negative certificates, or letting a CAS equality become a continuum or mass-gap claim.
- Edge case or counterexample: the equicorrelation matrix with off-diagonal \(1/2\) is PSD, but its entrywise inverse has off-diagonal \(2\) and is indefinite; this blocks unsupported quotient normalization.

## Epistemic Discipline

Assign epistemic status to each symbolic result: `exact_symbolic_certificate`, `finite_counterexample`, `conditional_gate`, `certified_finite_margin`, `paper_safe_lemma`, `proof_obligation`, `blocked`, `demoted`, or `explicit_unknown`.

Cite evidence through manuscript labels, source TeX paths, deterministic script outputs, JSON report paths, exact formulas, validator outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum boundary. A CAS certificate can support a finite theorem or obstruction, not a continuum Yang--Mills construction or mass-gap claim.

## Codex Exec Protocol

Follow `docs/reference/codex-exec-skill-protocol.md` when running symbolic scripts. Execute the smallest deterministic run that checks the formula in question, inspect the output artifact, and then add a generative mathematical interpretation. Record executed commands and artifact inspection when reporting results.

Do not leave deterministic run output uninterpreted. If the CAS report verifies a formula, state what manuscript claim it supports and what it does not support. If it finds an obstruction, state which open module is demoted or which proof obligation remains.

## Output Contract

Return:

1. `Symbolic Target`: module, manuscript section, matrix family, and finite/geometric/endpoint status.
2. `Definitions And Assumptions`: variables, projections, observables, normalization, error model, and validity regime.
3. `CAS Or Exact Audit`: command, report path, exact formulas checked, and pass/fail status.
4. `Paper-Level Interpretation`: theorem/proposition/lemma/certificate/demotion wording.
5. `Claim Boundary`: finite-only, conditional, geometric-collar, endpoint, continuum, or spectral non-claim.
6. `Proof Obligations`: remaining analytic estimates, same-theory certificates, path data, error bounds, or prior-art checks.
7. `Validation Handoff`: next Route A skill, local validator, TeX integration step, or unresolved open module.

## Failure/Demotion

Demote if the audit does not name the matrix family, if CAS output is not inspected, if finite algebra is promoted into continuum evidence, if source-collision variables are reused as geometric coefficients, if one-sided endpoint bounds are used for negative claims, or if manuscript prose contains process language rather than mathematical result language.
