# Discovery Process Slides for p-vs-np

_Audience: external mathematical experts. These slides summarize the current discovery process after the present `work` + `meta` round._

---

# Slide 1 - Current Discovery State

**Takeaway**  
After the current `work` + `meta` round, the programme is organized, auditable, and still open.

## Narrative

- We have completed 1 outer work cycle(s); the latest phase was `discovery` and the next phase is `prove`.
- The current plausibility score is 0.469; the system does not detect a plausible full proof yet.
- The current proof state should be read as a conditional research programme rather than as a near-complete proof.

## Concrete Examples

- Latest work result: Queued or refreshed 6 proof targets (added=0, updated=6).
- Meta judgment: The discovery process has genuinely improved understanding of where the problem is hard, but it has not yet produced evidence that the main conjecture is close to resolution.

---

# Slide 2 - Why The Problem Is Still Hard

**Takeaway**  
The framework now localizes the difficulty more sharply, but the essential hardness remains cross-regime transport under low evidence.

## Narrative

- p-vs-np is hard in this KB because global targets are framed across multiple incompatible proof regimes, barrier theorems restrict generic techniques, and explicit dependencies are sparse, forcing hypothesis-driven bridge construction.
- The current route still requires movement from a weak-model lower bound regime to a stronger separation consequence through a bridge object rather than by direct deduction.
- The bridge portfolio names the carrier as `MCSP witness family`, while the selected proof sketch currently operationalizes the route through `Gap-MCSP promise problem`. This is an unresolved representation shift inside the current macro-proof state, not a proved equivalence.

## Concrete Examples

- Direct proof aspiration has been replaced by a sharper nonuniform target.
- The current route still depends on a bridge object rather than a direct deduction from the KB.

---

# Slide 3 - What Changed In Framing

**Takeaway**  
The search no longer treats `P != NP` as a single undifferentiated target.

## Narrative

- The main conjecture is `P != NP`, but the active route target is `NP not in P/poly`.
- This is a real perspective shift: the search first tries to prove a stronger nonuniform consequence and only then closes back to the central conjecture.
- The decisive bottleneck is the leading magnification bridge. The final reduction from the nonuniform target to the main conjecture is already available, so the strategic question is whether the bridge object can be fixed and the source-realization, transport, route, and payoff lemmas can be discharged.

## Concrete Examples

- Grounding implication: If NP is not contained in P/poly, then P != NP.
- Leading route target: major consequences such as NP not in P/poly

---

# Slide 4 - New Concepts Introduced By The Search

**Takeaway**  
The discovery process is not only ranking statements; it is adding a more explicit conceptual vocabulary for the route.

## Narrative

- Connector and conjecture stages surfaced concrete target concepts, bridge objects, and invariants that did not appear as the primary unit of reasoning at the start.
- The key gain is that the route is now discussed through carriers and invariants rather than only by thematic similarity.

## Concrete Examples

- Target concepts: mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound, proof-lower-bounds-imply-circuit-lower-bounds, poly-bounded-proofs-iff-NP-equals-coNP
- Bridge objects: unspecified transport normal form, Gap-MCSP promise problem, unspecified reduction gadget family, unspecified promise-gap problem
- Leading bridge object: MCSP witness family
- Preserved invariant: MCSP complexity profile in nonuniform-circuits

---

# Slide 5 - New Connections Made Explicit

**Takeaway**  
The main novelty is in theorem-pair-specific connections, not generic topic clustering.

## Narrative

- The current bridge portfolio spells out concrete source-to-target routes together with what is supposed to be transported.
- These are inspectable research programmes because each route comes with a carrier, an invariant, and a missing route lemma.

## Concrete Examples

- Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-pich-santhanam-magnification-near-state` in model `nonuniform-circuits` to obtain `major consequences such as NP not in P/poly`.
- Adjacent route: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.oliveira-santhanam-hardness-magnification-for-na` in model `formula-size` to obtain `major lower bounds for NP in much stronger models (including superpolynomial formula/circuit lower bounds, and in some parameter...`.
- Generalization route: Move from `st.def.hardness-magnification-phenomenon-programme-leve` on problem `MCSP` in model `nonuniform-circuits` using `A barely-nontrivial lower bound for an explicit problem Q in a weak model` toward `st.thm.atserias-m-uller-simple-general-magnification-fr` to obtain `There exist general-purpose magnification theorems (not problem-specific) showing that certain mild lower bounds for...`.

---

# Slide 6 - How The Discovery Process Evolved

**Takeaway**  
The process moved from broad structural targeting to bridge design, then to typed conjectures, then to theorem-sized proof obligations.

## Narrative

- Stage 1 identified high-pressure targets and intervention points in the concept graph.
- Stage 2 converted those targets into bridge programmes with explicit missing interfaces.
- Stage 3 conjectured candidate objects and Stage 4 formalized them into proof sketches and queue items.

