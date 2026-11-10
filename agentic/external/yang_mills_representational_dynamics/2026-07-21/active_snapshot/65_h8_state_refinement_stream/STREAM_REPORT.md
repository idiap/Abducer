# H8 retained-state refinement stream

## Scope and present claim

H8 proposes using hostile conditional histories as completeness detectors for a retained boundary state. Its verified content is deliberately narrow: the Stage 52 four-state Markov example starts from an insufficient regular/defect partition, refines by transition signatures, and reaches a lumpable partition. This is a **C1 finite certificate**, not evidence that a bounded, physically sufficient Yang--Mills state exists. The independent stream developed here turns that probe into a theorem-shaped algorithm, a physical boundary-table contract, and an explicit failure test.

The connection to the existing transfer chain is precise. Stage 18 requires a bound after **every positive-probability adaptive history**; moment bounds cannot replace those conditionals. Stage 19 permits a state-weighted bad subkernel (Q) with (QV\le qV), so scalar row sums need not be small. Stage 24 separates regular, center, continuous, cut/orbit, and topology channels and shows that persistence and forced return affect the admissible weight. H8 must therefore refine states using normalized, channel-resolved transition information while leaving the later weighted-contraction problem separate.

## Finite conditional-sufficiency contract

Fix a regulator, finite volume, block, exposure order, boundary convention, and the set (H_+) of positive-mass microscopic histories. Let (P) be a partition of (H_+), interpreted as the retained state map (s_P:H_+\to P). For every declared channel (\alpha), let (K_\alpha(h,h')\ge0) be the exact normalized one-step subkernel, with all conditional partition functions, Haar factors, and chart Jacobians included.

The retained state is one-step conditionally sufficient when, for any (h,g) in the same cell and every destination cell (B\in P),

\[
\sum_{h'\in B}K_\alpha(h,h')
=\sum_{h'\in B}K_\alpha(g,h')
\quad\text{for every }\alpha.
\]

This is channelwise strong lumpability. It says the conditional law of the next retained state and channel depends on the past only through the current retained state. If the exploration also emits a quantity used later (root moment, normalizer class, reflection label, or weight update), its conditional distribution must be appended to the signature. Lumpability of a summed bad kernel alone is not sufficient for multichannel estimates.

## Monotone partition-refinement algorithm

Begin with a physically meaningful seed partition (P_0), not with desired estimates. For round (r), assign each history the signature

\[
\operatorname{sig}_r(h)=\left([h]_{P_r},
  \big(\sum_{h'\in B}K_\alpha(h,h')\big)_{\alpha,B\in P_r},
  \text{declared emitted data}\right).
\]

Split each cell into equality classes of these signatures to obtain (P_{r+1}). Never merge cells. Stop when (P_{r+1}=P_r). Exact arithmetic, symbolic expressions, or certified disjoint intervals should be used; decimal rounding is only a probe and cannot certify equality.

For finite (H_+), every strict round increases the number of cells, so termination occurs after at most (|H_+|-|P_0|) strict refinements. The stable partition is lumpable and is the coarsest lumpable refinement of the seed for the declared kernels and outputs. This generic statement is a candidate C2 finite theorem once written and proved independently of floating-point behavior. It says nothing about whether the answer is small, geometric, uniform, or closed under another block step.

## H8 certificate and counterexamples

The Stage 52 kernel has rows

```text
(0.9,0,0.1,0), (0,0.9,0,0.1), (1,0,0,0), (0,0,0,1)
```

and seed labels `(0,0,1,1)`. The initial lumpability defect is one. First, the two defect states split because one returns to the regular block while the other persists. On the next round, the regular states split because they feed the two newly distinct defect states. The stable labels are `(0,1,2,3)`, with defect zero. Thus the algorithm terminates after two strict splits, but only by remembering every hidden state. It proves detection, not compression.

Three nearby failures delimit the design. First, the Stage 18 law supported on `10` and `01` obeys intersection-moment bounds at (q=1/2) but has a positive history with next-bit bad probability one; refinement must inspect conditional rows, not event moments. Second, the Stage 19 two-state example has scalar ceiling one while a positive weight stores rare-entry cost and yields (QV=qV); state sufficiency does not imply contraction. Third, Stage 24 shows that channels with different entry, return, or persistence parameters cannot safely be lumped merely because all are called “bad.” In particular, any persistence (c_i\ge q) kills the canonical weighted ceiling, while the entry budget is of order (q^2). Refinement must preserve these distinctions before weights are optimized.

## Physical boundary tables

The first implementation artifact should contain two linked exact tables.

| Boundary-history table field | Required role | Split trigger |
|---|---|---|
| history key and positive-mass proof | fixes the adaptive conditioning domain | absent/zero-mass ambiguity |
| continuous collar data and chart owner | retains local boundary geometry | unequal normalized row or Jacobian class |
| center flux | tracks center channel | unequal sector transition |
| orbit/cut label and transition | tracks atlas ownership changes | unequal cut/orbit row |
| integer topological carrier | replaces center-plus-charge shorthand | unequal topology row |
| gauge-orbit and reflection partner | audits covariance and OS compatibility | broken equivariance |

| Transition table field | Required role |
|---|---|
| source history, destination history, channel | identifies an exact subkernel entry |
| numerator and conditional denominator | prevents normalization from being erased |
| Haar/Jacobian factor and chart complement | preserves the complete measure |
| exact value or rigorous interval with provenance | supports certified equality/splitting |
| destination seed labels at each scale | generates refinement signatures |

Symmetry reduction is allowed only after proving that the kernel and every emitted datum are equivariant. The table must include hostile positive-mass histories; discarding them because they spoil a bound invalidates Stage 18's premise.

## State explosion and physical stop rules

Finite termination is automatic; useful termination is not. Record at every round the number and sizes of cells, the physical feature responsible for each split, maximum lumpability defect, and whether representatives admit a gauge-covariant label. Declare **state explosion** if the stable state is essentially the full history table, if the cell count/support grows without a volume-independent bound, if continuous distinctions require uncontrolled precision, or if one further block step creates new label types without a contractive recursion. In any of these cases H8 has falsified the proposed finite retained description; it has not licensed an ad hoc extra label or an RG claim.

## Next theorem and guardrails

The next open result is the **physical one-block boundary-table sufficiency theorem**: for one frozen finite SU(2) heat-kernel block and all positive-mass histories, construct the exact channel-resolved tables above; prove that refinement terminates in a gauge-covariant, reflection-compatible partition described by the declared continuous, center, cut/orbit, and integer-topology data; and prove exact channelwise lumpability. Report the cell-growth law and apply the block once more as a closure test.

Claim discipline is strict. The existing H8 result remains C1. A proof of the abstract finite refinement theorem, or an exact frozen-table theorem, may be labeled C2 with its restrictions stated. No C3 claim of uniform physical conditional sufficiency, basin entry, repeated RG, continuum Yang--Mills, or a Hamiltonian mass gap follows. Even successful lumpability does not establish (QV\le qV); the Stage 19/24 weight and physical channel inequalities remain separate dependencies.
