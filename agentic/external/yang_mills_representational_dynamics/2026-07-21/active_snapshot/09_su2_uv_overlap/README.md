# Stage 09: `SU(2)` Ultraviolet Overlap Benchmark

This stage asks the first decisive question exposed by Stage 08: can the
nonlinear local-action inequalities and a small exceptional-field activity be
true at the same ultraviolet scale?

The answer is **yes in a rigorously delimited surrogate benchmark**.  At
`t=3e-6`, link-chart radius `r=0.0041`, curvature radius `rho=0.0082`, and
fiber radius `r_F=1e-5`, the Haar-augmented local action remains coercive and a
standalone one-plaquette heat-kernel tail is small enough to pass a weighted
independent-block polymer sum after a 216-plaquette union bound.

This is not full-measure Yang--Mills control.  In the four-dimensional link
measure, plaquettes share links, obey Bianchi constraints, carry boundary and
topological data, and are not independent.  The standalone heat-kernel law is
not established here as their marginal.  The stage therefore removes a scale
incompatibility objection but leaves the actual dependent activity theorem as
the first unproved implication.

## Files

- `su2_uv_overlap_theorem.{tex,pdf}`: theorem, proof, calibration, and audit.
- `su2_uv_overlap.py`: analytic certificates and declared grid search.
- `test_su2_uv_overlap.py`: positive, boundary, cross-representation, and
  fail-closed tests.
- `su2_uv_overlap_calibration.json`: complete witness and search output.
- `theorem_dependencies_uv_overlap.json`: machine-readable claims and edges.
- `su2_uv_overlap_frontier_ledger.md`: claim/limit audit.
- `topology_and_dependence_ledger.md`: missing full-measure sectors.
- `research_plan_todos.md`: the frozen and completed implementation plan.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_su2_uv_overlap.py
python3 su2_uv_overlap.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error su2_uv_overlap_theorem.tex
```

## Claim status

`C2` restricted finite certificate.  No dependent polymer, repeated RG,
continuum construction, or Hamiltonian mass gap is claimed.

