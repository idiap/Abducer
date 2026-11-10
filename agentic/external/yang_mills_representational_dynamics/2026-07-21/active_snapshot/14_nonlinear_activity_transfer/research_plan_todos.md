# Stage 14 Plan and Completed Todos

## Target

Convert the dependent Gaussian theorem and good-collar/charged-contour split
into one exact nonlinear connected-event criterion, then quantify the remaining
`SU(2)` analytic estimates.

## Completed todos

- [x] Split a connected bad event by the coherent-collar event.
- [x] Encode good-channel nonlinear comparison as `exp(kappa |X|)`.
- [x] Encode collar failure as a charged rate `exp(-K |X|)`.
- [x] Prove `q_eff=exp(kappa-J)+exp(-K)`.
- [x] Combine with the degree-18 connected-set count.
- [x] Derive the exact critical effective weight.
- [x] Compute the maximum comparison loss when collar failure is absent.
- [x] Compute the minimum collar rate at a declared comparison loss.
- [x] Calibrate `kappa=0.2`, `K=7.0` at the ultraviolet witness.
- [x] Prove finite-registry composition of scale-indexed rooted errors.
- [x] Fail a registry when any one scale is supercritical.
- [x] Keep actual nonlinear hypotheses, infinite-scale uniformity, and basin
  entry explicitly false.

## Decision

The analytic frontier is now a numerical target rather than an unspecified
"dependent polymer estimate": at the frozen witness it is sufficient to prove
a good-collar comparison loss `kappa<=0.2` and a charged collar-failure rate
`K>=7.0`, with the exact event definitions and uniformity obligations stated in
the frontier ledger.
