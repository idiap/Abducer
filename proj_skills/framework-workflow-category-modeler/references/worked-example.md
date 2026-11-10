<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Native abductive route with retained context

This is a modeling pattern, not frozen publication evidence. Refresh extraction before use. The inspected source is `abducer-prism/workflows/abducer_work_loop/{types,occurrences,relations,reasoning}.prism`.

```text
A : ActiveProofGap -> Generated[ProofRouteHypothesis]
D : ProofRouteHypothesis -> Generated[ProofRouteDerivedClaim]
R : ProofRouteDerivedClaim -> Generated[ProofRouteRefutationAssessment]
E : ProofWorkRoutingInput -> Generated[ProofWorkRoutingAssessment]

ProofWorkRoutingInput = {
  derived_claim: ProofRouteDerivedClaim,
  refutation_assessment: ProofRouteRefutationAssessment
}
```

The paper's `E ∘ R ∘ D ∘ A` describes an epistemic motif. Those exact native signatures do not directly compose: outputs are wrapped, and `E` needs both claim and assessment.

Let `G,H,C,V,J,S` abbreviate the six native types above, with `J = ProofWorkRoutingInput`. Write `Gen[T]` for the literal wrapper, without asserting a functor. A boundary object `B` has ports `{claim: C, assessment: Gen[V]}`; braces denote a record bundle, not a categorical product.

| Generator | Domain → codomain | Evidence and interpretation |
| --- | --- | --- |
| `a` | `G → Gen[H]` | Abductive occurrence |
| `unwrap_h` | `Gen[H] → H` | Explicit `route_hypothesis.value` |
| `d` | `H → Gen[C]` | Deductive occurrence, annotated `TreatsProofRouteAsClaimPremise` |
| `unwrap_c` | `Gen[C] → C` | Explicit `derived_claim.value` |
| `r_context` | `C → B` | Refutational occurrence with the same claim binding retained |
| `pack_j` | `B → J` | Explicit `ProofWorkRoutingInput` construction using claim and `refutation_assessment.value` |
| `e` | `J → Gen[S]` | Evidential occurrence, annotated `CalibratesProofWorkRouting` |

`r_context` models a declared binding in context, not a new implemented operation. Its evidence comes from the refutation occurrence and the later record constructor. It carries `TestsProofRouteDerivedClaim`. Record this distinction in the packet's contextual-occurrence fields rather than implying an unobserved native signature.

The finite path is:

```text
G --a--> Gen[H] --unwrap_h--> H --d--> Gen[C]
  --unwrap_c--> C --r_context--> B --pack_j--> J --e--> Gen[S]
```

Its composition is `e ∘ pack_j ∘ r_context ∘ unwrap_c ∘ d ∘ unwrap_h ∘ a`. Matching adjacent endpoints checks typing of this descriptive path; it proves neither handler execution nor truth. Assumption preserves conditionality. The output alternatives `ReadyForReleasePromotion`, `Reframe`, `Retarget`, and `Refuted` do not add executed outgoing arrows to the native declaration.

Place the retention explanation beside the appendix diagram and attach provenance/evidence posture. Preserve original-versus-native branch discrepancies. Guards extracted from an original ERFL workflow must retain that provenance rather than being attributed to the simpler native reasoning declaration.

## Review probes

- Erasing `Generated` or giving `E` the domain `V` loses required boundaries: restore adapters and the claim-bearing bundle.
- Equal endpoints do not make alternative paths commute; retain both until an equality notion and witness exist.
- An unordered parallel block should retain its partial order and join, not inherit this example's sequence or a product claim.
- Missing packing expressions or retained-binding evidence leave composition unresolved; return to extraction instead of inventing a copy operation.
