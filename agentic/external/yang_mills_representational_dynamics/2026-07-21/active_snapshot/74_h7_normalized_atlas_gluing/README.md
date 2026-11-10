# Stage 74: H7 normalized atlas gluing

This stage proves an exact **C2 finite atlas theorem** for the next H7 step.
It replaces the sampled coverage probe by an exact normalized measure model on
a two-center `+I`/`-I` cover, while preserving the distinction between atlas
coverage and probability control.

## The finite theorem

The six-atom carrier has two radius-`pi/2` chart supports.  Their two equator
atoms form an overlap and every carrier point is covered with multiplicity at
most two.  Subordinate weights `w_+` and `w_-` obey

```text
w_+(x) + w_-(x) = 1.
```

For every positive finite history `mu`, define

```text
p_s = sum_x mu(x) w_s(x),
mu_s(x) = mu(x) w_s(x) / p_s.
```

The implementation proves, for every one of the 64 carrier events,

```text
mu(A) = p_+ mu_+(A) + p_- mu_-(A).
```

On each overlap atom, the coordinate density transition contains all three
required factors:

```text
C_{s,t} = (w_t / w_s) (p_s / p_t) / J_{s,t},
f_t = C_{s,t} f_s,
C_{s,t} C_{t,s} = 1.
```

Nontrivial rational Jacobians are used, so a missing or inverted Jacobian is
detected.  The exceptional atom is still covered by both charts; isolating it
produces a third normalized channel whose coefficient is its actual
conditional probability.

## Falsification results

For the hostile history indexed by `n`,

```text
p_+ = 3/(4n),
N_+({plus_pole}) = 1/(4n),
mu_+({plus_pole}) = 1/3.
```

Thus an arbitrarily small unnormalized numerator gives no small normalized
chart probability.  A separate history family has atlas coverage exactly one
while exceptional probability is `1 - 1/n`.  Coverage is geometric; it is not
a probabilistic tail estimate.

## Two-block check

Two adjacent blocks use opposite charts on a shared retained equator edge.
Opposite signed half-turn coordinates, combined with their `+I` and `-I`
centers, reconstruct the identical quaternion. A same-sign minus-chart
perturbation fails. The forward/reverse
density cocycle and the four-step product-word square equal one exactly for
both overlap atoms.  This is a finite shared-edge consistency theorem, not the
full boundary-rooted lattice forest theorem.

## Run

```bash
python3 -m unittest -v test_h7_normalized_atlas_gluing.py
python3 h7_normalized_atlas_gluing.py
```

## Artifacts

- `h7_normalized_atlas_gluing.py`: exact-rational theorem implementation.
- `test_h7_normalized_atlas_gluing.py`: 16 unit tests, including exhaustive
  event gluing and hostile histories.
- `h7_normalized_atlas_gluing_results.json`: canonical calibration.
- `theorem_dependencies_h7_stage74.json`: dependency and claim graph.
- `RESULT_LEDGER.md`: proved statements and nonclaims.
- `NEXT_STEP_TODOS.md`: completed finite step and physical handoff.
- `validation_report.json`: machine-readable verification summary.

## Frontier

The physical target **H7-PT1 remains open**.  This stage does not construct the
normalized nonlinear `SU(2)` conditional law for all positive-mass boundary
histories, bound its exceptional channel uniformly in volume and cutoff, glue
the full boundary-rooted forest, iterate an RG map, construct a continuum
theory, or prove a mass gap.
