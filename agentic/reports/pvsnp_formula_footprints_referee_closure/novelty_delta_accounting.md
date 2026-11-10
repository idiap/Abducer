<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Novelty Delta Accounting

- Status: `integrated_in_revised_tex`
- TeX section: `Related work and open directions`
- Criteria served: `C7`, `C10`, `C11`
- Purpose: make the novelty claim auditable against nearby literature and keep the result package coherent rather than a fragmented ensemble.

## Accounting Rule

Every theorem-level contribution must declare four things:

1. the closest established object or literature family;
2. the shared mathematical feature;
3. the novelty delta in this paper;
4. the role it plays in the flagship formula-footprint arc.

A contribution passes this rule only if the delta changes the reader's
understanding of completion-sound local certificates for generated hardness
predicates.  A locally correct addition that needs a separate motivation fails
the C11 cohered-results gate even if it has a plausible proof.

## Novelty Delta Matrix

| Paper object | Closest literature object | Before this paper | After this paper | Role in the flagship arc |
|---|---|---|---|---|
| Formula-footprint barrier | Certificate complexity, Partial MCSP, circuit test suites | A certificate fixes examples or partial-function bits, but generator-induced formula labels and repeated generated objects are not separated from source inputs. | A two-polarity footprint lower bound says a completion-sound certificate must expose many distinct generated labels; the batched dictionary lemma is the quantitative engine. | `flagship` |
| Identity-carrier sharpness | Counting lower bounds against small circuits | Generic hard truth tables need finite distinguishing sets, but the formula-footprint lower bound could have been an artifact of the proof. | In the standard identity carrier, generic certificates match the lower bound up to polylogarithmic factors. | `calibration` |
| Row and quotient interfaces | Decision-tree certificate complexity, equality-constrained partial functions | Sparse patching gives coarse lower bounds for unfixed rows or coordinates. | The paper separates source rows, output polarities, and sound quotient residual distance as different interfaces of the same completion obstruction. | `interface_variant` |
| Semantic frontier and adaptive certificates | Boolean certificate complexity, decision trees, branching programs, SAT self-reduction frontiers | Local semantic constraints can be invoked informally without charging the exposed support object. | Exposed finite frontiers reduce to ordinary pointwise certificate complexity, while hidden transcript summaries are separated from sound support audits. | `boundary` |
| Proof-object bridges | Resolution, ER-style syntax, LRAT/DRAT/RUP/CDCL traces, implicit proofs | Proof traces may or may not reveal the local semantic atoms needed by a certificate lower bound. | Support-local normalizers, provenance/namespace conditions, strict-prefix replay, RUP-complete support audits, the carrier-independent audit criterion, the self-auditing RUP-CDCL instantiation, the append-only deletion-free refinement, and the prefix-typed append-only refinement state exactly when proof size inherits the footprint lower bound and which typed audit fields remain essential. | `proof_system_bridge` |

## Before/After Understanding Shift

This section records the before/after understanding shift required by C11.

Before the revision, the draft could be read as a collection of related lower
bounds, SAT-calibration observations, and proof-complexity motivations.  After
the novelty-delta accounting pass, the paper has a single thesis:

> Completion-sound evidence that a generated labeling is hard must either expose
> a large local footprint, or supply an auditable proof-system mechanism that
> computes the same footprint from the proof artifact.

The literature comparison is therefore not an appendix-level defense.  It is
part of the result: it explains why the paper is not claiming a new general
magnification theorem, not claiming a Partial MCSP theorem, and not claiming a
Frege/Extended-Frege/IPS lower bound, while still isolating a new and reusable
certificate obstruction.

## Admission Consequence

Future additions are admissible only if they strengthen one of the five roles:
`flagship`, `calibration`, `interface_variant`, `proof_system_bridge`, or
`boundary`.  A new lemma that merely adds another proof object without changing
the novelty delta, the before/after shift, or the proof-system bridge should be
quarantined from the main paper.
