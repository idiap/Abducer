# Proof-status ledger

Statuses: **P** proved here, **I** imported with a primary citation, **C**
conditional theorem proved from stated hypotheses, **R** restricted or finite
result, **O** open, **F** falsified as a general implication.

| ID | Claim | Status | Dependency / blocker |
|---|---|---:|---|
| T0 | Exact Clay target and claim hierarchy are frozen | P | Definitions in the dossier |
| T1 | The chosen gauge-invariant observable core separates all physical states | O | Requires a continuum construction and density theorem |
| T2 | Representation morphisms compose with additive error and intersected certificates | P | Proposition on typed morphisms; executable finite check |
| T3 | Uniform physical temporal rigidity on a dense OS core excludes spectrum in `(0,m)` | P | Positive spectral theorem |
| T4 | Regulated rigidity passes to the continuum under fixed-time quadratic-form convergence and vanishing errors | C | Requires convergence, positivity, and density |
| T5 | A weighted Dobrushin influence bound implies exponential block covariance decay | C | Uses the stated comparison inequality; Neumann-series proof is included |
| T6 | Entry into the proposed basin at physical scale `ell_*` gives rate at least `kappa/ell_*` | C | T5 plus observable transport and uniform RG errors |
| T7 | Strong-coupling lattice estimates imply the Clay mass gap | F | Cutoff/physical scaling and continuum construction are absent |
| T8 | A sampling-dynamics Poincare gap is the physical Hamiltonian gap | F | Time rescaling changes the former without changing the Euclidean theory |
| T9 | Small-field four-dimensional RG control extends uniformly to the full measure and topology | O | Exceptional polymers, orbit atlas, global sectors, scale summability |
| T10 | Four-dimensional pure Yang--Mills reaches the rigidity basin at finite physical scale | O | Central basin-entry inequality `BE(k_*,kappa,q)` |
| T11 | Continuum Schwinger functions exist, are nontrivial pure Yang--Mills, satisfy OS axioms, and are regulator independent | O | Tightness, uniqueness, theory identity, positivity, universality |
| T12 | The complete Clay theorem follows from T1, T4, T10, and T11 | C | Logical composition only; key hypotheses are open |
| T13 | Finite spectral core recognizes gapped, gapless, and hidden-sector examples | R | Verified by the unit tests |

## First unresolved implication

The first deliberately isolated frontier implication is

```text
asymptotically-free regulated 4D pure Yang--Mills trajectory
    => full-measure, volume- and cutoff-uniform basin entry BE(k_*, kappa, q).
```

Writing `gamma_B^(k)` for block conditional kernels on gauge-orbit data and
`c_BC^(k)` for their influence coefficients, the missing estimate is a finite
physical-scale bound of the form

```text
sup_B sum_C exp(kappa d(B,C)) c_BC^(k_*) <= q < 1,
```

together with summable RG reconstruction errors, uniformity in volume and
cutoff, and control of exceptional fields and topological sectors.  The
inequality may be replaced by an equally explicit polymer or transfer
contraction criterion, but it may not assume the desired mass gap or
all-distance exponential clustering.

## Strongest claim level reached

**C3: conditional continuum/transfer theorem.**  The dossier contains genuine
mathematical progress at the level of definitions, obstruction separation,
finite proofs, and conditional bridges.  It does not reach C5 or C6 because T1,
T10, and T11 are open.