## Concrete Examples

- Connect stage headline: targets mild-lower-bounds-imply-major-separation, MCSP-near-threshold-nonuniform-circuit-lower-bound
- Bridge-plan headline: Move from `st.def.item-5` in model `nonuniform-circuits` using `P/poly is the class of languages L decidable by polynomial-size Boolean circuit families, equivalently by polynomial-time Turing...` toward `st.thm.williams-improved-exhaustive-search-circuit-lowe` on problem `SAT` in model `nondeterministic-verifier` t...; invariants nonuniform-circuit-lower-bound witness complexity, MCSP complexity profile in nonuniform-circuits
- Conjecture headline: Move from `st.thm.karp-many-natural-problems-are-np-complete-karp1` using `NP-complete under polynomial-time many-one reductions` toward `st.thm.murray-williams-non-np-hardness-of-mcsp-under-lo` on problem `MCSP` to obtain `is not NP-complete. More broadly, the paper develops evidence and conditional consequences su...; bridge objects unspecified transport normal form, Gap-MCSP promise problem
- Proof-sketch examples: MCSP witness family via strat.001, unspecified witness family via strat.002, Gap-MCSP promise problem via strat.001

---

# Slide 7 - What The Queue Now Means

**Takeaway**  
The frontier is no longer a vague backlog; it is a queue of theorem-shaped claims that can be proved, disproved, or blocked.

## Narrative

- The proof queue currently contains 6 pending items.
- Each item states a self-contained route conjecture, attaches a missing route lemma, and exposes proof obligations and failure logic.
- This is the main operational outcome of the `work` cycle so far.

## Concrete Examples

- MCSP witness family: major consequences such as NP not in P/poly
- There exists an admissible MCSP witness family, realized as a family of instances equipped with a monotone witness measure, such that whenever A barely-nontrivial lower bound for an explicit problem Q in a weak model holds for MCSP in nonuniform-circuits, the object organizes the source-side mathematical content while preserving the invariant MCSP complexity profile in nonuniform-circuits and yields major consequences such as NP not in P/poly.
- Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

---

# Slide 8 - What Still Blocks Completion

**Takeaway**  
The open problem is now narrower, but the missing mathematics is still substantial.

## Narrative

- The bridge portfolio names the carrier as `MCSP witness family`, while the selected proof sketch currently operationalizes the route through `Gap-MCSP promise problem`. This is an unresolved representation shift inside the current macro-proof state, not a proved equivalence.
- Current signals remain weak at the terminal level: evidence_count=0, proved_count=0, plausible_solution_detected=False.
- The macro-proof has a coherent leading route and a grounded implication to the main conjecture, but it remains conditional. The unresolved mass sits in the bridge object, the route lemma, and the absence of external evidence or discharged proof obligations.

## Concrete Examples

- No terminal proved attempts yet.
- Evidence count remains 0.
- Current bottleneck: Prove that a hardness-magnification witness family turns `A barely-nontrivial lower bound for an explicit problem Q in a weak model` into `major consequences such as NP not in P/poly` while preserving `MCSP complexity profile in nonuniform-circuits`.

---

# Slide 9 - How An External Expert Should Read The State

**Takeaway**  
This is already expert-inspectable, but it is not yet expert-endorsable as a proof claim.

## Narrative

- An external expert should read the current state as a conditional macro-proof programme with concrete bridge objects and explicit failure points.
- The right expert question is no longer 'what topic should we try?' but 'is this bridge object mathematically real, and can the route lemma be discharged or ruled out?'
- What changed is the granularity of the problem: the search now isolates a sharper target, a typed carrier, a representation defect, and a queue of inspectable obligations. What persists is the absence of terminal proof evidence, adversarial stress, and representation closure.

## Concrete Examples

- Inspect first: MCSP witness family versus Gap-MCSP promise problem.
- Inspect first: the source-to-object lemma and the transport claim.
- Supported but not decisive: phyp.p-vs-np.042, phyp.p-vs-np.033, phyp.p-vs-np.034

---

# Slide 10 - Next Governing Question

**Takeaway**  
The next cycle should be governed by one sharp mathematical question, not by generic additional search.

## Narrative

- Should the next cycle try to close the leading bridge representation defect, or should it seek a barrier result showing that one operationalization cannot realize the route as currently stated?
- The next outer-loop phase is `prove`, so the system is ready to consume the highest-priority queued route.
- The best immediate use of expert time is to either close the representation defect or to derive a barrier result that compresses the search space.

## Concrete Examples

- Primary route: bridge.001 toward NP not in P/poly.
- Next best stress test: bridge.002 through the nonuniform-circuits -> formula-size transfer.
