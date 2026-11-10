# State-Weighted Nonlinear Frontier: Synthesis

> **Stages 23--26 update.**  The centered-reference local normalization gate
> is now closed by dependency-safe cylinders, and the remaining physical
> problem has been reduced to a uniform weighted conditional partition-ratio
> inequality.  See `PARTITION_RATIO_FRONTIER_SYNTHESIS.md` for the current
> frontier.

## Strongest new result

The local probability/nonlinearity overlap obstruction has been removed at
the frozen finite scale.

The Stage 17 global `408`-ball required a diagnostic radius `0.02463088` and
therefore appeared incompatible with the Stage 8 nonlinear radius.  Stage 21
replaces that global ball by the correct dependency-safe four-link local
constraint.  Its degree-18 typical radius is

```text
r_typ = 0.006023157807602598.
```

Stage 22 proves that the exact identity Hessian of the four-factor plaquette
logarithm has norm

```text
1+sqrt(2) = 2.414213562373095.
```

Transporting this exact value with the certified third derivative gives at
`r_typ`:

| quantity | certified value |
|---|---:|
| total nonlinear Hessian remainder | `0.4746710866` |
| nonlinear physical singular floor | `1.3742159724` |
| fiber margin | `1.5253289134` |
| generated-base margin | `0.6888073894` |
| centered transport | `0.0619725685` |

The sharp certificate remains valid to radius `0.0114537860`, an overlap
factor `1.9016` above the required local radius.

## Probabilistic representation advance

Stage 19 proves that a state-weighted bad subkernel `Q` satisfying

```text
QV <= q_V V
```

gives exponential bad-chain and rooted connected-cluster bounds.  This can
hold even when the scalar conditional ceiling equals one.  The finite
two-state example `Q=[[0,q^2],[1,0]]`, `V=[1,1/q]` has weighted ceiling `q`.

Stage 20 supplies the exact finite interface needed by that theorem: relative
tree gauge identifies interior gauge orbits with nonforest links while
retaining a boundary-covariant connection.  Haar measure disintegrates exactly
into retained state and interior fiber.

## Corrected first unproved implication

On the certified local overlap window, construct the complete finite-volume
`SU(2)` conditional kernels and prove both:

1. a boundary-uniform normalized good-channel comparison with logarithmic
   loss at most `0.2` per connected support unit; and
2. a positive state weight charging center, continuous, cut-locus/orbit, and
   topological complement channels such that the combined weighted bad
   ceiling is below

```text
q_crit = 0.0027927080803578997.
```

Equivalently, after chart, determinant, and transition entropy, the weighted
free-energy cost per extension must exceed `5.8807435158`.

## Remaining chain

```text
normalized boundary-state good-channel comparison [OPEN]
  + weighted multi-link complement charge [OPEN]
  -> volume-uniform one-scale SU(2) K+R basin inequality [OPEN]
  -> gauge-covariant RG stability and repeated propagation [OPEN]
  -> finite-physical-scale basin entry [OPEN]
  -> continuum OS coherence and theory identity [OPEN]
  -> Hamiltonian mass gap [OPEN].
```

## Epistemic status

Stages 19--22 are `C2` abstract or finite regulated theorems, with Stage 21's
large matrix constants classed as executable `C1` spectral calibrations.  They
do not establish normalized full-measure nonlinear comparison, repeated RG,
continuum Yang--Mills, or the Clay mass gap.
