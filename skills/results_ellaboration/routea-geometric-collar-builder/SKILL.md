---
name: routea-geometric-collar-builder
description: Attack Route A module G1 by constructing or refuting a cutoff-indexed geometric collar family for the SU(2) Wilson-block paper. Use when the paper needs explicit lattice paths gamma_{+,k}(delta), gamma_{-,k}(delta), gamma_{0,k}(delta), positive-time support, reflection pairing, locked boundary footprint, and joint cutoff/collar scaling.
---

# Route A Geometric Collar Builder

## Mathematical Target

Build an explicit family of lattice paths
\[
\gamma_{+,k}(\delta),\qquad \gamma_{-,k}(\delta),\qquad \gamma_{0,k}(\delta)
\]
on a finite four-dimensional lattice with spacing \(a_k\), satisfying:

- positive-time support for every edge of the positive algebra observable;
- reflected pairing \(\rho\gamma_{+,k}(\delta)=\gamma_{-,k}(\delta)\);
- invariant central channel \(\rho\gamma_{0,k}(\delta)=\gamma_{0,k}(\delta)\);
- locked reflection-plane footprint independent of collar sign;
- physical scaling \(a_kr_k\to R\), \(a_ks_k\to S\), \(a_kh_k\to H\), \(a_km_k(\delta)\to\delta\).

## Attack Procedure

1. Reconstruct the paper's existing hairpin geometry and time-reflection convention.
2. Define a coordinate model for vertices and directed edges before attempting prose.
3. Propose explicit edge lists for \(+\), \(-\), and \(0\) channels.
4. Check support: every non-reflected observable must lie in \(t\ge1\), or the base time must be shifted and recorded.
5. Check footprint locking: compute the intersection with the reflection boundary and compare across channels.
6. Check reflection: apply \(\rho\) to every edge and verify the image path.
7. Decide promotion:
   - promote to a paper lemma only if all checks pass;
   - otherwise emit the smallest obstruction and a revised construction attempt.


## Epistemic Discipline

Treat each manuscript result as a mathematical object with an explicit epistemic status: proved, certified finite, conditional, conjectural, blocked, or demoted. Cite evidence through source artifacts, paper labels, validation reports, deterministic script outputs, or explicit unknowns. Preserve the finite/geometric/endpoint/continuum claim boundary, and end with a validation handoff or unresolved obligations.

## Output Contract

Return: coordinate conventions, edge-list definitions, scaling assumptions, support proof, footprint proof, reflection proof, obstruction if any, and manuscript lemma/proof text or demotion text.

## Failure/Demotion

Demote if the construction requires different boundary footprints for different collar signs, leaves the positive-time algebra, hides an order-of-limits assumption, or merely says a collar should exist without edge lists.
