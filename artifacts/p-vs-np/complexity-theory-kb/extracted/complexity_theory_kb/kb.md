# Complexity Theory Knowledge Base

## Scope and normalization

This knowledge base systematically captures every numbered **definition, theorem, lemma, corollary, and claim** in the lecture portion of *Theory of Computation* and in the supplied chapter *NP and NP completeness*. It also adds a curated layer of unnumbered concepts and headline results needed to connect the formal statements. Exercises, proof text, examples, and solution sections are excluded unless promoted to a concept node.

- Numbered formal statements: **151** (66 theorems, 28 definitions, 47 lemmas, 6 corollaries, 4 claims).
- Curated concept/headline-result nodes: **36**.
- Total KB entries: **187**; explicit semantic relations: **20**.

Statements are restated rather than copied verbatim. Mathematical notation is normalized, PDF page numbers are retained, and the original printed page is also given.

## Source-level synthesis

The focused NP chapter develops the verifier and nondeterministic definitions of NP, polynomial Karp reductions, Cook–Levin, a web of natural NP-complete problems, search-versus-decision, coNP, and padding. Kozen places that material inside a much broader hierarchy: logspace and P completeness, PSPACE and alternation, PH, randomized and interactive computation, PCP, circuit lower bounds, logical theories, recursion theory, and the arithmetic/analytic hierarchies.

## Cross-source alignment

- **Verifier definition of NP** — `equivalent_via` → **Machine characterization of NP**. Verifier and nondeterministic-machine definitions of NP are equivalent.
- **Machine characterization of NP** — `aligns_with` → **Named complexity classes**. Both identify NP with polynomial nondeterministic time.
- **Nondeterministic time** — `aligns_with` → **Basic time and space classes**. Both define nondeterministic time classes.
- **Karp reduction, NP-hardness, NP-completeness** — `weaker_than` → **Logspace many-one reduction**. The chapter uses polynomial-time Karp reductions; Kozen often uses the stronger logspace many-one reductions.
- **Logspace reductions are polynomial-time reductions** — `explains` → **Karp reduction, NP-hardness, NP-completeness**. Every logspace many-one reduction is also a polynomial-time Karp reduction.
- **Cook–Levin theorem** — `aligns_with` → **Cook–Levin theorem, logspace form**. Both state Cook–Levin; Kozen strengthens the reduction to logspace many-one completeness.
- **NP-hardness of SAT** — `component_of` → **Cook–Levin theorem**. SAT hardness is the main hardness half of Cook–Levin.
- **Reduction from SAT to 3SAT** — `component_of` → **Cook–Levin theorem**. SAT ≤ᵖ 3SAT transfers NP-hardness from SAT to 3SAT.
- **Consequences of polynomial reductions** — `aligns_with` → **Transitivity of logspace reductions**. Both use transitivity of reductions.
- **Consequences of polynomial reductions** — `aligns_with` → **Closure under logspace reduction**. Both express closure of efficient computation under reduction.
- **P-completeness of circuit value** — `parallel_to` → **Cook–Levin theorem, logspace form**. CVP is complete for P; SAT is complete for NP.
- **PSPACE-completeness of QBF** — `uses` → **Alternation simulation theorem**. QBF membership and hardness are naturally expressed through alternation.
- **PSPACE-completeness of generalized geography** — `reduces_from` → **PSPACE-completeness of QBF**. Generalized geography is shown PSPACE-hard by reducing QBF.
- **Ruzzo’s characterization of NC** — `same_statement_as` → **Ruzzo’s characterization of NC**. Lecture 11 states Ruzzo’s theorem; Lecture 12 proves it.
- **IP = PSPACE** — `summarizes` → **Interactive proof system**. The IP definition is the basis for the equality IP=PSPACE.
- **PCP theorem** — `strengthens` → **Weak PCP construction**. The full PCP theorem improves randomness from O(n³) to O(log n) while retaining O(1) queries.
- **Valiant–Vazirani theorem** — `feeds_into` → **Toda’s theorem**. Valiant–Vazirani isolation is one of the randomized/counting ingredients around Toda’s theorem.
- **Strong constant-depth parity lower bound** — `implies` → **Oracle separation of PH and PSPACE**. The strong parity circuit lower bound yields an oracle with PHᴬ≠PSPACEᴬ via Theorem 30.1.
- **Low simple set** — `supports` → **Friedberg–Muchnik theorem**. A low simple set supplies the intermediate r.e. degree used in the Friedberg–Muchnik theorem.
- **Padding implication** — `uses_technique` → **Deterministic space hierarchy**. Both use padding/diagonalization ideas to transfer separations across resource scales.

# Source: Theory of Computation

**Author:** Dexter C. Kozen
**Year:** 2006
**Source file:** `1-84628-477-5.pdf`

## Lecture 1: The Complexity of Computations

*PDF pages 14–21*

### Concept — Deterministic one-tape Turing machine

**Location:** PDF p. 16; printed p. 5.
**Importance:** foundational.
**Tags:** turing-machines, models-of-computation.

A finite-control machine with a semi-infinite read/write tape, a head, input and tape alphabets, and a transition function δ:Q×Γ→Q×Γ×{L,R}; it accepts or rejects by entering distinguished halting states.

### Theorem 1.1 — One-tape palindrome lower bound

**Location:** PDF p. 18; printed p. 7.
**Importance:** supporting.
**Tags:** turing-machines, lower-bounds, crossing-sequences.

