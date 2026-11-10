<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Nearest-Literature Anchor Table

- Status: `implemented`
- Purpose: convert the literature criticism into claim boundaries.
- Decision: the draft can claim a batched static-lookup lower-bound package for structured inputwise certificates, displayed acyclic ER-style proof objects, expansion-bounded compressed ER objects, macro-compressed ER objects, support-declared macro ER objects, support-audited LRAT traces, provenance-typed LRAT traces, namespace-typed LRAT antecedent-closure traces, strict-prefix Qrep replay objects, trace-complete DPLL decision logs, antecedent-complete CDCL learned-clause logs, CDCL antecedent-erasure trichotomy, RUP-complete CDCL support normalization, and support-audit/provenance separators, but not a new general hardness-magnification theorem, not an unrestricted SAT lower bound, and not a lower bound for arbitrary strong, raw RUP/DRUP without support parsing, arbitrary CDCL without a positive non-plain invariant, or compressed proof systems.

## Anchor Table

| Draft object | Nearest established objects | What is shared | Possible novelty delta | Required claim reset |
|---|---|---|---|---|
| Formula-label hardness predicate | Partial MCSP, partial Boolean functions, nondeterministic certificate complexity | A partial labeling is sound only if every completion avoids small circuits. | The generator-induced variable set and batched lookup argument count distinct generated formulas of both polarities nearly at the threshold. | Do not claim a new meta-complexity problem unless the predicate is compared directly to Partial MCSP instances. |
| Batched formula-footprint theorem | Static dictionary lookup, sorting-network circuits, certificate lower bounds | A small exception set gives a cheap completion circuit by hardwiring the exceptions. | The shared dictionary across the whole generated batch improves the naive `M K ell` comparison to near-linear batch-plus-dictionary size. | Present this as the main technical contribution. |
| Labeled points excluding small circuits | Circuit test suites, anti-checkers, lower-bound refuters | A small set of labeled examples can rule out a hypothesis class. | The paper asks for examples that force high circuit complexity under all completions of a generator-induced source function. | Add a paragraph saying the theorem is a certificate lower bound for a structured refuter, not a general test-suite theory. |
| Inputwise certificates | Decision-tree certificate complexity, exact certification, teaching/specification dimension | A certificate fixes enough coordinates to force membership in a concept/property class. | The row/quotient structure gives polarity and row forcing lower bounds for a specific induced-hardness property. | Use standard certificate-complexity language and avoid implying a new proof-complexity measure. |
| Occurrence row forcing | Aggregator certificate complexity, sparse-row patching | If unforced rows can be completed to a constant value, a small exceptional row set is patchable. | The theorem cleanly separates source-row count from aggregator forcing numbers. | Keep as a supporting lemma unless matched by examples or proof-system extraction. |
| Equality quotient | Partial functions under equality constraints, affine images/codes | Equality links restrict completions to an affine subspace before applying sparse patching. | The quotient theorem states residual distance from both constants after sound equality identifications. | State that nonlinear SAT semantics and self-reduction are not covered. |
| Nonlinear semantic relation support | SAT self-reduction, local relation certificates, constrained partial assignments | A semantic proof may impose local Boolean relations between formula labels. | The semantic-relation support theorem shows that a support-local audit must contain a standard relation-membership certificate for each imposed relation instance; for \(y=y_0\vee y_1\), unsat branches require parent and both children.  The acyclic OR-tree theorem gives the eliminated-frontier certificate for bounded OR self-reduction trees, and the OR-DAG theorem shows that sharing and repeated reachable frontier formulas do not change the cost after sound quotienting. | Do not claim a full residual-completion theorem for hidden, learned-clause, cyclic, or arbitrary SAT self-reduction closures. |
| Exposed Boolean and adaptive semantic frontiers | Boolean certificate complexity, decision-tree and branching-program certificate complexity, SAT self-reduction frontiers, semantic proof influence | Once a finite acyclic semantic frontier, adaptive decision tree, or adaptive branching program is exposed, support soundness is ordinary certificate soundness for the induced Boolean function. | The acyclic Boolean frontier theorem identifies support-locality with the root coordinate plus pointwise certificate complexity of the exposed frontier circuit; the visible-adaptive theorems add that logged transcript or computation paths are sufficient only because the full adaptive control object is checker-visible; the hidden-transcript separator shows that an uncertified transcript summary alone can mask all-frontier OR support. | Do not claim hidden adaptive SAT self-reduction closure unless the frontier circuit or adaptive control object, quotienting, and support budget are checker-visible. |
| Strict-prefix Qrep replay | Quotient compression, proof-carrying rewriting, proof certificates for equivalence, compressed proof objects | A proof may replace a local object by a representative after proving same-theory equivalence. | The Qrep proposition makes the temporal support condition explicit: quotient compression is transparent only when the same-theory certificate forest is displayed and charged before first representative use. | Do not count delayed quotient certificates, representative rebinding, or advice-chosen representatives as transparent support. |
| SAT parity carrier | Hardness magnification, beta-zero substitution, MCSP/MKtP carrier attempts | A source lower bound for a polylog-query SAT carrier could transfer to a SAT lower bound. | The paper factors out local certificate costs conditional on such a source lower bound. | Demote to calibration unless an explicit hard source theorem is added. |
| Proof-system motivation | Frege, Extended Frege, IPS, implicit proofs, DPLL/CDCL proof logs, proof-to-circuit connections | Strong proof systems and solver traces may encode semantic information nonlocally. | Restricted extraction and normalization routes are proved for explicit/support-local interfaces, acyclic syntactic cones, final backward slices, slice-explicit ER-style size measures, ordinary displayed acyclic ER length, expansion-bounded compressed ER, macro-compressed ER, support-declared macro ER, support-audited LRAT traces, provenance-typed LRAT traces, namespace-typed LRAT antecedent-closure traces, strict-prefix Qrep replay, trace-complete DPLL decision logs, antecedent-complete CDCL learned-clause logs, CDCL antecedent-erasure trichotomy, RUP-complete CDCL support normalization, canonical-namespace RUP-CDCL standardization, support-audit necessity, support-erasure indistinguishability, and plain LRAT extraction trichotomy; no arbitrary strong, arbitrary CDCL without learned-clause antecedent provenance or RUP-complete parsed support traces, raw RUP/DRUP without support parsing or manifest, plain unaudited or untyped LRAT/DRAT, or compressed standard-system lower bound follows without proving controlled expansion, adding namespace/provenance/support parsing or a system-specific invariant, or proving a sound support-local budget. | Keep proof-size lower-bound rhetoric conditional on a concrete budget theorem for a recognizable compressed or less-local system. |
| Dense functional certificates | Natural proofs and constructive lower bounds | A constructive, large, useful property enters the natural-proofs regime. | Sparse local certificates may avoid largeness, but this does not itself prove a lower bound. | Keep the naturalization proposition as a boundary observation. |

