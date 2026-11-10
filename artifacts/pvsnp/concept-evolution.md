# Evolution of Concepts and Results in `KB/p-vs-np.kb.md`

## Scope

This description summarizes how the P vs NP knowledge base evolves conceptually from foundations to current frontier programmes, using statement IDs already present in the KB.

## 1) Foundational language of complexity

The KB begins by fixing the core vocabulary of tractability, verifiability, and reductions:

- Reductions and classes: `st.def.polynomial-time-many-one-karp-reduction`, `st.def.item` (P), `st.def.item-2` (NP), `st.def.item-3` (coNP), `st.def.np-completeness`, `st.def.polynomial-hierarchy`, `st.def.exponential-time-classes`, `st.def.item-4` (BPP).

This phase establishes that P vs NP is not an isolated question but part of a structured hierarchy where reductions transfer hardness and class inclusions/collapses matter.

## 2) First major milestone: NP-completeness landscape

The first global result layer is the NP-completeness canon:

- `st.thm.cook-levin-sat-is-np-complete-cook1971`
- `st.thm.karp-many-natural-problems-are-np-complete-karp1`

Conceptual shift: the question moves from “single hard problem” to a universality thesis where many natural problems share one hardness core.

## 3) Nonuniform reformulation as a proof target

The KB then pivots from uniform machines to circuit families:

- Circuit definitions: `st.def.boolean-circuit-and-size-depth`, `st.def.circuit-family-s-n`, `st.def.item-5` (P/poly).
- Target theorem: `st.thm.nonuniform-separation-target` (NP not subset P/poly implies P != NP).

Conceptual shift: proving P != NP is reframed as proving strong circuit lower bounds.

## 4) Unconditional lower bounds in restricted models

The KB records strong but model-limited successes:

- `st.thm.h-stad-near-optimal-0-lower-bounds-for-parity-ha`
- `st.thm.razborov-smolensky-0-p`
- `st.thm.monotone-lower-bounds-for-clique-exemplar-razbor`

Conceptual shift: lower-bound machinery works deeply in restricted classes, but full P/poly separation remains out of reach.

## 5) Barrier era: limits of common proof templates

The next phase formalizes why many direct strategies fail:

- Relativization barrier: `st.thm.baker-gill-solovay-relativisation-barrier-bakerg`
- Natural proofs barrier: `st.thm.razborov-rudich-natural-proofs-barrier-razborovr`
- Algebrization barrier: `st.thm.aaronson-wigderson-algebrisation-barrier-aaronso`

Conceptual shift: progress criteria become “barrier-aware”; methods must evade known impossibility templates.

## 6) Algorithms-to-lower-bounds transfer

A modern transition in the KB is the Williams programme:

- `st.thm.williams-nonuniform-0-lower-bounds-for-williams2`
- `st.thm.williams-improved-exhaustive-search-circuit-lowe`

Conceptual shift: algorithmic improvements can force circuit lower bounds, linking constructive algorithm design to separation goals.

## 7) Derandomization and PIT as a structural bridge

The KB then integrates pseudorandomness and identity testing:

- Definitions: `st.def.polynomial-identity-testing-pit`, `st.def.hitting-set-for-pit-black-box`, `st.def.pseudorandom-generator-prg-against-circuits`, `st.def.pseudorandom-function-prf-informal`.
- Core theorems: `st.thm.kabanets-impagliazzo-pit-derandomisation-implies`, `st.thm.nisan-wigderson-hardness-vs-randomness-nisanwigd`, `st.thm.impagliazzo-wigderson-e-hardness-nonuniform-form`.

Conceptual shift: randomness removal and lower bounds become two faces of one agenda.

## 8) Proof complexity as a parallel route

Another branch ties propositional proof size to circuit complexity:

- `st.thm.cook-reckhow-proof-systems-and-cookreckhow1979`
- `st.thm.resolution-php-lower-bounds-exemplar-buss1988`
- `st.thm.bounded-depth-frege-php-lower-bounds-beamepitass`
- `st.thm.grochow-pitassi-ips-ties-proof-lower-bounds-to-a`

Conceptual shift: separating proof systems can imply arithmetic/Boolean circuit lower bounds, giving an orthogonal route to core separations.

## 9) Meta-complexity and hardness magnification phase

The KB’s newest frontier emphasizes "small lower bound -> big consequence" transfers:

- `st.def.minimum-circuit-size-problem-mcsp`, `st.def.gap-mcsp`, `st.def.mktp-mktp-time-bounded-kolmogorov-meta-problem`.
- `st.thm.oliveira-santhanam-hardness-magnification-for-na`
- `st.thm.oliveira-pich-santhanam-magnification-near-state`
- `st.thm.atserias-m-uller-simple-general-magnification-fr`
- `st.thm.hirahara-ilango-np-hardness-of-mcsp-from-well-st`
- `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo`

Conceptual shift: effort concentrates on explicit meta-problems where modest progress may unlock major separations.

## 10) Communication/lifting unification layer

The KB adds communication complexity and lifting frameworks:

- `st.def.deterministic-communication-complexity`
- `st.def.deterministic-decision-tree-complexity`
- `st.def.composition-with-a-gadget-lifting-set-up`
- `st.thm.g-o-os-pitassi-watson-and-coauthors-query-to-com`

Conceptual shift: lower bounds are transferred across models (query -> communication -> proofs/circuits), enriching reusable proof pathways.

## Current KB state and trajectory

- The KB now has broad conceptual coverage (64 canonical statements) but sparse explicit dependency wiring (`depends_on` edges are mostly absent).
- Because of this, the active evolution has moved from "collect statements" to "connect statements":
  - relational analysis: `artifacts/pvsnp/connection-analysis.json`
  - proof-hypothesis set: `phyp/p-vs-np.proof-hypotheses.yaml`

Highest-priority current hypotheses (examples):

- `phyp.p-vs-np.001`: bridge from Adleman-style nonuniformity context toward Williams ACC0 lower-bound target.
- `phyp.p-vs-np.002` and `phyp.p-vs-np.003`: bridge barriers/collapse results into the nonuniform separation target.
- `phyp.p-vs-np.004`: bridge polynomially-bounded proof-system definition into Cook-Reckhow equivalence theorem.

Overall evolution pattern: foundational class theory -> completeness theory -> circuit/nonuniform targeting -> barrier awareness -> transfer theorems (algorithms, PIT, proofs, communication) -> magnification/meta-complexity -> hypothesis-driven connection search.
