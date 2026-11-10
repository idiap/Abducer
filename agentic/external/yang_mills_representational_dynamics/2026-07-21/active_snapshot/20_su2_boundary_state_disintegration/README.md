# Stage 20: `SU(2)` Boundary-State Disintegration

This stage gives an exact finite-graph representation theorem.  Relative tree
gauge quotients interior gauge transformations while leaving a covariant
boundary connection.  The normalized nonforest links split into retained
boundary state and conditional interior fiber, and product Haar measure
factorizes in these coordinates up to the constant gauge volume.

The executable block is a reflection-symmetric `2x2` plaquette square with one
interior vertex.  The graph theorem is general, but the completed calibration
is not yet the full four-dimensional RG block.

```bash
python3 -m unittest -v test_su2_boundary_state_disintegration.py
python3 su2_boundary_state_disintegration.py --output json
```

