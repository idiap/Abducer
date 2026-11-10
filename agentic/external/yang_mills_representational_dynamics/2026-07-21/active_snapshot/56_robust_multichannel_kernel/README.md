# Stage 56 -- robust multichannel kernel

This stage replaces a single calibrated matrix by a rigorous Perron envelope
for uncertain channel rows and computes the exact remaining slack.

The theorem note is `robust_multichannel_kernel_theorem.pdf`.

```bash
python3 robust_multichannel_kernel.py --write robust_multichannel_kernel_results.json
python3 -m unittest -v test_robust_multichannel_kernel.py
```
