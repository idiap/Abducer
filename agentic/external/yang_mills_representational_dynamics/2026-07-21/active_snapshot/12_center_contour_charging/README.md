# Stage 12: Exact Center-Contour Charging

This stage reconstructs the full center-valued curvature behind the Stage 10
conditioning.  Cubical Bianchi exactness and an exhaustive syndrome
certificate prove that the one-negative/five-positive incident staple pattern
requires at least five negative plaquettes in the full configuration.  The
matching Stage 10 link assignment attains five.

The center subsector becomes an exact polymer gas with relative weight
`q^{|X|}` for a connected center contour.  Connectivity uses common
three-cells so that no Bianchi parity equation is split between components.
A volume-uniform rooted sum follows from the computed degree and the fact that every nonempty
exact center contour has at least three plaquettes.

This is a center-sector theorem, not control of the continuous `SU(2)` measure.

## Reproduce

```bash
python3 -m unittest -v test_center_contour_charging.py
python3 center_contour_charging.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error center_contour_charging_theorem.tex
```

Claim level: `C2`, exact dependent center-sector theorem.