## Citations Already Present In The Draft

- Certificate complexity and decision trees: Nisan; Buhrman and de Wolf.
- Sorting networks and batched lookup substrate: Batcher; Ajtai, Komlos, and Szemeredi.
- Hardness magnification: Oliveira and Santhanam; Oliveira, Pich, and Santhanam; McKay, Murray, and Williams; Chen, Hirahara, Oliveira, Pich, Rajgopal, and Santhanam; Atserias and Muller.
- Natural proofs and constructive lower bounds: Razborov and Rudich; Carmosino, Impagliazzo, Kabanets, and Kolokolova.
- Strong proof systems and nonlocal proof information: Krajicek; Arteche, Khaniki, Pich, and Santhanam.

## Citation Status

The current draft now contains direct references, with bibliographic details checked, for the four nearest-literature buckets that previously appeared as citation debt:

- Partial MCSP and promise/partial-function versions of circuit-size membership: Hirahara, FOCS 2022.
- Circuit test suites and anti-checkers as lower-bound refuter analogues: Chapman and Williams, ITCS 2015.
- Teaching dimension, specification dimension, and exact certification from examples: Anthony--Brightwell--Cohen--Shawe-Taylor, COLT 1992; Doliwa--Fan--Simon--Zilles, JMLR 2014.
- Lower-bound refuter formulations where labeled examples exclude all small circuits: covered by the circuit-input game/test-suite comparison and the exact-specification comparison.

Remaining bibliography work is style-level only unless a new theorem adds a new nearest-neighbor literature class.

## Novelty Delta Accounting

The revised paper now includes a novelty-delta accounting matrix in the related-work section.  This is the bridge between C7 literature closure and C11 cohered results:

| Paper object | Before this paper | After this paper | C11 role |
|---|---|---|---|
| Formula-footprint barrier | Certificates fix examples or partial-function bits, but generated formula labels and repeated generated objects are not separated from source inputs. | A two-polarity footprint lower bound forces many distinct generated labels under all completions; batched lookup supplies the near-threshold count. | `flagship` |
| Identity-carrier sharpness | The lower bound might be a proof artifact without a matching ordinary carrier. | Generic truth-table carriers have certificates matching the lower bound up to polylogarithmic factors. | `calibration` |
| Row and quotient interfaces | Sparse patching gives coarse lower bounds for unfixed rows or coordinates. | Source rows, output polarities, and quotient residual distance become separate interfaces of the same completion obstruction. | `interface_variant` |
| Semantic frontiers and adaptive certificates | Local semantic constraints can be invoked without charging a visible support object. | Exposed frontiers reduce to ordinary certificate complexity; hidden transcripts are separated from sound support audits. | `boundary` |
| Proof-object bridges | Proof traces may or may not reveal the local atoms needed by the certificate lower bound. | Support-local normalizers and audit criteria state exactly when proof size inherits the formula footprint lower bound. | `proof_system_bridge` |

Before/after understanding shift: completion-sound evidence that a generated labeling is hard must either expose a large local footprint, or supply an auditable proof-system mechanism that computes the same footprint from the proof artifact.

## Claim Boundary

The literature boundary closes the superficiality objection only if the paper states:

1. The batched formula-footprint theorem is the main technical novelty.
2. Row forcing and quotient distance are supporting structural lemmas.
3. The SAT section is a conditional calibration.
4. Proof-complexity claims require a separate extraction theorem.
5. Exposed acyclic semantic frontiers and checker-visible adaptive decision-tree or branching-program frontiers reduce to ordinary Boolean certificate complexity, but hidden adaptive SAT semantics still require a separate support theorem; transcript summaries alone are separated from sound support audits.
6. The draft is not a new general hardness-magnification theorem.
