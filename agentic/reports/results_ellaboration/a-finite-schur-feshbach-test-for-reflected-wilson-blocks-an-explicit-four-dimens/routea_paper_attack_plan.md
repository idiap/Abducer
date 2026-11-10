<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Route A Paper Attack Plan

## Diagnosis

The last paper draft now describes the open modules in useful physics and mathematics language, but that is not enough. The next layer must try to discharge those modules. The decisive question is whether the finite source-collision Wilson block can be upgraded into a genuine geometric-collar Route A theorem without leaving the same regulated \(SU(2)\) heat-kernel theory.

The current finite result is solid: the reflected Gram block, diagonal normalization, Schur--Feshbach correction, determinant, and reduced margins are exact at finite cutoff. The unresolved work begins where the paper asks for geometric variation, renormalized same-theory normalization, coefficient extraction, strict cutoff margins, endpoint estimates, and eventually continuum/spectral handoffs.

## Strategic Ordering

1. **G1: geometric collar construction.** This is the first hard gate. Without explicit cutoff-indexed paths, positive-time support, reflection pairing, locked footprint, and \(a_k,\delta\) scaling, there is no geometric-collar object to normalize or expand.
2. **G2: same-theory normalization.** A collar geometry is useless for the Schur--Feshbach test if normalization leaves the reflected Gram class. Pair-dependent entrywise quotients must be certified or demoted.
3. **G3: geometric coefficient extraction.** The paper needs \(H_k,K_k\) and an operator-norm remainder from the geometric collar itself, not from the source-amplitude construction.
4. **G4: strict margins.** Only after \(H_k,K_k\) are meaningful do cutoff-dependent \(\sigma_k,\tau_k\) lower bounds become well typed.
5. **E1/E2: endpoint estimates.** Endpoint work should depend on actual paths, not a free-standing incidence ansatz.
6. **M1/M2: continuum and spectral gatekeeping.** These remain claim-boundary modules unless earlier results supply a same-theory bridge.

## New Skills

- `routea-paper-attack-orchestrator`: chooses the active Route A module and enforces dependency order.
- `routea-geometric-collar-builder`: attempts G1 by producing explicit edge lists and proofs of support, reflection, footprint locking, and scaling.
- `routea-same-theory-normalization-certifier`: attempts G2 by classifying normalization factors and proving congruence or positive-kernel status.
- `routea-geometric-coefficient-extractor`: attempts G3 by deriving \(H_k,K_k\), the Schur correction, and the operator-norm remainder from the geometric block.
- `routea-margin-endpoint-certifier`: attempts G4/E1/E2 by certifying strict margins and same-regulator endpoint estimates with two-sided errors.
- `routea-continuum-gap-gatekeeper`: protects M1/M2 from finite-to-continuum or finite-to-gap overclaims.
- `routea-paper-result-integrator`: converts validated module artifacts into theorem, proposition, lemma, certificate, remark, or demotion text without process language in the paper.

## Concrete TODO Queue

The executable TODO queue is in:

`agentic/todos/routea_paper_attack_todos.yaml`

The queue now has a claim-boundary lock, eight mathematical module tasks, and a final paper export gate. The first three mathematical TODOs are the main route:

1. Construct or refute the explicit geometric collar path family.
2. Certify geometric-collar normalization as same-theory.
3. Derive \(H_k,K_k\) and the geometric-collar remainder from \(q_{k,\delta}\).

The endpoint and continuum tasks should not be promoted until these dependencies are resolved or explicitly demoted.

Every module has an explicit deterministic regime, generative regime, result artifact, and paper integration target. This is deliberate: deterministic checks can verify algebra, labels, support, finite matrices, TeX compilation, and forbidden-language scans, while generative work designs the geometry, proof, estimate, or demotion. No result is allowed into the paper until it passes through `routea-paper-result-integrator`.

## What Would Count As Real Progress

- A paper lemma giving explicit \(\gamma_{+,k}(\delta),\gamma_{-,k}(\delta),\gamma_{0,k}(\delta)\) edge lists with verified support and reflection properties.
- A proposition proving that every collar normalization is a same-theory congruence or positive-kernel operation.
- A theorem deriving the geometric-collar \(H_k,K_k\) and a cutoff-uniform \(o(\delta^2)\) remainder.
- A strict lower-bound theorem or certified interval protocol for the reduced margins.
- A same-regulator endpoint estimator with a two-sided error bound.

## What Should Be Demoted

- Any attempt that restates the source-collision calculation as a geometric-collar result.
- Any normalization using pair-dependent entrywise division without a positivity certificate.
- Any endpoint sign claim inferred from the null-channel incidence pattern alone.
- Any continuum or spectral statement that does not name a same-theory transfer theorem.

## Paper Integration Rule

Successful work enters the paper only as mathematics:

- definitions for new objects;
- lemmas for support, footprint, reflection, congruence, coefficient, or stencil facts;
- propositions for same-theory normalization, endpoint estimators, finite certificates, or lower-bound protocols;
- theorems only for complete constructions or estimates;
- remarks/open modules for precise demotions.

The paper body must not contain process terms such as pipeline, workflow, TODO, result-elaboration, implementation packet, agent, skill, or queue.

## Immediate Next Move

Run `routea-geometric-collar-builder` on the current paper geometry and force an object-level answer: either explicit edge lists with proofs, or a precise obstruction showing why the collar cannot be made with the present hairpin layout. Any proposed paper patch then goes through `routea-paper-result-integrator`.
