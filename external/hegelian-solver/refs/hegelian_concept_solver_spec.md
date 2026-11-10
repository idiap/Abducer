<!--
SPDX-FileCopyrightText: Copyright © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Solver-Implementable Formalization of Dialectical Concept Development in Mathematics

## 1. Aim

This document turns the Hegelian schema of mathematical concept development into a solver-oriented formal framework. The goal is not to encode Hegel's metaphysics directly, but to extract a computationally usable pattern:

> A concept is represented as a typed mathematical structure with operations, constraints, examples, and intended tasks. A concept develops when the solver detects a determinate failure such as non-closure, incompleteness, insufficient expressivity, excessive rigidity, or representational dependence. A constructive extension is then proposed and verified by proof obligations.

The Hegelian notions are operationalized as follows:

| Hegelian notion | Solver interpretation |
|---|---|
| Concept | Typed theory/module/signature with axioms, operations, models, tasks |
| Determinate negation | A typed counterexample or failed proof obligation exposing a specific limit |
| Contradiction | Structured incompatibility between intended task and current concept constraints |
| Aufhebung | Constructive transformation producing a richer concept that preserves the old one as an embedding, quotient, completion, extension, or abstraction |
| Preservation | Existence of an interpretation/embedding from old concept into new concept |
| Elevation | The new concept satisfies tasks that failed in the old concept |
| Mediation | Explicit morphism, abstraction map, quotient map, completion map, or representation map connecting stages |

## 2. Basic formal objects

Let a concept be a tuple:

\[
C = (\Sigma, A, M, T, I, P)
\]

where:

- \(\Sigma\) is a typed signature of sorts, constants, functions, predicates, and relations.
- \(A\) is a set of axioms over \(\Sigma\).
- \(M\) is a class of admissible models satisfying \(A\).
- \(T\) is a set of intended tasks or desiderata.
- \(I\) is an interface specifying admissible operations and queries.
- \(P\) is a set of preservation constraints that must remain valid under future transformations.

A task is represented as:

\[
\tau = (\phi, \kappa, \rho)
\]

where:

- \(\phi\) is a formula, construction request, or query.
- \(\kappa \in \{\textsf{prove}, \textsf{construct}, \textsf{decide}, \textsf{compute}, \textsf{classify}\}\).
- \(\rho\) is a required status such as valid, satisfiable, computable, closed, complete, invariant, or unique up to equivalence.

The solver evaluates:

\[
\operatorname{Eval}(C,\tau) \in \{\textsf{success}, \textsf{failure}(F), \textsf{unknown}\}
\]

where \(F\) is a typed failure certificate.

## 3. Failure certificates as determinate negations

A determinate negation is not an arbitrary rejection of a concept. It is a structured failure:

\[
F = (\ell, w, \psi, \Gamma)
\]

where:

- \(\ell\) is a failure label.
- \(w\) is a witness or counterexample.
- \(\psi\) is the failed obligation.
- \(\Gamma\) is the dependency trace showing which axioms, operations, and intended tasks generated the failure.

Canonical labels:

\[
\ell \in \{
\textsf{NonClosure},
\textsf{NonSolvability},
\textsf{Incompleteness},
\textsf{NonInvariance},
\textsf{Rigidity},
\textsf{Inconsistency},
\textsf{Undecidability},
\textsf{NonRepresentability},
\textsf{AmbiguousEquivalence}
\}.
\]

Examples:

- \(3 - 5 \notin \mathbb{N}\): \(\textsf{NonClosure}\).
- \(x^2 + 1 = 0\) has no solution in \(\mathbb{R}\): \(\textsf{NonSolvability}\).
- A Cauchy sequence in \(\mathbb{Q}\) has no rational limit: \(\textsf{Incompleteness}\).
- A construction changes under coordinate representation: \(\textsf{NonInvariance}\).
- Strict equality is too strong for structural classification: \(\textsf{Rigidity}\).

## 4. Concept transformations

A concept transformation is an operator:

\[
\Theta : (C,F) \mapsto C'
\]

