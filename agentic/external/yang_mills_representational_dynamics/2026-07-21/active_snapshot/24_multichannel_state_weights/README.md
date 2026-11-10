# Stage 24: Multichannel Retained-State Weights

This stage solves exactly a star-shaped bad-subkernel model with regular,
center, continuous, cut/orbit, and topology states.  For entry rates `a_i`,
forced returns `b_i`, persistence `c_i`, and target `q`, the canonical weight
is

```text
V_i = b_i/(q-c_i),
```

and feasibility is exactly `sum_i a_i V_i <= q`, with every `c_i<q`.
The current local block does not yet carry a genuine topology label, and the
physical entry rates have not been bounded.

```bash
python3 -m unittest -v test_multichannel_state_weights.py
python3 multichannel_state_weights.py --output json
```
