# Stage 69: H2 state-dependent tempered equivalence

This directory completes the first open finite-mathematics target in the H2
physical-length stream.

## Main result

For sharp equivalence constants (a_nV_n\leq W_n\leq b_nV_n), the
algebraically defined least weighted ceilings satisfy

\[
q_n^V\frac{a_{n+1}}{b_n}
\leq q_n^W\leq
q_n^V\frac{b_{n+1}}{a_n}.
\]

The product distortion decomposes into an endpoint scalar coboundary plus an
accumulated state-dependent projective width. Both must be sublinear in
physical length for a robust representation-independent exponent. Scalar
rescaling is recovered as the exact zero-width telescoping case.

The stage also implements the Duhamel formula for additive defects and four
countermodels showing why non-tempered charts, merely summable errors, and
uncontrolled support growth can each erase the physical meaning of a raw
cocycle exponent.

## Files

- `tempered_equivalence.py` -- theorem certificates and countermodels.
- `test_tempered_equivalence.py` -- 25 hostile unit tests.
- `tempered_equivalence_results.json` -- canonical numerical output.
- `theorem_dependencies_h2_tempered.json` -- dependency and claim graph.
- `RESULT_LEDGER.md` -- theorem, proof, additive extension, and frontier.
- `NEXT_STEP_TODOS.md` -- completed finite phase and open physical gates.

## Reproduce

From this directory:

```bash
python3 -m unittest -v test_tempered_equivalence.py
python3 tempered_equivalence.py --write tempered_equivalence_results.json
python3 -m json.tool tempered_equivalence_results.json >/dev/null
python3 -m json.tool theorem_dependencies_h2_tempered.json >/dev/null
```

## Claim boundary

This is a C2 finite positive-kernel theorem with floating-point executable
certificates. The theorem is exact mathematics; numerical residuals are
tolerance-certified. The canonical results explicitly
set the physical Yang--Mills kernel, uniform chart atlas, observable pullback,
OS reconstruction, and continuum mass gap to `false`.