where \(C'\) is a candidate successor concept.

Canonical transformation types:

| Failure | Transformation | Mathematical example |
|---|---|---|
| NonClosure | Closure completion | \(\mathbb{N} \to \mathbb{Z}\) |
| NonSolvability | Algebraic extension | \(\mathbb{R} \to \mathbb{C}\) |
| Incompleteness | Metric/order completion | \(\mathbb{Q} \to \mathbb{R}\) |
| NonInvariance | Quotient / invariant representation | coordinate expressions \(\to\) tensors |
| Rigidity | Equivalence weakening | equality \(\to\) isomorphism/equivalence |
| Inconsistency | Axiomatic restriction or stratification | naive set theory \(\to\) ZF/type theory |
| NonRepresentability | Abstraction / categorical lifting | functions \(\to\) morphisms/functors |

## 5. Aufhebung as a verified repair operator

A transformation \(\Theta(C,F)=C'\) counts as an Aufhebung only if it satisfies three proof obligations.

### 5.1 Preservation

There must be an interpretation, embedding, or faithful translation:

\[
\iota : C \hookrightarrow C'
\]

such that for all preserved propositions \(p \in P\):

\[
C \models p \implies C' \models \iota(p).
\]

### 5.2 Resolution

The original failed task must become solvable, or the failure must be relocated into an explicitly characterized boundary condition:

\[
\operatorname{Eval}(C', \iota(\tau)) = \textsf{success}
\]

or:

\[
\operatorname{Eval}(C', \iota(\tau)) = \textsf{failure}(F')
\quad\text{with}\quad
\operatorname{rank}(F') < \operatorname{rank}(F).
\]

### 5.3 Non-collapse

The successor concept must not trivialize the theory:

\[
\operatorname{Consistent}(C')
\]

and it must not identify distinctions protected by \(P\):

\[
\forall a,b.\; \operatorname{ProtectedDistinct}_C(a,b) \implies \operatorname{ProtectedDistinct}_{C'}(\iota(a),\iota(b)).
\]

Thus:

\[
\operatorname{Aufhebung}(C,F,C') \iff
\operatorname{Preserve}(C,C') \land
\operatorname{Resolve}(F,C') \land
\operatorname{NonCollapse}(C').
\]

## 6. Solver loop

The solver performs iterative concept development:

```text
Input: initial concept C0, task set T, transformation library L
Output: concept chain C0 -> C1 -> ... -> Cn with proof certificates

C := C0
Trace := []
repeat:
    failures := []
    for task τ in C.T:
        r := Eval(C, τ)
        if r = failure(F):
            failures.append(F)

    if failures is empty:
        return Success(C, Trace)

    F* := SelectMostDeterminate(failures)
    candidates := []

    for Θ in L.applicable(F*):
        C_candidate := Θ(C, F*)
        obligations := GenerateObligations(C, F*, C_candidate)
        status := ProveObligations(obligations)
        if status.success:
            candidates.append((C_candidate, status.certificates))

    if candidates is empty:
        return Stuck(C, F*, Trace)

    C_next := RankCandidates(candidates)
    Trace.append((C, F*, C_next, certificates))
    C := C_next
until resource limit
```

## 7. Ranking candidate concept extensions

Candidate concepts can be ranked by a multi-objective score:

\[
S(C') =
\alpha R(C') + \beta P(C') + \gamma E(C') + \delta I(C') - \lambda K(C')
\]

where:

- \(R(C')\): resolution score for failed tasks.
- \(P(C')\): preservation score for old theorems and constructions.
- \(E(C')\): expressivity gain.
- \(I(C')\): invariance gain.
- \(K(C')\): complexity cost.

The solver chooses:

\[
C_{n+1} = \arg\max_{C' \in \mathcal{Cand}(C_n,F_n)} S(C').
\]

## 8. Minimal DSL sketch

A solver-friendly concept specification may use the following abstract DSL.

```yaml
concept: Naturals
sorts:
  - Nat
operations:
  zero: Nat
  succ: Nat -> Nat
  add: Nat x Nat -> Nat
  sub: Nat x Nat -> Nat?   # partial
axioms:
  - PeanoAxioms
intended_tasks:
  - name: closed_subtraction
    kind: construct
    formula: forall a b: Nat, exists c: Nat, c = a - b
    required: closed
preserve:
  - addition_laws
  - order_laws
failure_handlers:
  NonClosure:
    - GrothendieckGroupCompletion
```

The transformation produces:

```yaml
concept: Integers
extends: Naturals
embedding:
  from: Nat
  to: Int
  map: n -> class(n, 0)
sorts:
  - Int
operations:
  zero: Int
  succ: Int -> Int
  add: Int x Int -> Int
  neg: Int -> Int
  sub: Int x Int -> Int
axioms:
  - AbelianGroupUnderAddition
  - NatEmbeddingPreservesAddition
proof_obligations:
  - preserves_addition_laws
  - resolves_closed_subtraction
  - noncollapse_nat_embedding_injective
```

## 9. Implementation architecture

A practical implementation can be decomposed into the following modules.

### 9.1 Concept Registry

Stores signatures, axioms, tasks, embeddings, and known transformations.

### 9.2 Evaluation Engine

Dispatches proof, model finding, SMT solving, type checking, and counterexample search.

Backends may include:

- SMT solvers for first-order fragments.
- CAS systems for algebraic constructions.
- theorem provers such as Lean/Coq/Isabelle for certified obligations.
- model finders such as Alloy/Mace-style engines for finite counterexamples.

### 9.3 Failure Classifier

Maps failed tasks to determinate failure certificates.

### 9.4 Transformation Library

Contains operators such as:

- closure completion;
- quotient formation;
- localization;
- completion;
- algebraic extension;
- categorical abstraction;
- equivalence weakening;
- stratification/type refinement.

### 9.5 Obligation Generator

Generates preservation, resolution, consistency, and non-collapse obligations.

### 9.6 Candidate Ranker

Chooses among multiple valid successor concepts.

### 9.7 Trace Explainer

Records the chain:

\[
C_0 \xrightarrow{F_0,\Theta_0} C_1 \xrightarrow{F_1,\Theta_1} \cdots \xrightarrow{F_{n-1},\Theta_{n-1}} C_n
\]

with proof certificates and human-readable explanations.

## 10. Example: number-system development

### Stage 1: Naturals

Task:

\[
\forall a,b\in\mathbb{N},\; \exists c\in\mathbb{N}: c = a-b.
\]

Counterexample:

\[
3-5 \notin \mathbb{N}.
\]

Failure:

\[
F = \textsf{NonClosure}(\operatorname{sub},3,5).
\]

Transformation:

\[
\Theta = \textsf{GroupCompletion}.
\]

Successor:

\[
\mathbb{Z}.
\]

Proof obligations:

1. \(\mathbb{N}\) embeds into \(\mathbb{Z}\).
2. Addition is preserved.
3. Subtraction is total in \(\mathbb{Z}\).
4. The embedding is injective.

### Stage 2: Integers

Task:

\[
\forall a,b\in\mathbb{Z}, b\neq 0, \exists c\in\mathbb{Z}: c = a/b.
\]

Counterexample:

\[
3/5 \notin \mathbb{Z}.
\]

Failure:

\[
F = \textsf{NonClosure}(\operatorname{div},3,5).
\]

Transformation:

\[
\Theta = \textsf{FieldOfFractions}.
\]

Successor:

\[
\mathbb{Q}.
\]

## 11. Solver-readable output trace

A solver should emit traces like:

```json
{
  "from_concept": "Naturals",
  "failed_task": "closed_subtraction",
  "failure": {
    "label": "NonClosure",
    "operation": "sub",
    "witness": [3, 5],
    "failed_obligation": "exists c: Nat, c = 3 - 5"
  },
  "transformation": "GroupCompletion",
  "to_concept": "Integers",
  "obligations": [
    {"name": "nat_embedding_injective", "status": "proved"},
    {"name": "addition_preserved", "status": "proved"},
    {"name": "subtraction_total", "status": "proved"},
    {"name": "noncollapse", "status": "proved"}
  ],
  "hegelian_interpretation": {
    "determinate_negation": "Naturals are inadequate for total subtraction.",
    "preservation": "Naturals embed into integers.",
    "elevation": "Subtraction becomes total."
  }
}
```

## 12. Lean-oriented encoding sketch

In Lean-style terms, a concept can be represented as a structure containing a carrier, operations, laws, tasks, and preservation properties.

```lean
structure Concept where
  Carrier : Type
  ops     : OperationSignature Carrier
  laws    : Prop
  tasks   : List Task
  preserve : List Prop

structure Failure where
  label : FailureLabel
  witness : Option Witness
  obligation : Prop
  trace : List Dependency

structure Transformation where
  name : String
  apply : Concept -> Failure -> Concept
  obligations : Concept -> Failure -> Concept -> List Prop

structure Aufhebung (C C' : Concept) (F : Failure) where
  embedding : C.Carrier -> C'.Carrier
  preserve_obligations : AllProved (Preserve C C' embedding)
  resolution_obligations : AllProved (Resolve F C')
  noncollapse_obligations : AllProved (NonCollapse C C' embedding)
```

For concrete mathematical domains, this should use Lean's existing algebraic hierarchy where possible:

- `Nat` with partial subtraction issue represented as an intended totality task.
- `Int` as additive group completion.
- `Rat` as field of fractions.
- `Real` as completion.
- `Complex` as algebraic extension of `Real` by a square root of `-1`.

## 13. Key design principle

The central computational move is:

\[
\text{philosophical contradiction}
\quad\leadsto\quad
\text{typed failure certificate}
\quad\leadsto\quad
\text{constructive transformation}
\quad\leadsto\quad
\text{verified proof obligations}.
\]

This makes dialectical concept development implementable as a solver loop.
