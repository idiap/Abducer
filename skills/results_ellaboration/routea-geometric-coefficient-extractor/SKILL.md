---
name: routea-geometric-coefficient-extractor
description: Attack Route A module G3 by deriving the first and second geometric-collar coefficients H_k and K_k and the operator-norm remainder from the same normalized Wilson block. Use when the paper needs to move beyond source-amplitude collision into a genuine geometric-collar Schur--Feshbach theorem.
---

# Route A Geometric Coefficient Extractor

## Mathematical Target

Derive, from the same normalized collar block \(q_{k,\delta}\),
\[
q_{k,\delta}
=\one\one^T+\delta H_k+\delta^2K_k+R_{k,\delta},
\qquad
\sup_k\frac{\norm{R_{k,\delta}}}{\delta^2}\to0.
\]

This must not reuse the source-collision \(H,K\) as if they were geometric derivatives.

## Attack Procedure

1. Define the exact entry \(q_{k,\delta}(i,j)\) as a Wilson expectation after G1/G2.
2. Decide whether to expand \(q_{k,\delta}\) or \(\log q_{k,\delta}\); state the conversion.
3. Compute first variations and identify one-body terms killed by \(P\).
4. Compute second variations and separate genuine \(PK_kP\) from Schur correction terms.
5. Bound the remainder in operator norm, not only entrywise formal notation.
6. Apply the rank-one Schur--Feshbach reduction:
\[
A_k=PH_kP,\qquad
C_k=P\left(K_k-\frac1nH_kee^*H_k\right)P.
\]
7. Decide whether the paper earns a theorem, a conditional theorem, or a demotion.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: entry definitions, expansion choice, \(H_k\), \(K_k\), remainder bound, reduced \(A_k,C_k\), proof obligations, and manuscript theorem/demotion text.

## Failure/Demotion

Demote if \(H_k,K_k\) are not computed from the geometric block, the remainder is formal rather than controlled, or the Schur correction is omitted.
