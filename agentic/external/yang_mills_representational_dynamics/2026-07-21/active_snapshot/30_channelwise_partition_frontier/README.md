# Stage 30: Channelwise Partition Frontier

This stage assembles the center, coherent continuous, incoherent continuous,
cut/orbit, and topology channels into a conservative executable frontier. It
also computes the charge-versus-entropy remedy curve for the next witness
polymer.

Run:

```bash
python3 -m unittest -v test_channelwise_partition_frontier.py
python3 channelwise_partition_frontier.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error channelwise_partition_frontier_theorem.tex
```

No physical channel is yet closed uniformly in boundary state and volume. The
claim level is `C2`; no basin-entry, continuum, or mass-gap theorem is claimed.
