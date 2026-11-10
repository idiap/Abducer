# Dispersion-Witness Ten-Phase Synthesis

Date: 21 July 2026  
Stages: 31--40  
Claim level: C2 exact/conditional finite theorems and restricted Gaussian closure

## Outcome

The run replaces the Stage 30 charge--entropy deficit by a sharper split based
on the exact Fréchet dispersion of the six staples incident on a link.  It
produces a nonempty common parameter interval in the full dependent Gaussian
block, but it does not prove the corresponding nonlinear, retained-state
uniform Yang--Mills estimate.

The strongest exact correction is

\[
  E_U=\sum_i d(I,US_i)^2=\Phi(U^{-1}),\qquad
  \Phi(C)=\sum_i d(C,S_i)^2.
\]

Consequently, failure of every radius-\(\eta\) common staple ball forces
\(E_U>\eta^2\) for every link value \(U\).  This doubles the deterministic
energy charge used at Stage 16, which had only obtained \(\eta^2/2\).

That correction is not by itself enough.  After the three-dimensional radial
entropy is restored, the single-plaquette action route is supercritical at the
coherent endpoint:

```text
coherent eta                            0.007171451491488068
bare action rate                        8.571619415794405
entropy-complete radial rate            4.4571320608142475
degree-20 entropy branching ratio       5.126035156032165
```

The successful restricted replacement is the full quadratic dispersion, not
the maximum of individual plaquette radii.  Its exact projected-Gaussian star
spectrum yields

```text
minimum RMS radius for required free energy    0.00386371990241687
maximum RMS radius accepted by low channel    0.007171451491488068
common interval width                          0.003307731589071198
midpoint rooted free energy lower bound       21.21918020230499
```

No plaquette independence is assumed in this calculation: the covariance is
the full projected curvature covariance and the tail follows from its exact
determinant moment.

## Ten implemented phases

| Stage | Result | Status |
|---:|---|---|
| 31 | Exact link-energy/Fréchet identity and corrected covering charge | exact finite theorem |
| 32 | Dispersion-aware low-channel optimizer and high-dispersion charge interface | conditional finite theorem |
| 33 | Canonical gauge-invariant plaquette witness with sharp incidence capacity four | exact finite theorem |
| 34 | Radial-entropy-complete activity audit | exact Gaussian theorem and falsification |
| 35 | Exact dependent-Gaussian staple-dispersion spectrum and tail | restricted Gaussian closure |
| 36 | Retained-state adaptive filtration and shared-uniform domination | exact implication; physical premise open |
| 37 | Weighted partition repair and congestion law | exact finite theorem; physical repair open |
| 38 | Five-channel sector-aware numerator allocation | exact bookkeeping theorem; channel bounds open |
| 39 | Periodic \(GF(2)\) cohomology and six center-flux carriers | exact finite topology carrier |
| 40 | Composite frontier and ranked nonlinear targets | conservative audit |

## Phenomena preserved

The run preserves the following structure explicitly rather than hiding it in
a scalar bad-event probability:

- gauge covariance through bi-invariant staple dispersion and gauge-invariant
  curvature witnesses;
- dependence through the exact projected Gaussian covariance;
- normalization through good/bad partition functions and repair congestion;
- adaptive history through a positive-mass retained-state filtration;
- defect ownership through five typed numerator channels;
- periodic center topology through six independent two-flux labels;
- entropy through radial integration, witness multiplicity, Jacobian loss, and
  repair-fiber congestion.

The retained state now has named fields for dispersion class, Fréchet-center
chart, center flux, boundary holonomy, orbit chart, and topology sector.

## First open physical inequality

For every finite volume, positive-mass retained history \(h\), and owned
channel \(c\), construct a gauge-covariant nonlinear comparison or repair
\(T_c\) such that

\[
  \sum_c\left(e^{\ell_c(h)}q_{\mathrm{low},c}(h)
  + C_{T_c}(h)\right)
  \le 0.002430277501841998,
\]

uniformly, with all multiplicity, Jacobian, state-weight, orbit-chart,
center-flux, and topology factors included.  Here \(C_{T_c}\) is the exact
weighted repair congestion from Stage 37.  Equal allocation among the five
channels would require free energy at least
\(7.62918774229502\) per channel before channel-specific losses.

## What the run does not prove

It does not establish:

1. a nonlinear retained-state-uniform transfer of the Gaussian determinant
   tail;
2. the physical adaptive history table;
3. a gauge-covariant nonlinear repair with bounded congestion;
4. integer second-Chern or instanton-sector control;
5. a volume-uniform one-scale basin, repeated renormalization, a continuum
   Yang--Mills measure, Osterwalder--Schrader reconstruction, or a Hamiltonian
   mass gap.

The finite Gaussian common interval is therefore evidence for a mechanism and
a sharply specified target, not a solution of the Clay problem.

## Ranked next targets

1. Construct a nonlinear dispersion repair on one periodic block and compute
   its exact energy drop, multiplicity, Jacobian, and state-weight congestion.
2. Prove a comparison from the projected Gaussian determinant tail to the
   nonlinear conditional measure uniformly over the complete retained state.
3. Populate the adaptive positive-mass history table from that comparison and
   invoke the already-proved domination theorem.
4. Extend the topology carrier beyond center two-flux to integer bundle data
   and prove uniform sector weights.
5. Only after these gates close, claim one-scale basin entry and begin an
   iterated gauge-covariant RG argument.

Machine-readable numerical constants are in
`dispersion_witness_parameter_registry.json`; the cross-stage proof graph is
in `dispersion_witness_dependencies.json`.
