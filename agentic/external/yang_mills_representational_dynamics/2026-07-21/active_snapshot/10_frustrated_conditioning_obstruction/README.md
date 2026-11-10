# Stage 10: Frustrated Conditioning Obstruction

Stage 09 found a strict overlap between local nonlinear control and an
independent ultraviolet defect benchmark.  Stage 10 tests the most direct
dependent extension: bounding a bad plaquette uniformly over every
microscopic conditioning of neighboring links.

That route fails for an exact structural reason.  On the side-two
four-dimensional block, center-valued surrounding links can give an interior
link five identity staples and one `-I` staple.  The conditional density is

```text
p_t(U)^5 p_t(-U) dU.
```

Its weak-coupling rate is minimized at class angle `pi/6`, leaving the
frustrated plaquette at angle `5pi/6`.  Consequently, for every chart radius
below `5pi/6`, that plaquette is conditionally bad with probability tending to
one as the heat time tends to zero.

The theorem rules out a worst-case single-link Dobrushin proof based on rare
small-curvature failures.  It does not rule out the viable replacements:
charge the frustrating boundary to a contour, condition on a good collar,
integrate a multi-link block, or keep center/topological sectors as labeled
polymer species.

## Files

- `frustrated_conditioning_theorem.{tex,pdf}`: theorem, proof, and audit.
- `frustrated_conditioning.py`: exact incidence, GF(2), rate, and numerical
  certificates.
- `test_frustrated_conditioning.py`: 17 positive and failing tests.
- `frustrated_conditioning_calibration.json`: complete executable output.
- `theorem_dependencies_frustrated.json`: claim graph.
- `replacement_strategy_ledger.md`: viable dependent-polymer replacements.
- `frustrated_conditioning_frontier_ledger.md`: claim and limit audit.
- `research_plan_todos.md`: completed implementation plan.

## Reproduce

```bash
python3 -m unittest -v test_frustrated_conditioning.py
python3 frustrated_conditioning.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error frustrated_conditioning_theorem.tex
```

Claim level: `C2`, restricted obstruction theorem.  This stage does not prove
a dependent polymer expansion, repeated RG control, continuum Yang--Mills, or
a mass gap.