For Σ = {0,1,#}, the palindrome language PAL = {z ∈ Σ* : z = rev(z)} requires Ω(n²) time on every one-tape Turing machine.

### Concept — Nondeterministic Turing machine

**Location:** PDF p. 18; printed p. 7.
**Importance:** foundational.
**Tags:** turing-machines, nondeterminism.

A Turing machine whose transition rule is a finite relation rather than a function. Its computation is a tree, and it accepts when some branch reaches an accepting configuration.

### Lemma 1.2 — Crossing-sequence disjointness

**Location:** PDF p. 19; printed p. 8.
**Importance:** supporting.
**Tags:** turing-machines, lower-bounds, crossing-sequences.

For distinct x,y ∈ PALₙ, the sets C(x) and C(y) of crossing sequences in the middle half of the input are disjoint.

### Theorem 1.3 — Sub-log-log space collapse

**Location:** PDF p. 19; printed p. 8.
**Importance:** supporting.
**Tags:** turing-machines, lower-bounds, crossing-sequences.

Every Turing machine using o(log log n) work space accepts a regular language. This is tight up to constants: a specific nonregular language is accepted in O(log log n) space.

### Concept — Crossing sequence

**Location:** PDF p. 19; printed p. 8.
**Importance:** foundational.
**Tags:** lower-bounds, crossing-sequences.

The sequence of finite-control states seen as a one-tape TM crosses a fixed boundary between adjacent tape cells. Crossing sequences transfer all information communicated across that boundary.

### Lemma 1.4 — Constant accepted-space bound

**Location:** PDF p. 20; printed p. 9.
**Importance:** supporting.
**Tags:** turing-machines, lower-bounds, crossing-sequences.

If a machine uses at most a fixed finite number of work-tape cells on every accepted input, then its accepted language is regular.

## Lecture 2: Time and Space Complexity Classes and Savitch’s Theorem

*PDF pages 22–27*

### Definition 2.1 — Time- and space-bounded machines

**Location:** PDF p. 22; printed p. 11.
**Importance:** foundational.
**Tags:** time-complexity, space-complexity.

A nondeterministic TM is T(n)-time-bounded when, except on finitely many inputs, every computation path halts within T(|x|) steps. It is S(n)-space-bounded when, except on finitely many inputs, every path uses at most S(|x|) work-tape cells.

### Definition 2.2 — Basic time and space classes

**Location:** PDF p. 23; printed p. 12.
**Importance:** foundational.
**Tags:** time-complexity, space-complexity.

DTIME(T), NTIME(T), DSPACE(S), and NSPACE(S) are the languages accepted within the indicated deterministic or nondeterministic time or space bound. For a class A, co-A is the class of complements of languages in A.

### Theorem 2.3 — Linear speedup

**Location:** PDF p. 23; printed p. 12.
**Importance:** supporting.
**Tags:** time-complexity, space-complexity.

For T(n) ≥ n+1, S(n) = Ω(log n), and every constant c ≥ 1: DTIME(cT) ⊆ DTIME(T), NTIME(cT) ⊆ NTIME(T), DSPACE(cS) ⊆ DSPACE(S), and NSPACE(cS) ⊆ NSPACE(S).

### Definition 2.4 — Named complexity classes

**Location:** PDF p. 23; printed p. 12.
**Importance:** foundational.
**Tags:** time-complexity, space-complexity.

LOGSPACE = DSPACE(log n), NLOGSPACE = NSPACE(log n), P = ⋃ₖ DTIME(nᵏ), NP = ⋃ₖ NTIME(nᵏ), PSPACE = ⋃ₖ DSPACE(nᵏ), NPSPACE = ⋃ₖ NSPACE(nᵏ), and analogously EXPTIME, NEXPTIME, EXPSPACE, and NEXPSPACE use bounds 2^{nᵏ}.

### Theorem 2.5 — Basic time-space inclusions

**Location:** PDF p. 24; printed p. 13.
**Importance:** supporting.
**Tags:** time-complexity, space-complexity.

For S(n) ≥ log n: DTIME(T) ⊆ DSPACE(T), NTIME(T) ⊆ NSPACE(T), DSPACE(S) ⊆ DTIME(2^{O(S)}), and NSPACE(S) ⊆ NTIME(2^{O(S)}).

### Theorem 2.6 — Deterministic simulation bounds

**Location:** PDF p. 25; printed p. 14.
**Importance:** supporting.
**Tags:** time-complexity, space-complexity.

For S(n) ≥ log n: NTIME(T) ⊆ DSPACE(T), and NSPACE(S) ⊆ DTIME(2^{O(S)}).

### Theorem 2.7 — Savitch’s theorem

**Location:** PDF p. 26; printed p. 15.
**Importance:** core.
**Tags:** time-complexity, space-complexity.

For S(n) ≥ log n, NSPACE(S(n)) ⊆ DSPACE(S(n)²). In particular, PSPACE = NPSPACE.

**Why it matters:** Converts nondeterministic space into only a quadratic deterministic-space overhead.

## Lecture 3: Separation Results

*PDF pages 28–32*

### Theorem 3.1 — Deterministic space hierarchy

**Location:** PDF p. 28; printed p. 17.
**Importance:** supporting.
**Tags:** hierarchy-theorems, diagonalization, padding.

If S is space-constructible, then DSPACE(S) contains a language outside DSPACE(S′) for every S′ = o(S).

### Theorem 3.2 — Deterministic time hierarchy

**Location:** PDF p. 30; printed p. 19.
**Importance:** supporting.
**Tags:** hierarchy-theorems, diagonalization, padding.

If T is time-constructible and T(n) ≥ n, then DTIME(T) contains a language outside every DTIME(T′) satisfying T′(n) log T′(n) = o(T(n)).

## Lecture 4: The Immerman–Szelepcsényi Theorem

*PDF pages 33–35*

### Theorem 4.1 — Immerman–Szelepcsényi theorem

**Location:** PDF p. 33; printed p. 22.
**Importance:** core.
**Tags:** space-complexity, complement.

For every S(n) ≥ log n, NSPACE(S(n)) is closed under complement: NSPACE(S(n)) = co-NSPACE(S(n)).

**Why it matters:** Shows nondeterministic space is closed under complement, including NL = coNL.

## Lecture 5: Logspace Computability

*PDF pages 36–40*

### Concept — Logspace transducer

**Location:** PDF p. 37; printed p. 26.
**Importance:** foundational.
**Tags:** logspace, transducers.

A total deterministic logspace machine with read-only input, O(log n) read/write work space, and a write-only output tape. Its output defines a logspace-computable function.

### Lemma 5.1 — Transitivity of logspace reductions

**Location:** PDF p. 38; printed p. 27.
**Importance:** supporting.
**Tags:** logspace, reductions, completeness.

Logspace many-one reducibility is transitive: if A ≤ₘˡᵒᵍ B and B ≤ₘˡᵒᵍ C, then A ≤ₘˡᵒᵍ C.

### Lemma 5.2 — LOGSPACE as reduction to a fixed language

**Location:** PDF p. 38; printed p. 27.
**Importance:** supporting.
**Tags:** logspace, reductions, completeness.

A language A is in LOGSPACE exactly when A ≤ₘˡᵒᵍ {0,1}.

### Lemma 5.3 — Closure under logspace reduction

**Location:** PDF p. 38; printed p. 27.
**Importance:** supporting.
**Tags:** logspace, reductions, completeness.

If A ≤ₘˡᵒᵍ B and B ∈ LOGSPACE, then A ∈ LOGSPACE.

### Concept — Logspace many-one reduction

**Location:** PDF p. 38; printed p. 27.
**Importance:** foundational.
**Tags:** reductions, logspace, completeness.

A≤ₘˡᵒᵍB when a logspace-computable function σ satisfies x∈A iff σ(x)∈B. Hardness and completeness are defined using this reduction.

### Lemma 5.4 — Logspace reductions are polynomial-time reductions

**Location:** PDF p. 39; printed p. 28.
**Importance:** supporting.
**Tags:** logspace, reductions, completeness.

If A ≤ₘˡᵒᵍ B, then A ≤ₘᵖ B.

### Definition 5.5 — MAZE / directed reachability

**Location:** PDF p. 39; printed p. 28.
**Importance:** foundational.
**Tags:** logspace, reductions, completeness.

MAZE asks whether a directed graph G with distinguished vertices s and t contains a directed path from s to t.

### Theorem 5.6 — NLOGSPACE-completeness of reachability

**Location:** PDF p. 39; printed p. 28.
**Importance:** core.
**Tags:** logspace, reductions, completeness.

MAZE is complete for NLOGSPACE under logspace many-one reductions.

### Corollary 5.7 — Reachability criterion for L = NL

**Location:** PDF p. 40; printed p. 29.
**Importance:** supporting.
**Tags:** logspace, reductions, completeness.

MAZE is in LOGSPACE if and only if LOGSPACE = NLOGSPACE.

## Lecture 6: The Circuit Value Problem

*PDF pages 41–45*

### Theorem 6.1 — P-completeness of circuit value

**Location:** PDF p. 42; printed p. 31.
**Importance:** core.
**Tags:** circuits, sat, completeness.

The Boolean circuit value problem is complete for P under logspace many-one reductions.

### Concept — Boolean circuit and circuit value problem

**Location:** PDF p. 42; printed p. 31.
**Importance:** foundational.
**Tags:** circuits, p-completeness.

A Boolean circuit is an acyclic network of Boolean gates. CVP supplies both a circuit and its input assignment and asks for the output value.

### Theorem 6.2 — Cook–Levin theorem, logspace form

**Location:** PDF p. 45; printed p. 34.
**Importance:** core.
**Tags:** circuits, sat, completeness.

Boolean satisfiability is complete for NP under logspace many-one reductions.

**Why it matters:** Provides the canonical complete problem for NP.

## Supplementary Lecture A: The Knaster–Tarski Theorem

*PDF pages 46–54*

### Concept — Complete lattice and monotone operator

**Location:** PDF p. 49; printed p. 38.
**Importance:** foundational.
**Tags:** lattices, fixed-points.

A complete lattice has a supremum for every subset. An operator τ is monotone when x≤y implies τ(x)≤τ(y); chain-continuity preserves suprema of chains, and finitary set operators depend only on finite subsets.

### Concept — Prefixpoint, fixpoint, and closure operator

**Location:** PDF p. 50; printed p. 39.
**Importance:** foundational.
**Tags:** lattices, fixed-points.

A prefixpoint satisfies τ(x)≤x; a fixpoint satisfies τ(x)=x. A closure operator is monotone, extensive, and idempotent.

### Lemma A.3 — Infima of prefixpoints

**Location:** PDF p. 51; printed p. 40.
**Importance:** supporting.
**Tags:** lattices, fixed-points.

The infimum of any family of prefixpoints of a monotone operator is again a prefixpoint.

### Lemma A.4 — Least fixpoint existence

**Location:** PDF p. 51; printed p. 40.
**Importance:** supporting.
**Tags:** lattices, fixed-points.

Every monotone operator on a complete lattice has a least fixpoint.

### Lemma A.5 — Prefixpoint closure operator

**Location:** PDF p. 52; printed p. 41.
**Importance:** supporting.
**Tags:** lattices, fixed-points.

For a monotone operator τ, the map τ†(x), defined as the least prefixpoint of τ above x, is a closure operator.

### Lemma A.8 — Monotonicity of transfinite approximants

**Location:** PDF p. 53; printed p. 42.
**Importance:** supporting.
**Tags:** lattices, fixed-points.

For ordinals α ≤ β, the transfinite iterates satisfy τ^α(x) ≤ τ^β(x).

### Theorem A.9 — Knaster–Tarski theorem

**Location:** PDF p. 54; printed p. 43.
**Importance:** core.
**Tags:** lattices, fixed-points.

For every monotone operator τ on a complete lattice, the least prefixpoint above x equals the supremum of the transfinite iteration from below: τ†(x) = τ*(x).

**Why it matters:** Supplies the fixed-point machinery used for alternating computation and games.

## Lecture 7: Alternation

*PDF pages 55–61*

### Definition 7.1 — Alternating Turing machine

**Location:** PDF p. 56; printed p. 45.
**Importance:** foundational.
**Tags:** alternation.

An alternating Turing machine is a nondeterministic TM whose states are typed as AND, OR, or NOT states; NOT configurations have exactly one successor. An accepting leaf is an AND state with no successors, and a rejecting leaf is an OR state with no successors.

### Definition 7.2 — Acceptance for alternating machines

**Location:** PDF p. 58; printed p. 47.
**Importance:** foundational.
**Tags:** alternation.

Let ℓ* be the least fixed-point labeling of configurations by {0,1,⊥}. The machine accepts x when ℓ*(start(x)) = 1 and rejects x when ℓ*(start(x)) = 0; value ⊥ means neither acceptance nor rejection.

### Lemma 7.3 — Eliminating negation states

**Location:** PDF p. 58; printed p. 47.
**Importance:** supporting.
**Tags:** alternation.

Every alternating TM with NOT states can be simulated by an alternating TM using only AND and OR states, with no asymptotic increase in time or space.

### Theorem 7.4 — Alternation simulation theorem

**Location:** PDF p. 59; printed p. 48.
**Importance:** core.
**Tags:** alternation.

For T(n) ≥ n and S(n) ≥ log n: (i) ATIME(T) ⊆ DSPACE(T); (ii) DSPACE(S) ⊆ ATIME(S²); (iii) ASPACE(S) ⊆ DTIME(2^{O(S)}); and (iv) DTIME(T) ⊆ ASPACE(log T).

**Why it matters:** Identifies alternation as the bridge between time and space.

### Concept — Alternating time and space classes

**Location:** PDF p. 59; printed p. 48.
**Importance:** foundational.
**Tags:** alternation, complexity-classes.

ATIME(T) and ASPACE(S) are the languages accepted by alternating TMs whose every path respects the stated time or space bound.

### Corollary 7.5 — Alternation characterizations

**Location:** PDF p. 60; printed p. 49.
**Importance:** core.
**Tags:** alternation.

For T(n) ≥ n and S(n) ≥ log n, ATIME(T^{O(1)}) = DSPACE(T^{O(1)}) and ASPACE(S) = DTIME(2^{O(S)}).

## Lecture 8: Problems Complete for PSPACE

*PDF pages 62–67*

### Definition 8.1 — Quantified Boolean formula problem

**Location:** PDF p. 62; printed p. 51.
**Importance:** foundational.
**Tags:** pspace, complete-problems, games.

QBF asks whether a fully quantified Boolean expression Q₁x₁…Qₙxₙ B(x₁,…,xₙ), with each Qᵢ ∈ {∃,∀}, is true over {0,1}.

### Theorem 8.2 — PSPACE-completeness of QBF

**Location:** PDF p. 62; printed p. 51.
**Importance:** core.
**Tags:** pspace, complete-problems, games.

QBF is complete for PSPACE under logspace many-one reductions.

**Why it matters:** Gives the canonical PSPACE-complete problem.

### Definition 8.3 — Forced-win predicate

**Location:** PDF p. 64; printed p. 53.
**Importance:** foundational.
**Tags:** pspace, complete-problems, games.

For a two-player perfect-information game, checkmate(y) means y has no legal successor. The predicate win is the least fixed point satisfying win(x) iff there exists a move x→y such that every legal reply y→z leads to win(z) (with immediate checkmate covered vacuously).

### Theorem 8.4 — PSPACE-completeness of generalized geography

**Location:** PDF p. 65; printed p. 54.
**Importance:** core.
**Tags:** pspace, complete-problems, games.

Generalized geography is complete for PSPACE under logspace many-one reductions.

## Lecture 9: The Polynomial-Time Hierarchy

*PDF pages 68–72*

### Definition 9.1 — Bounded-alternation machines

**Location:** PDF p. 68; printed p. 57.
**Importance:** foundational.
**Tags:** polynomial-hierarchy, oracles.

A Σₖ-machine is an alternating TM whose paths have at most k maximal blocks of like-typed configurations and begin with an OR block. A Πₖ-machine is defined dually and begins with an AND block; Σ₁ is nondeterminism and Σ₀ = Π₀ is determinism.

### Definition 9.2 — Levels of the polynomial hierarchy

**Location:** PDF p. 69; printed p. 58.
**Importance:** foundational.
**Tags:** polynomial-hierarchy, oracles.

Σₖᵖ is the class accepted in polynomial time by Σₖ-machines, and Πₖᵖ is the class accepted in polynomial time by Πₖ-machines. Thus Σ₁ᵖ = NP, Π₁ᵖ = coNP, and Σ₀ᵖ = Π₀ᵖ = P.

### Lemma 9.3 — Basic polynomial-hierarchy relations

**Location:** PDF p. 69; printed p. 58.
**Importance:** supporting.
**Tags:** polynomial-hierarchy, oracles.

For every k: Πₖᵖ = co-Σₖᵖ; Σₖᵖ ∪ Πₖᵖ ⊆ Σₖ₊₁ᵖ ∩ Πₖ₊₁ᵖ; and ⋃ₖΣₖᵖ = ⋃ₖΠₖᵖ ⊆ PSPACE.

### Theorem 9.4 — Generic Σₖᵖ-complete problem

**Location:** PDF p. 70; printed p. 59.
**Importance:** supporting.
**Tags:** polynomial-hierarchy, oracles.

The bounded alternating acceptance language Hₖ is complete for Σₖᵖ under logspace many-one reductions.

### Corollary 9.5 — Generic Πₖᵖ-complete problem

**Location:** PDF p. 70; printed p. 59.
**Importance:** supporting.
**Tags:** polynomial-hierarchy, oracles.

The complement of Hₖ is complete for Πₖᵖ under logspace many-one reductions.

### Concept — Oracle Turing machine

**Location:** PDF p. 70; printed p. 59.
**Importance:** foundational.
**Tags:** oracles, relativization.

An oracle machine may ask membership questions about a fixed set B and receive each answer in one step, enabling relativized classes such as Pᴮ and NPᴮ.

### Definition 9.6 — Relativized polynomial classes

**Location:** PDF p. 71; printed p. 60.
**Importance:** foundational.
**Tags:** polynomial-hierarchy, oracles.

For an oracle B, Pᴮ and NPᴮ are the languages accepted by polynomial-time deterministic and nondeterministic oracle machines using B. For a class C, Pᶜ = ⋃_{B∈C}Pᴮ and NPᶜ = ⋃_{B∈C}NPᴮ.

### Definition 9.7 — Polynomial-time Turing reduction

**Location:** PDF p. 72; printed p. 61.
**Importance:** foundational.
**Tags:** polynomial-hierarchy, oracles.

A ≤ᵀᵖ B means A ∈ Pᴮ; this is polynomial-time Turing (Cook) reducibility.

### Theorem 9.8 — Oracle definition of PH

**Location:** PDF p. 72; printed p. 61.
**Importance:** core.
**Tags:** polynomial-hierarchy, oracles.

Define NP₁ = NP and NPₖ₊₁ = NP^{NPₖ}. Then NPₖ = Σₖᵖ for every k ≥ 1.

## Lecture 10: More on the Polynomial-Time Hierarchy

*PDF pages 73–76*

### Theorem 10.1 — Equivalence of PH definitions

**Location:** PDF p. 73; printed p. 62.
**Importance:** core.
**Tags:** polynomial-hierarchy, quantifiers.

For every k ≥ 1, the iterated-oracle class NPₖ equals the alternating-machine class Σₖᵖ.

### Theorem 10.2 — Quantifier characterization of Σₖᵖ

**Location:** PDF p. 76; printed p. 65.
**Importance:** core.
**Tags:** polynomial-hierarchy, quantifiers.

A language A is in Σₖᵖ iff there are a polynomial-time predicate R and constant c such that x ∈ A exactly when ∃y₁∀y₂∃y₃…Qₖyₖ R(x,y₁,…,yₖ), where every |yᵢ| ≤ |x|ᶜ and Qₖ is ∃ for odd k and ∀ for even k.

## Lecture 11: Parallel Complexity

*PDF pages 77–80*

### Definition 11.1 — Uniform-circuit definition of NC

**Location:** PDF p. 78; printed p. 67.
**Importance:** foundational.
**Tags:** parallel-complexity, nc, circuits.

A logspace-uniform circuit family has n-input circuits Cₙ of polynomial size and polylogarithmic depth, constructible from 0ⁿ by a logspace transducer. NC is the class of languages decided by such Boolean circuit families.

### Definition 11.2 — STA classes

**Location:** PDF p. 80; printed p. 69.
**Importance:** foundational.
**Tags:** parallel-complexity, nc, circuits.

STA(S,T,A) consists of languages accepted by alternating TMs simultaneously bounded by space S(n), time T(n), and A(n) alternations. An asterisk means no bound; Σ or Π may specify the initial branch type.

### Theorem 11.3 — Ruzzo’s characterization of NC

**Location:** PDF p. 80; printed p. 69.
**Importance:** core.
**Tags:** parallel-complexity, nc, circuits.

NC = STA(log n, *, (log n)^{O(1)}).

## Lecture 12: Relation of NC to Time-Space Classes

*PDF pages 81–84*

### Theorem 12.1 — Ruzzo’s characterization of NC

**Location:** PDF p. 81; printed p. 70.
**Importance:** core.
**Tags:** parallel-complexity, nc, alternation.

NC = STA(log n, *, (log n)^{O(1)}).

## Lecture 13: Probabilistic Complexity

*PDF pages 85–92*

### Concept — Probabilistic Turing machine

**Location:** PDF p. 88; printed p. 77.
**Importance:** foundational.
**Tags:** randomized-computation.

A deterministic TM with access to a read-only random bit tape; acceptance probability is measured over uniformly random bit strings.

### Definition 13.1 — RP and BPP

**Location:** PDF p. 89; printed p. 78.
**Importance:** foundational.
**Tags:** randomized-computation, polynomial-identity-testing.

A language is in RP if a polynomial-time randomized TM accepts yes-instances with probability at least 3/4 and never accepts no-instances. It is in BPP if the same machine errs with probability at most 1/4 on every input.

### Theorem 13.2 — Schwartz–Zippel lemma

**Location:** PDF p. 90; printed p. 79.
**Importance:** core.
**Tags:** randomized-computation, polynomial-identity-testing.

If p is a nonzero n-variate polynomial of total degree d over a field F and S ⊆ F, then p has at most d|S|^{n-1} zeros in Sⁿ.

### Corollary 13.3 — Random evaluation bound

**Location:** PDF p. 90; printed p. 79.
**Importance:** supporting.
**Tags:** randomized-computation, polynomial-identity-testing.

Under the hypotheses of Schwartz–Zippel, a uniformly random s ∈ Sⁿ satisfies p(s)=0 with probability at most d/|S|.

## Lecture 14: BPP ⊆ Σ₂ᵖ ∩ Π₂ᵖ

*PDF pages 93–96*

### Lemma 14.1 — Amplification lemma

**Location:** PDF p. 93; printed p. 82.
**Importance:** core.
**Tags:** bpp, polynomial-hierarchy.

For every polynomial nᵈ, an RP algorithm can be amplified so that yes-instances are accepted with probability at least 1−2^{-nᵈ} while no-instances are never accepted. A BPP algorithm can be amplified so that its error is at most 2^{-nᵈ}.

### Core result — BPP lies low in PH

**Location:** PDF p. 93; printed p. 82.
**Importance:** core.
**Tags:** bpp, polynomial-hierarchy, derandomization.

BPP ⊆ Σ₂ᵖ ∩ Π₂ᵖ. The proof amplifies the randomized algorithm and uses a small family of XOR shifts to cover the random-bit space.

### Claim 14.2 — XOR-shift covering claim

**Location:** PDF p. 95; printed p. 84.
**Importance:** supporting.
**Tags:** bpp, polynomial-hierarchy.

In the amplified BPP setup, let m be the number of random bits and Aₓ = {y : M(x,y) accepts}. Then x ∈ A iff there exist m shifts z₁,…,zₘ ∈ {0,1}ᵐ such that ⋃ⱼ(Aₓ ⊕ zⱼ) = {0,1}ᵐ.

## Supplementary Lecture B: Chinese Remaindering

*PDF pages 97–100*

### Theorem B.1 — Chinese remainder theorem

**Location:** PDF p. 97; printed p. 86.
**Importance:** supporting.
**Tags:** number-theory, chinese-remainder.

For pairwise coprime positive integers n₁,…,nₖ and n = ∏ᵢnᵢ, the map x mod n ↦ (x mod n₁,…,x mod nₖ) is a ring isomorphism Zₙ ≅ Z_{n₁}×…×Z_{nₖ}.

### Theorem B.2 — Chinese remainder theorem for ideals

**Location:** PDF p. 99; printed p. 88.
**Importance:** supporting.
**Tags:** number-theory, chinese-remainder.

If I₁,…,Iₖ are pairwise comaximal ideals of a commutative ring R and I = ⋂ᵢIᵢ, then R/I ≅ R/I₁×…×R/Iₖ via [x]_I ↦ ([x]_{I₁},…,[x]_{Iₖ}).

## Supplementary Lecture C: Complexity of Primality Testing

*PDF pages 101–105*

### Lemma C.1 — Fermat’s theorem / primitive root criterion

**Location:** PDF p. 102; printed p. 91.
**Importance:** supporting.
**Tags:** primality, number-theory.

An integer p ≥ 2 is prime iff some element of {1,…,p−1} has multiplicative order p−1 modulo p.

### Lemma C.2 — Euler totient divisor identity

**Location:** PDF p. 103; printed p. 92.
**Importance:** supporting.
**Tags:** primality, number-theory.

For every positive integer n, ∑_{m|n} φ(m) = n.

### Lemma C.3 — Degree of the order polynomial

**Location:** PDF p. 103; printed p. 92.
**Importance:** supporting.
**Tags:** primality, number-theory.

For k dividing q−1, the polynomial Φₖ whose roots are the elements of GF(q)* of order k has degree φ(k).

### Theorem C.4 — Pratt’s primality theorem

**Location:** PDF p. 104; printed p. 93.
**Importance:** supporting.
**Tags:** primality, number-theory.

The language PRIMES belongs to NP ∩ coNP.

## Lecture 15: Interactive Proofs

*PDF pages 110–113*

### Definition 15.1 — Interactive proof system

**Location:** PDF p. 111; printed p. 100.
**Importance:** foundational.
**Tags:** interactive-proofs.

A protocol (P,V) is an interactive proof for A when V is probabilistic polynomial time, yes-instances are accepted with probability at least 3/4 with the honest prover, and no-instances are accepted with probability at most 1/4 against every prover strategy. IP is the class of languages with such protocols.

## Lecture 16: PSPACE ⊆ IP

*PDF pages 114–119*

### Core result — IP = PSPACE

**Location:** PDF p. 114; printed p. 103.
**Importance:** core.
**Tags:** interactive-proofs, pspace.

Every PSPACE language has an interactive proof, and every language with an interactive proof is in PSPACE; therefore IP = PSPACE.

### Definition 16.1 — Simple quantified Boolean formula

**Location:** PDF p. 115; printed p. 104.
**Importance:** foundational.
**Tags:** interactive-proofs, pspace, arithmetization.

A QBF is simple when negations apply only to variables and, between any free occurrence of a variable in a quantified subformula and its binding quantifier, there is at most one intervening universal quantifier.

### Lemma 16.2 — Simplifying QBFs

**Location:** PDF p. 115; printed p. 104.
**Importance:** supporting.
**Tags:** interactive-proofs, pspace, arithmetization.

Every quantified Boolean formula can be transformed in logspace into an equivalent simple formula with at most quadratic growth in size.

### Lemma 16.3 — Low-degree arithmetization

**Location:** PDF p. 118; printed p. 107.
**Importance:** supporting.
**Tags:** interactive-proofs, pspace, arithmetization.

If ∑_{x∈{0,1}}D(x) or ∏_{x∈{0,1}}D(x) arises by arithmetizing a simple Boolean formula, then D(x) is equivalent modulo p to a polynomial over Zₚ whose degree is linear in the expression size.

### Lemma 16.4 — Univariate root bound

**Location:** PDF p. 118; printed p. 107.
**Importance:** supporting.
**Tags:** interactive-proofs, pspace, arithmetization.

A nonzero polynomial d(x) ∈ Zₚ[x] of degree at most n vanishes at a uniformly random element of Zₚ with probability at most n/p.

## Lecture 18: Probabilistically Checkable Proofs

*PDF pages 124–129*

### Concept — PCP(r,q)

**Location:** PDF p. 124; printed p. 113.
**Importance:** foundational.
**Tags:** pcp, proof-systems.

PCP(r(n),q(n)) consists of languages with polynomial-time proof verifiers using O(r(n)) random bits and O(q(n)) oracle queries, with perfect completeness and constant soundness.

### Theorem 18.1 — PCP theorem

**Location:** PDF p. 125; printed p. 114.
**Importance:** core.
**Tags:** pcp, approximation.

NP = PCP(log n, 1): every NP language has a verifier using O(log n) random bits and O(1) proof queries, with perfect completeness and constant soundness.

**Why it matters:** Foundation of modern hardness of approximation.

### Lemma 18.2 — 7/8 approximation for MAX-3SAT

**Location:** PDF p. 126; printed p. 115.
**Importance:** supporting.
**Tags:** pcp, approximation.

There is a polynomial-time algorithm that, for a 3CNF formula with m clauses and three distinct variables per clause, finds an assignment satisfying at least 7m/8 clauses.

### Theorem 18.3 — Hardness of approximating MAX-CLIQUE

**Location:** PDF p. 127; printed p. 116.
**Importance:** core.
**Tags:** pcp, approximation.

A polynomial-time constant-factor approximation algorithm for MAX-CLIQUE exists for some fixed α>0 iff P = NP.

### Theorem 18.4 — Hardness of a PTAS for MAX-3SAT

**Location:** PDF p. 127; printed p. 116.
**Importance:** core.
**Tags:** pcp, approximation.

MAX-3SAT has a polynomial-time approximation scheme iff P = NP.

## Lecture 19: NP ⊆ PCP(n³, 1)

*PDF pages 130–134*

### Core result — Weak PCP construction

**Location:** PDF p. 130; printed p. 119.
**Importance:** core.
**Tags:** pcp, linearity-testing.

NP ⊆ PCP(n³,1), proved using arithmetization, linearity testing, tensor-consistency tests, and random self-correction.

### Lemma 19.1 — Linearity testing lemma

**Location:** PDF p. 133; printed p. 122.
**Importance:** supporting.
**Tags:** pcp, linearity-testing.

Let F=Zₚ and V be finite-dimensional. If ε<1/6 and Pr_{u,v}[f(u+v)=f(u)+f(v)]>1−ε, then there is a linear g:V→F agreeing with f on at least a 1−3ε fraction of V.

## Supplementary Lecture E: A Crash Course in Logic

*PDF pages 139–145*

### Concept — First-order structure, formula, sentence, and theory

**Location:** PDF p. 139; printed p. 128.
**Importance:** foundational.
**Tags:** logic, model-theory.

A structure interprets a signature over a domain; terms denote elements, formulas receive truth values under valuations, sentences have no free variables, and Th(A) is the set of sentences true in A.

## Lecture 21: Complexity of Decidable Theories

*PDF pages 146–150*

### Theorem 21.1 — Back-and-forth theorem for dense orders

**Location:** PDF p. 147; printed p. 136.
**Importance:** supporting.
**Tags:** logic, decision-procedures, pspace.

Any two countable dense linear orders without endpoints are isomorphic. More generally, every finite local isomorphism between such orders extends to a full isomorphism.

### Theorem 21.2 — Complexity of dense linear order

**Location:** PDF p. 150; printed p. 139.
**Importance:** core.
**Tags:** logic, decision-procedures, pspace.

The first-order theory of dense linear orders without endpoints is PSPACE-complete.

## Lecture 22: Complexity of the Theory of Real Addition

*PDF pages 151–156*

### Core result — Exact complexity of real addition

**Location:** PDF p. 151; printed p. 140.
**Importance:** core.
**Tags:** logic, real-addition, alternation.

The first-order theory Th(R,+,≤) is complete for STA(*,2^{O(n)},n).

### Definition 22.1 — Integer affine functions

**Location:** PDF p. 152; printed p. 141.
**Importance:** foundational.
**Tags:** logic, real-addition.

An integer affine function f:Rᵏ→R has the form c₀+∑ᵢcᵢxᵢ with integer coefficients. Its norm is ‖f‖ = max_{0≤i≤k}|cᵢ|; Aₘᵏ denotes those with norm at most m.

### Definition 22.2 — Bounded affine equivalence

**Location:** PDF p. 152; printed p. 141.
**Importance:** foundational.
**Tags:** logic, real-addition.

For a,b∈Rᵏ, define a ≡ₘᵏ b when every integer affine f with ‖f‖≤m has the same sign on a and b; equivalently, a and b satisfy the same bounded-coefficient linear inequalities.

### Lemma 22.3 — One-step extension lemma

**Location:** PDF p. 152; printed p. 141.
**Importance:** technical.
**Tags:** logic, real-addition.

If a ≡_{2m²}ᵏ b, then for every a′∈R there is b′∈R such that (a,a′) ≡ₘ^{k+1} (b,b′).

### Lemma 22.4 — Finite representatives lemma

**Location:** PDF p. 153; printed p. 142.
**Importance:** technical.
**Tags:** logic, real-addition.

If σ is the ≡_{2m²}ᵏ-class of a, then points of the form (a,f(a)/c), with f∈A_{2m²}ᵏ and |c|≤2m², include a representative of every ≡ₘ^{k+1}-class consistent with σ.

### Lemma 22.5 — Logical invariance under bounded affine equivalence

**Location:** PDF p. 154; printed p. 143.
**Importance:** technical.
**Tags:** logic, real-addition.

If a ≡_{r(n,ℓ)}ᵏ b, then a and b agree on every reduced formula with at most n quantifiers and integer constants of magnitude at most ℓ.

### Theorem 22.6 — Upper bound for real addition

**Location:** PDF p. 155; printed p. 144.
**Importance:** core.
**Tags:** logic, real-addition.

The first-order theory Th(R,+,≤) belongs to STA(*,2^{O(n)},n).

## Lecture 23: Lower Bound for the Theory of Real Addition

*PDF pages 157–161*

### Lemma 23.1 — Recursive decomposition of large integer ranges

**Location:** PDF p. 159; printed p. 148.
**Importance:** technical.
**Tags:** logic, lower-bounds, real-addition.

For Iₙ={z∈Z:0≤z<2^{2ⁿ}}, one has Iₙ₊₁ = {z₁z₂+z₃+z₄ : z₁,z₂,z₃,z₄∈Iₙ}.

## Lecture 24: Lower Bound for Integer Addition

*PDF pages 162–164*

### Core result — Exact complexity of Presburger arithmetic

**Location:** PDF p. 162; printed p. 151.
**Importance:** core.
**Tags:** logic, presburger-arithmetic.

The first-order theory Th(Z,+,≤) is complete for STA(*,2^{2^{n^{O(1)}}},n).

## Lecture 25: Automata on Infinite Strings and S1S

*PDF pages 165–171*

### Concept — Büchi automaton

**Location:** PDF p. 166; printed p. 155.
**Importance:** foundational.
**Tags:** omega-automata, buchi.

An automaton on infinite words whose run is accepting when a designated accepting state occurs infinitely often.

### Concept — Muller automaton

**Location:** PDF p. 168; printed p. 157.
**Importance:** foundational.
**Tags:** omega-automata, muller.

An automaton on infinite words with an acceptance family F⊆2^Q; a run is accepting when its set of infinitely recurring states belongs to F.

### Theorem 25.3 — S1S–automata correspondence

**Location:** PDF p. 169; printed p. 158.
**Importance:** core.
**Tags:** omega-automata, s1s.

(i) Every S1S formula φ(x,X) can be translated into a Muller automaton whose accepted track encodings are exactly the tuples satisfying φ. (ii) Every nondeterministic Büchi automaton over {0,1} can be translated into an S1S formula defining the sets whose characteristic strings it accepts.

## Lecture 26: Determinization of ω-Automata

*PDF pages 172–177*

### Concept — Rabin automaton

**Location:** PDF p. 173; printed p. 162.
**Importance:** foundational.
**Tags:** omega-automata, rabin.

A deterministic ω-automaton with pairs (Gᵢ,Rᵢ); a run accepts when some Gᵢ is visited infinitely often while the corresponding Rᵢ is visited only finitely often.

### Lemma 26.1 — König’s lemma

**Location:** PDF p. 176; printed p. 165.
**Importance:** supporting.
**Tags:** omega-automata, determinization.

Every infinite tree of finite branching degree has an infinite path.

## Lecture 27: Safra’s Construction

*PDF pages 178–181*

### Claim 27.1 — Acceptance invariant in Safra’s construction

**Location:** PDF p. 180; printed p. 169.
**Importance:** supporting.
**Tags:** omega-automata, safra.

The nondeterministic Büchi automaton B accepts x iff, in the determinized construction, some color’s bell rings infinitely often while that color’s buzzer sounds only finitely often.

### Theorem 27.2 — Safra determinization theorem

**Location:** PDF p. 181; printed p. 170.
**Importance:** core.
**Tags:** omega-automata, safra.

Every n-state nondeterministic Büchi automaton can be simulated by a deterministic Rabin automaton with at most 2^{O(n log n)} states and n Rabin pairs.

## Lecture 28: Relativized Complexity

*PDF pages 182–185*

### Theorem 28.1 — Oracle collapsing P and NP

**Location:** PDF p. 183; printed p. 172.
**Importance:** core.
**Tags:** oracles, relativization.

There exists a recursive oracle A such that Pᴬ = NPᴬ.

### Theorem 28.2 — Oracle separating P and NP

**Location:** PDF p. 183; printed p. 172.
**Importance:** core.
**Tags:** oracles, relativization.

There exists a recursive oracle B such that Pᴮ ≠ NPᴮ.

## Lecture 29: Nonexistence of Sparse Complete Sets

*PDF pages 186–190*

### Concept — Sparse language

**Location:** PDF p. 186; printed p. 175.
**Importance:** foundational.
**Tags:** sparse-sets, np-completeness.

A language S is sparse when the number of strings of length at most n in S is bounded by a polynomial in n.

### Theorem 29.1 — Fortune’s sparse-hard-set theorem

**Location:** PDF p. 187; printed p. 176.
**Importance:** core.
**Tags:** sparse-sets, np-completeness.

If a sparse language is polynomial-time many-one hard for coNP, then P = NP.

### Theorem 29.2 — Mahaney’s theorem

**Location:** PDF p. 188; printed p. 177.
**Importance:** core.
**Tags:** sparse-sets, np-completeness.

If a sparse language is polynomial-time many-one complete for NP, then P = NP.

## Supplementary Lecture F: Unique Satisfiability

*PDF pages 191–195*

### Concept — Unique satisfiability

**Location:** PDF p. 191; printed p. 180.
**Importance:** foundational.
**Tags:** unique-sat, randomized-reductions.

USAT is the promise-style satisfiability problem restricted to formulas having at most one satisfying assignment; it is used as the target of the Valiant–Vazirani randomized reduction.

### Lemma F.1 — Random subspace isolation lemma

**Location:** PDF p. 192; printed p. 181.
**Importance:** technical.
**Tags:** unique-sat, randomized-reductions.

Let S be a nonempty subset of GF(2)ⁿ, and choose a random nested tower E₀⊂…⊂Eₙ with dim(Eᵢ)=i. Then Pr[there exists i with |S∩Eᵢ|=1] ≥ 3/4.

### Theorem F.2 — Valiant–Vazirani theorem

**Location:** PDF p. 194; printed p. 183.
**Importance:** core.
**Tags:** unique-sat, randomized-reductions.

NP ⊆ RP^USAT: every NP language has a randomized polynomial-time reduction to unique satisfiability.

## Supplementary Lecture G: Toda’s Theorem

*PDF pages 196–202*

### Concept — The class #P

**Location:** PDF p. 196; printed p. 185.
**Importance:** foundational.
**Tags:** counting-complexity, toda.

#P consists of functions counting accepting computation paths of nondeterministic polynomial-time machines. P^#P denotes polynomial-time computation with access to such counts.

### Theorem G.1 — Toda’s theorem

**Location:** PDF p. 198; printed p. 187.
**Importance:** core.
**Tags:** counting-complexity, toda.

PH ⊆ P^#P.

**Why it matters:** Shows the entire polynomial hierarchy is controlled by a counting oracle.

### Lemma G.2 — Operator identities used in Toda’s theorem

**Location:** PDF p. 198; printed p. 187.
**Importance:** technical.
**Tags:** counting-complexity, toda.

For every class C downward closed under polynomial-time Turing reductions: (i) Σᵖ·C ⊆ R·Σˡᵒᵍ·⊕·C; (ii) Πˡᵒᵍ·⊕·C ⊆ ⊕·C; (iii) ⊕·BP·C ⊆ BP·⊕·C; (iv) BP·BP·C ⊆ BP·C; (v) ⊕·⊕·C ⊆ ⊕·C; and (vi) BP·C and ⊕·C are downward closed under ≤ᵀᵖ.

## Lecture 30: Circuit Lower Bounds and Relativized PSPACE = PH

*PDF pages 203–208*

### Concept — AC⁰

**Location:** PDF p. 204; printed p. 193.
**Importance:** foundational.
**Tags:** circuit-complexity, lower-bounds.

AC⁰ is the class of constant-depth, polynomial-size Boolean circuit families with unbounded-fan-in AND and OR gates and negations at inputs.

### Theorem 30.1 — Circuit lower bounds imply oracle separation

**Location:** PDF p. 205; printed p. 194.
**Importance:** core.
**Tags:** circuit-complexity, oracles.

If parity has no depth-d circuit family of size 2^{(log n)^c} for any constants c and d, then some oracle A satisfies PHᴬ ≠ PSPACEᴬ.

## Lecture 31: Lower Bounds for Constant-Depth Circuits

*PDF pages 209–214*

### Lemma 31.1 — Many variables survive a random restriction

**Location:** PDF p. 210; printed p. 199.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

Under the lecture’s random partial valuation, the probability that fewer than √n/2 variables remain unassigned is at most (2/e)^{√n/2}.

### Lemma 31.2 — Few variables survive inside a small set

**Location:** PDF p. 210; printed p. 199.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

For a constant c and a variable set A with c ≤ |A| and |A| = o(n^{1/c}), the probability that a random partial valuation leaves more than c variables of A unassigned is at most n^{1−c/2} for all sufficiently large n.

### Lemma 31.3 — Hitting many disjoint small sets

**Location:** PDF p. 211; printed p. 200.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

Let S contain at least b log n pairwise disjoint variable sets, each of size <a. If E(A) is the event that all variables in A are assigned 0, then for sufficiently large n the probability that no E(A) occurs is at most n^{b log(1−2^{-a})}.

### Lemma 31.4 — Bounded bottom fan-in

**Location:** PDF p. 211; printed p. 200.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

If parity has polynomial-size depth-d circuits, then it has polynomial-size depth-d t-circuits for some constant t.

### Lemma 31.5 — Reduce bottom fan-in

**Location:** PDF p. 211; printed p. 200.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

If parity has polynomial-size depth-d t-circuits with d≥3 and t≥1, then it has polynomial-size depth-d (t−1)-circuits.

### Lemma 31.6 — Remove a circuit level

**Location:** PDF p. 211; printed p. 200.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

If parity has polynomial-size depth-d 1-circuits, then it has polynomial-size circuits of depth d−1.

### Lemma 31.7 — Parity is not shallow CNF/DNF

**Location:** PDF p. 214; printed p. 203.
**Importance:** technical.
**Tags:** circuit-lower-bounds, random-restrictions.

No (n−1)-CNF and no (n−1)-DNF computes parity on n inputs.

### Theorem 31.8 — Furst–Saxe–Sipser lower bound

**Location:** PDF p. 214; printed p. 203.
**Importance:** core.
**Tags:** circuit-lower-bounds, random-restrictions.

Parity is not in AC⁰.

**Why it matters:** A foundational unconditional circuit lower bound.

## Supplementary Lecture H: The Switching Lemma

*PDF pages 215–221*

### Lemma H.1 — Minterm restriction lemma

**Location:** PDF p. 216; printed p. 205.
**Importance:** technical.
**Tags:** switching-lemma, circuit-lower-bounds.

Let M be a minterm of φ∧C. Assign the variables shared by M and clause C in the unique way that keeps M nonzero. Then the restricted formula φ∧C equals the restricted φ, and the restricted M is a minterm of the restricted φ.

### Lemma H.2 — Eliminating a variable set

**Location:** PDF p. 216; printed p. 205.
**Importance:** technical.
**Tags:** switching-lemma, circuit-lower-bounds.

For φ^{-W}=∧_{τ:W→{0,1}}τ(φ): (i) if φ is CNF, φ^{-W} has an equivalent CNF with no more clauses; (ii) any minterm of φ disjoint from W remains a minterm of φ^{-W}; (iii) restrictions fixing no variable of W commute with −W; and (iv) under such restrictions, φ is true iff φ^{-W} is true.

### Lemma H.3 — Håstad switching lemma

**Location:** PDF p. 217; printed p. 206.
**Importance:** core.
**Tags:** switching-lemma, circuit-lower-bounds.

Let φ be a t-CNF. Independently set each variable to 0 or 1 with probability (1−p)/2 each, or leave it unset with probability p. Then Pr[the restricted φ is not equivalent to an s-DNF] ≤ αˢ, where α=4pt/ln 2≈5.77pt.

### Theorem H.4 — Strong constant-depth parity lower bound

**Location:** PDF p. 220; printed p. 209.
**Importance:** core.
**Tags:** switching-lemma, circuit-lower-bounds.

For no constants c,d does parity have a depth-d circuit family of size 2^{(log n)^c}.

**Why it matters:** Strong enough to produce a relativized PH–PSPACE separation.

### Corollary H.5 — Oracle separation of PH and PSPACE

**Location:** PDF p. 221; printed p. 210.
**Importance:** core.
**Tags:** switching-lemma, circuit-lower-bounds.

There exists an oracle A such that PHᴬ ≠ PSPACEᴬ.

## Lecture 32: The Gap Theorem and Other Pathology

*PDF pages 226–230*

### Theorem 32.1 — Gap theorem

**Location:** PDF p. 227; printed p. 216.
**Importance:** core.
**Tags:** complexity-pathology, speedup.

For every total recursive f with f(x)≥x, there is a time bound T such that DTIME(f∘T)=DTIME(T); hence the interval between T and f(T) contains no new deterministic time class.

### Theorem 32.2 — Blum speedup theorem

**Location:** PDF p. 227; printed p. 216.
**Importance:** core.
**Tags:** complexity-pathology, speedup.

For every monotone total recursive f with f(n)≥n², there is a recursive language A such that every TM Mᵢ deciding A has another decider Mⱼ for A with f(Tⱼ(x))<Tᵢ(x) for almost all x.

## Lecture 33: Partial Recursive Functions and Gödel Numberings

*PDF pages 231–236*

### Concept — Gödel numbering

**Location:** PDF p. 231; printed p. 220.
**Importance:** foundational.
**Tags:** computability, godel-numbering.

An effective enumeration φ₀,φ₁,… of the partial recursive functions supporting universal simulation and effective program manipulation.

### Theorem 33.1 — Recursion theorem

**Location:** PDF p. 235; printed p. 224.
**Importance:** core.
**Tags:** computability, recursion-theorem.

For every total recursive index transformation σ, there is an index i with φᵢ=φ_{σ(i)}; such an i is effectively computable from an index for σ.

**Why it matters:** Formalizes self-reference for programs.

## Lecture 34: Applications of the Recursion Theorem

*PDF pages 237–241*

### Theorem 34.1 — No enumerable list of minimal indices

**Location:** PDF p. 239; printed p. 228.
**Importance:** supporting.
**Tags:** computability, godel-numbering.

In any Gödel numbering, there is no infinite recursively enumerable list consisting entirely of minimal indices.

### Lemma 34.2 — Effective padding lemma

**Location:** PDF p. 239; printed p. 228.
**Importance:** technical.
**Tags:** computability, godel-numbering.

In every Gödel numbering there is a total recursive σ such that σ(x)>x and φₓ=φ_{σ(x)} for all x.

### Theorem 34.3 — Rogers isomorphism theorem

**Location:** PDF p. 240; printed p. 229.
**Importance:** core.
**Tags:** computability, godel-numbering.

For any two Gödel numberings (φᵢ) and (ψᵢ) of the partial recursive functions, there is a recursive bijection ρ of N such that φᵢ=ψ_{ρ(i)} for every i.

## Supplementary Lecture J: Abstract Complexity

*PDF pages 242–246*

### Theorem J.1 — Abstract gap theorem

**Location:** PDF p. 243; printed p. 232.
**Importance:** core.
**Tags:** abstract-complexity.

For an abstract complexity measure Φ and every total recursive f(x)≥x, there is a total recursive t with C_t^Φ=C_{f∘t}^Φ. Equivalently, every program bounded by f(t(x)) almost everywhere has an equivalent program bounded by t(x) almost everywhere.

### Theorem J.2 — Abstract speedup theorem

**Location:** PDF p. 243; printed p. 232.
**Importance:** core.
**Tags:** abstract-complexity.

For every abstract complexity measure Φ and total recursive f, there is a total recursive function g such that every index i for g has another index j for g with f(n,Φⱼ(n))<Φᵢ(n) almost everywhere.

### Theorem J.3 — Union theorem

**Location:** PDF p. 245; printed p. 234.
**Importance:** core.
**Tags:** abstract-complexity.

For every recursively enumerable nondecreasing list f₀≤f₁≤… of total recursive bounds, there is a total recursive f such that C_f^Φ=⋃ᵢC_{fᵢ}^Φ.

## Lecture 35: The Arithmetic Hierarchy

*PDF pages 247–252*

### Concept — Arithmetic hierarchy

**Location:** PDF p. 247; printed p. 236.
**Importance:** foundational.
**Tags:** arithmetic-hierarchy, computability.

The classes Σₙ⁰ and Πₙ⁰ classify sets definable by n alternating first-order number quantifiers over a decidable predicate, beginning existentially or universally.

### Theorem 35.1 — Quantifier characterization of the arithmetic hierarchy

**Location:** PDF p. 248; printed p. 237.
**Importance:** core.
**Tags:** arithmetic-hierarchy.

A∈Σₙ⁰ iff A={x:∃y₁∀y₂∃y₃…Qₙyₙ R(x,y₁,…,yₙ)} for some decidable R, with Qₙ=∃ for odd n and ∀ for even n. Dually, A∈Πₙ⁰ iff the prefix begins universally and alternates.

## Lecture 36: Complete Problems in the Arithmetic Hierarchy

*PDF pages 253–257*

### Lemma 36.1 — Finite-halting completeness lift

**Location:** PDF p. 254; printed p. 243.
**Importance:** core.
**Tags:** arithmetic-hierarchy, complete-problems.

FINHP is many-one complete for Σ₃⁰. More generally, if A is many-one complete for Σₙ⁰, then FIN_A is many-one complete for Σ_{n+2}⁰.

## Lecture 37: Post’s Problem

*PDF pages 258–263*

### Concept — Many-one and Turing degrees

**Location:** PDF p. 258; printed p. 247.
**Importance:** foundational.
**Tags:** reducibility, degrees.

A≤ₘB uses a total recursive many-one map; A≤ᵀB means A is decidable with oracle B. Mutual reducibility defines m-degrees and Turing degrees.

### Theorem 37.1 — Post’s theorem on intermediate m-degrees

**Location:** PDF p. 259; printed p. 248.
**Importance:** core.
**Tags:** recursion-theory, degrees.

There exists a recursively enumerable, nonrecursive language that is not r.e.-complete.

### Definition 37.2 — Immune set

**Location:** PDF p. 260; printed p. 249.
**Importance:** foundational.
**Tags:** recursion-theory, degrees.

A set A⊆N is immune when it is infinite but contains no infinite recursively enumerable subset.

### Definition 37.3 — Simple set

**Location:** PDF p. 260; printed p. 249.
**Importance:** foundational.
**Tags:** recursion-theory, degrees.

A set B⊆N is simple when B is recursively enumerable and its complement is immune; equivalently, the complement is infinite and B meets every infinite r.e. set.

### Definition 37.4 — Productive set

**Location:** PDF p. 260; printed p. 249.
**Importance:** foundational.
**Tags:** recursion-theory, degrees.

A set C⊆N is productive when there is a total recursive function σ such that Wₓ⊆C implies σ(x)∈C∖Wₓ. Such σ is a productive function.

### Lemma 37.6 — Existence of a simple set

**Location:** PDF p. 261; printed p. 250.
**Importance:** technical.
**Tags:** recursion-theory, degrees.

There exists a simple set.

### Lemma 37.7 — Simple complements are not productive

**Location:** PDF p. 261; printed p. 250.
**Importance:** technical.
**Tags:** recursion-theory, degrees.

If B is simple, then its complement is not productive.

### Lemma 37.8 — Completeness implies productivity of the complement

**Location:** PDF p. 261; printed p. 250.
**Importance:** technical.
**Tags:** recursion-theory, degrees.

If A is r.e.-complete, then its complement is productive.

## Lecture 38: The Friedberg–Muchnik Theorem

*PDF pages 264–267*

### Theorem 38.1 — Friedberg–Muchnik theorem

**Location:** PDF p. 264; printed p. 253.
**Importance:** core.
**Tags:** priority-method, degrees.

There exists an r.e. set A of intermediate Turing degree: ∅ <ᵀ A <ᵀ K.

**Why it matters:** Solves Post’s problem by constructing an intermediate r.e. Turing degree.

### Definition 38.2 — Low set

**Location:** PDF p. 265; printed p. 254.
**Importance:** foundational.
**Tags:** priority-method, degrees.

An r.e. set A is low when Kᴬ ≤ᵀ K; equivalently, the halting problem relative to A is no harder than the ordinary halting problem.

### Lemma 38.3 — Low sets are incomplete

**Location:** PDF p. 265; printed p. 254.
**Importance:** technical.
**Tags:** priority-method, degrees.

If A is low, then A <ᵀ K.

### Lemma 38.4 — Low simple set

**Location:** PDF p. 265; printed p. 254.
**Importance:** technical.
**Tags:** priority-method, degrees.

There exists a low simple set.

## Lecture 39: The Analytic Hierarchy

*PDF pages 268–273*

### Concept — Analytic hierarchy

**Location:** PDF p. 268; printed p. 257.
**Importance:** foundational.
**Tags:** analytic-hierarchy, second-order-logic.

The analytic hierarchy extends the arithmetic hierarchy by allowing second-order quantification over sets or functions; its first universal level Π₁¹ contains well-foundedness-type problems.

## Lecture 40: Kleene’s Theorem

*PDF pages 274–277*

### Theorem 40.1 — Kleene’s theorem

**Location:** PDF p. 275; printed p. 264.
**Importance:** core.
**Tags:** kleene, analytic-hierarchy.

Over the natural numbers, the inductive relations are exactly the Π₁¹ relations, and the hyperelementary relations are exactly the Δ₁¹ relations.

**Why it matters:** Connects inductive definitions with the first analytic level.

### Theorem 40.2 — Ordinal characterization of inductive sets

**Location:** PDF p. 277; printed p. 266.
**Importance:** supporting.
**Tags:** kleene, analytic-hierarchy.

A set A⊆N is inductive iff there is a hyperelementary relation R with A={x:∃α<ω₁^{CK} R(x,α)}; equivalently, the existential witness can be a code for a recursive ordinal.

## Lecture 41: Fair Termination and Harel’s Theorem

*PDF pages 278–423*

### Concept — Fair termination

**Location:** PDF p. 278; printed p. 267.
**Importance:** foundational.
**Tags:** program-verification, analytic-hierarchy.

A computation tree is fairly terminating when every fair path terminates; the lecture reduces this property to well-foundedness of recursively encoded ω-trees.

### Theorem 41.1 — Harel’s theorem

**Location:** PDF p. 282; printed p. 271.
**Importance:** core.
**Tags:** fair-termination, program-verification.

There is a recursive bijective encoding τ from binary trees to nontrivial full ω-trees such that a binary tree is fairly terminating for the condition (true,last(0)) iff τ(T) is well-founded.

### Corollary 41.2 — Complexity of fair termination

**Location:** PDF p. 282; printed p. 271.
**Importance:** core.
**Tags:** fair-termination, program-verification.

Fair termination is Π₁¹-complete.

**Why it matters:** Places a natural program-termination problem at Π₁¹-complete complexity.

# Source: NP and NP completeness (Chapter 2)

**Source file:** `np_and_np_completeness.pdf`

## Section 2.1: The Class NP

*PDF pages 2–4*

### Definition 2.1 — Verifier definition of NP

**Location:** PDF p. 2; printed p. 39.
**Importance:** foundational.
**Tags:** np, certificates, nondeterminism.

A language L is in NP iff there are a polynomial p and a polynomial-time verifier M such that x∈L exactly when some certificate u∈{0,1}^{p(|x|)} satisfies M(x,u)=1.

### Concept — Certificate / witness

**Location:** PDF p. 2; printed p. 39.
**Importance:** foundational.
**Tags:** np, certificates.

A polynomial-length string u that causes a polynomial-time verifier M(x,u) to accept, thereby certifying that x is a yes-instance of an NP language.

### Claim 2.4 — Basic inclusions

**Location:** PDF p. 4; printed p. 41.
**Importance:** supporting.
**Tags:** np, certificates, nondeterminism.

P ⊆ NP ⊆ EXP.

### Definition 2.5 — Nondeterministic time

**Location:** PDF p. 4; printed p. 41.
**Importance:** foundational.
**Tags:** np, certificates, nondeterminism.

L∈NTIME(T(n)) when some nondeterministic TM decides L in O(T(n)) time on every computation branch.

### Theorem 2.6 — Machine characterization of NP

**Location:** PDF p. 4; printed p. 41.
**Importance:** core.
**Tags:** np, certificates, nondeterminism.

NP = ⋃_{c∈N} NTIME(nᶜ).

### Concept — Nondeterministic Turing machine

**Location:** PDF p. 4; printed p. 41.
**Importance:** foundational.
**Tags:** np, nondeterminism.

A TM with multiple transition choices. It accepts an input when at least one sequence of nondeterministic choices reaches the accepting state.

## Section 2.2: Reducibility and NP-Completeness

*PDF pages 5–6*

### Definition 2.7 — Karp reduction, NP-hardness, NP-completeness

**Location:** PDF p. 5; printed p. 42.
**Importance:** foundational.
**Tags:** reductions, np-completeness.

L≤ᵖL′ when a polynomial-time function f maps x∈L exactly to f(x)∈L′. A language is NP-hard if every NP language reduces to it, and NP-complete if it is both NP-hard and in NP.

### Theorem 2.8 — Consequences of polynomial reductions

**Location:** PDF p. 6; printed p. 43.
**Importance:** core.
**Tags:** reductions, np-completeness.

(1) Polynomial-time Karp reductions are transitive. (2) If an NP-hard language lies in P, then P=NP. (3) An NP-complete language lies in P iff P=NP.

### Theorem 2.9 — NP-completeness of TMSAT

**Location:** PDF p. 6; printed p. 43.
**Importance:** core.
**Tags:** reductions, np-completeness.

TMSAT = {⟨α,x,1ⁿ,1ᵗ⟩ : some u∈{0,1}ⁿ makes machine Mα accept ⟨x,u⟩ within t steps} is NP-complete.

## Section 2.3: The Cook-Levin Theorem: Computation Is Local

*PDF pages 7–12*

### Concept — CNF, SAT, and 3SAT

**Location:** PDF p. 7; printed p. 44.
**Importance:** foundational.
**Tags:** sat, cnf, np-completeness.

A CNF formula is a conjunction of clauses, each a disjunction of literals. SAT asks whether a CNF formula is satisfiable; 3SAT restricts each clause to at most three literals.

### Theorem 2.10 — Cook–Levin theorem

**Location:** PDF p. 8; printed p. 45.
**Importance:** core.
**Tags:** cook-levin, sat.

SAT is NP-complete, and 3SAT is NP-complete.

**Why it matters:** The central theorem establishing natural NP-complete problems.

### Lemma 2.11 — NP-hardness of SAT

**Location:** PDF p. 8; printed p. 45.
**Importance:** supporting.
**Tags:** cook-levin, sat.

SAT is NP-hard.

### Claim 2.13 — Universality of AND, OR, NOT

**Location:** PDF p. 9; printed p. 46.
**Importance:** supporting.
**Tags:** cook-levin, sat.

Every Boolean function f:{0,1}^ℓ→{0,1} has an ℓ-variable CNF formula of size at most ℓ·2^ℓ that computes f.

### Lemma 2.14 — Reduction from SAT to 3SAT

**Location:** PDF p. 12; printed p. 49.
**Importance:** supporting.
**Tags:** cook-levin, sat.

SAT ≤ᵖ 3SAT.

## Section 2.4: The Web of Reductions

*PDF pages 13–16*

### Concept — Levin and parsimonious reductions

**Location:** PDF p. 13; printed p. 50.
**Importance:** foundational.
**Tags:** reductions, counting.

A Levin reduction efficiently maps both instances and witnesses between NP problems. A parsimonious reduction additionally preserves the number of witnesses.

### Theorem 2.15 — NP-completeness of independent set

**Location:** PDF p. 14; printed p. 51.
**Importance:** core.
**Tags:** np-complete-problems, reductions.

INDSET is NP-complete.

### Theorem 2.16 — NP-completeness of 0/1 integer programming

**Location:** PDF p. 15; printed p. 52.
**Importance:** core.
**Tags:** np-complete-problems, reductions.

0/1 IPROG is NP-complete.

### Theorem 2.17 — NP-completeness of directed Hamiltonian path

**Location:** PDF p. 16; printed p. 53.
**Importance:** core.
**Tags:** np-complete-problems, reductions.

The directed Hamiltonian path language dHAMPATH is NP-complete.

## Section 2.6: coNP, EXP, and NEXP

*PDF pages 18–19*

### Theorem 2.18 — Decision-to-search under P=NP

**Location:** PDF p. 18; printed p. 55.
**Importance:** core.
**Tags:** conp, exp, nexp.

If P=NP, then for every NP language and every polynomial-time verifier, a valid certificate for any yes-instance can be found in polynomial time.

**Why it matters:** Shows that, for NP problems, efficient decision would yield efficient witness recovery.

### Definition 2.19 — coNP by complementation

**Location:** PDF p. 18; printed p. 55.
**Importance:** foundational.
**Tags:** conp, exp, nexp.

coNP = {L : the complement of L is in NP}.

### Concept — Downward self-reducibility

**Location:** PDF p. 18; printed p. 55.
**Importance:** foundational.
**Tags:** search-vs-decision, self-reduction.

SAT can recover a satisfying assignment by repeatedly fixing one variable and querying satisfiability of the smaller formulas; this converts a decision procedure into a search procedure.

### Definition 2.20 — Universal-certificate characterization of coNP

**Location:** PDF p. 19; printed p. 56.
**Importance:** foundational.
**Tags:** conp, exp, nexp.

A language L is in coNP iff there are a polynomial p and polynomial-time M such that x∈L exactly when M(x,u)=1 for every u∈{0,1}^{p(|x|)}.

### Concept — EXP and NEXP

**Location:** PDF p. 19; printed p. 56.
**Importance:** foundational.
**Tags:** exponential-time, padding.

EXP is deterministic exponential time ⋃₍c₎DTIME(2^{nᶜ}); NEXP is its nondeterministic analogue ⋃₍c₎NTIME(2^{nᶜ}).

## Section 2.7: More Thoughts about P, NP, and All That

*PDF pages 20–30*

### Theorem 2.22 — Padding implication

**Location:** PDF p. 20; printed p. 57.
**Importance:** core.
**Tags:** complexity-philosophy.

If EXP ≠ NEXP, then P ≠ NP.
