# Stage 14: Nonlinear Two-Tier Activity Transfer

This stage proves an abstract connected-event bridge required after Stages 11--13.  If a
connected nonlinear bad event has a good-collar comparison cost `kappa` per
plaquette and its incoherent-collar channel has charged rate `K`, then its
effective weight is

```text
q_eff = exp(kappa-J) + exp(-K),
```

where `J` is the dependent Gaussian rate.  The degree-18 rooted activity sum
converges when

```text
exp(alpha) 18^2 q_eff < 1.
```

At the frozen witness, the declared target `kappa=0.2`, `K=7.0` is
subcritical.  The theorem does not establish those two estimates for the full
nonlinear `SU(2)` measure or identify Mayer/Ursell activities; it makes the
estimates and the subsequent activity/domination conversion explicit proof obligations.

## Reproduce

```bash
python3 -m unittest -v test_nonlinear_activity_transfer.py
python3 nonlinear_activity_transfer.py --output json
latexmk -pdf -interaction=nonstopmode -halt-on-error nonlinear_activity_transfer_theorem.tex
```

Claim level: `C2` abstract transfer theorem with a conditional `SU(2)` gate.
