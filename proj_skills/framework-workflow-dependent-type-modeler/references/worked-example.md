<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# A claim-sensitive presentation of the abductive route

This example is a reusable modeling pattern, not frozen publication evidence. Re-extract `abducer-prism/workflows/abducer_work_loop/{types,occurrences,relations,reasoning,materialization}.prism` before citing it in a paper. All proposed types below belong to the authoring model.

## Native layer in context

Abbreviate the exact nominal types as follows:

```text
G = ActiveProofGap                 H = ProofRouteHypothesis
C = ProofRouteDerivedClaim         V = ProofRouteRefutationAssessment
J = ProofWorkRoutingInput           S = ProofWorkRoutingAssessment

A : G -> Generated[H]              D : H -> Generated[C]
R : C -> Generated[V]              E : J -> Generated[S]
J has fields derived_claim:C and refutation_assessment:V
```

`A,D,R,E` label the four occurrence declarations in their source order. They are opaque signature symbols in this presentation; they do not denote proven total executable functions. Write the native declaration as a context extension, with each expression typed under preceding bindings:

```text
g:G
hg:Generated[H] := A(g)
h:H := hg.value
cg:Generated[C] := D(h)       [TreatsProofRouteAsClaimPremise(h,cg)]
c:C := cg.value
vg:Generated[V] := R(c)       [TestsProofRouteDerivedClaim(c,vg)]
v:V := vg.value
j:J := ProofWorkRoutingInput(derived_claim=c, refutation_assessment=v)
sg:Generated[S] := E(j)       [CalibratesProofWorkRouting(j,sg)]
```

The `.value` uses and record construction are source-explicit adapters. The relation labels are annotations with generated targets, not additional constructed proof terms. The materialization layer provides three relation builders that construct source/target records; these do not prove the scientific content of either value. A comment in `relations.prism` describes builders as future work, so preserve this comment-versus-implementation discrepancy instead of treating the comment as the current implementation state. Retaining `c` records the same source binding passed to `R` and the routing input. The native type `V` contains a string field, not an index enforcing the association with this particular `c`. No pair typing rule prevents native `J` from combining some other `c′:C` with `v:V`.

The occurrence declaration signatures above omit materialization details by explicit scope: the materialized agents declare `Result[Generated[T], ModelFailure]` with effects `{AI.Generate, Context.Disclose}`. Any presentation of that layer must preserve its failure boundary and effects separately; this local declaration telescope does not prove successful effectful evaluation.

## Proposed refinement: assessment data tied to its source claim

Declare an abstract family `Linked(c,v) : Type` under `c:C,v:V`. Its stipulated inhabitant contract is a provenance record connecting exactly claim artifact `c` to assessment data `v` through the relevant assessment occurrence; it is not a proposition that `c` is scientifically true. Source bindings motivate this contract, but native code provides no dependent-family checker or general producer of such records.

Define in the proposed mathematical model:

```text
Vhat(c) := Σ(v:V). Linked(c,v)
Jhat    := Σ(c:C). Vhat(c)

Rhat : Π(c:C). Generated[Vhat(c)]          [proposed; realization unresolved]
erase : Jhat -> J
erase(p) := ProofWorkRoutingInput(
              derived_claim=π₁(p),
              refutation_assessment=π₁(π₂(p)))
Ehat : Jhat -> Generated[S]
Ehat(p) := E(erase(p))                    [proposed descriptive adapter]
```

Dependence is genuine: `Linked(c,v)` constrains admissible pair inhabitants by the exact claim and assessment values. `Jhat` retains the exact claim in the type of its second component. `Ehat` has an ordinary arrow because its displayed result type has no value-dependent index. Do not decorate it with a dependent `Π` merely for style. The mathematical erasure map forgets linkage data; it establishes no ability to construct linkage data from every native `J`.

Under the proposed signature `Rhat` and an explicitly proposed wrapper-value projection for its new payload, the local derivation is:

```text
Γ,c:C ⊢ Rhat(c) : Generated[Vhat(c)]       [dependent application]
Γ,c:C,vg:Generated[Vhat(c)] ⊢ vg.value : Vhat(c)
Γ,c:C,vhat:Vhat(c) ⊢ (c,vhat) : Jhat       [dependent pair]
Γ,c:C,vhat:Vhat(c) ⊢ Ehat((c,vhat)) : Generated[S]
```

This derivation explains a possible stronger boundary; it does not upgrade native `R`. A realization must supply the linkage family, its record producer, wrapper accessor support, and enforcement of exact indices. These remain obligations. An alternative future implementation can preserve the full generated assessment inside the linkage contract; it must then state that wrapper-preserving contract and adapter explicitly.

## Mismatch and equality

With `c₁:C,c₂:C,v₁:Vhat(c₁)`, the proposed pair `(c₂,v₁):Jhat` is unsupported unless the indices convert under declared definitional rules or a supplied `p:Id_C(c₁,c₂)` justifies explicit `transport_Vhat(p,v₁):Vhat(c₂)`. Matching field strings, names, graph endpoints, a calibration certificate, or a successful replay supplies neither kind of equality. In contrast, substituting the same argument `a:C` consistently for `c` yields `vhat[a/c]:Vhat(a)`; this is capture-avoiding substitution in the presentation, not a Prism metatheorem.

## Paper boundary

This notation makes a specific desired association visible and contrasts it with the current nominal record. It does not turn `Linked` into proof of the claim or `S` into a theorem. The alternatives `ReadyForReleasePromotion`, `Reframe`, `Retarget`, and `Refuted` remain returned data unless source routing executes them. Keep original ERFL branches distinct from the simpler native sequence, and keep retained values separate from resource duplication semantics.

When mapping the category example to this presentation, associate its retained claim boundary with the telescope and its packing adapter with the record constructor. This is a notation correspondence, not a proved equivalence of categories or a comprehension-category semantics.
