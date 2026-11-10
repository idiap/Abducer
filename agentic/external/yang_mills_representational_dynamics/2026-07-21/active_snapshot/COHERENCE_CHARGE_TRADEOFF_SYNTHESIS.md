# Coherence--Charge Trade-off Frontier: Synthesis

## Strategic outcome

The Stage 26 free-energy target has been turned into a common-parameter test.
The coherent and incoherent continuous channels demand opposite behavior from
the collar radius `eta`:

- smaller `eta` improves the coherent-staple conditional numerator;
- larger `eta` strengthens the deterministic energy charge of collar failure.

The new run proves exact or certified statements on both sides and tests them
inside the same nonlinear radius window.

## Stage 27 -- exact Haar entropy

For normalized Haar measure on `SU(2)=S^3`,

```text
v(r) = (r-sin(r)cos(r))/pi
     = (2/pi) integral_0^r sin(u)^2 du.
```

For `0 <= r <= 1`,

```text
2r^3(1-r^2/5)/(3pi) <= v(r) <= 2r^3/(3pi).
```

At the former Stage 25 radius `0.00614955590043`, the exact Haar entropy is
`16.8243287906`. This explains why a tiny one-link denominator ball cannot be
treated as costless: the action gap must pay a cubic geometric entropy.

## Stage 28 -- conditional coherent channel

The finite-time logarithmic bound has a unique denominator optimizer solving

```text
v'(delta)/v(delta) = m(eta+delta)/t.
```

At `t=3e-6`, `m=6`, and `eta=0.001`, the optimizer is
`delta=0.000822875604347`. The former equal-split radius gives a trivial bound,
but re-optimizing the local `K+R` radius yields

```text
local radius                 0.00695051447204
curvature-chain radius       0.0139010289441
corrected reference ceiling  3.12507678090e-6
coherent ceiling             0.00241703202889
combined ceiling             0.00242015710567
target ceiling               0.00243027750184.
```

Thus the coherent continuous channel closes strictly, conditional on collar
coherence, inside the certified maximum radius `0.01145378595997`.

## Stage 29 -- overlap-correct incoherent channel

For `k` collar-failure witnesses whose plaquette supports overlap at most
`nu`, the global Gibbs exponent is at least

```text
k eta^2/(4 nu t).
```

The connected-witness branching ratio is

```text
theta = exp(alpha) D^2 exp(-eta^2/(4 nu t)).
```

The factor `nu` is necessary: repeating one identical witness `k` times
falsifies naive additive charging by a factor `k`.

At the largest nonlinear radius and ideal overlap `nu=1`:

```text
maximum eta accepted by coherent bound       0.00717145149149
minimum eta for entropy convergence           0.00840053106592
minimum eta for required free energy           0.00893686329306
common feasible interval width                -0.00176541180158.
```

Hence the present two-channel mechanism has no common `eta`, even before any
overlap loss. This is a no-go for the current certificates, not for Yang--Mills
theory.

## Stage 30 -- exact repair frontier

At the coherent eta ceiling, a size-at-least-two connected witness polymer can
meet `F_*>6.71292101139` along the following charge/entropy curve:

| charge amplification | maximum effective degree |
|---:|---:|
| 1.0 | 2.20542417159 |
| 1.2 | 4.95435778073 |
| 1.4 | 10.5919707256 |
| 1.55294508627 | 18.0 |

This is the best next target: construct a gauge-covariant canonical witness
polymer whose exact overlap and counting constants land on this curve, and
then compare its weighted numerator to the same retained-state good partition.

## Channel audit

- Center: exact restricted contour; continuous-measure activity transfer open.
- Continuous coherent: strict conditional budget; collar occurrence open.
- Continuous incoherent: exact charge theorem; current parameter regions
  disjoint.
- Cut/orbit: atlas and disintegration available; weighted numerator open.
- Topology: not represented by the present open local block.

Physical channels closed uniformly in boundary state and volume: `0/5`.

## Main programme

```text
canonical sector-aware witness polymer [NEXT]
  -> normalized multichannel physical partition ratio [OPEN]
  -> volume-uniform one-scale nonlinear basin entry [OPEN]
  -> repeated gauge-covariant RG control [OPEN]
  -> continuum OS-coherent Yang--Mills theory [OPEN]
  -> Hamiltonian mass gap [OPEN].
```

The strongest status remains `C2`. No physical basin entry, continuum theory,
or Clay mass gap has been proved.
