# Stage 54 -- normalized retained-kernel interface

This stage implements the first target after H1: the exact finite conditional
partition object whose nonlinear `SU(2)` realization remains open.

The theorem note is `normalized_retained_kernel_theorem.pdf`.

Run:

```bash
python3 normalized_retained_kernel.py --write normalized_retained_kernel_results.json
python3 -m unittest -v test_normalized_retained_kernel.py
```

The finite theorem is C2. It does not construct the physical Yang--Mills row.
