---
name: ym-prove-state-weighted-defect-transfer
description: Construct, prove, falsify, and audit retained-boundary-state weighted defect-transfer kernels for nonlinear lattice Yang--Mills measures. Use when scalar worst-history conditioning is too strong, rare frustrated states must retain their energetic cost, or local typical-set estimates must be converted into connected-cluster suppression without assuming Bernoulli domination.
---

# Prove State-Weighted Yang--Mills Defect Transfer

## Target

For retained boundary states `sigma`, a positive weight `V>=1`, and a bad
extension subkernel `Q`, prove

```text
integral V(sigma') Q(sigma,d sigma') <= q_V V(sigma)
```

with `exp(alpha) Delta^2 q_V < 1` and a uniform root-state `V` moment. Then
derive connected-chain and rooted-cluster decay by positive-kernel iteration.

## Workflow

1. Freeze the finite regulator, volume, block graph, boundary state, fiber,
   bad predicate, exploration order, and all heat-time/cutoff parameters.
2. Prove the retained state is conditionally sufficient. Use relative tree
   gauge or another exact quotient; preserve boundary gauge covariance,
   reflection compatibility, center, cut-locus, orbit, and topology data.
3. Prove `QV<=q_V V => Q^nV<=q_V^nV` and include the initial `V` moment.
4. Optimize finite multitype weights by Perron--Frobenius analysis. A large
   scalar conditional is allowed only when the weight proves its entry cost.
5. Use local link, plaquette-input, or curvature norms for the good region.
6. Prove normalized good-channel comparison with partition functions,
   Haar/Jacobian factors, chart overlap, and boundary dependence.
7. Prove multi-link weighted energy charging for center, continuous,
   cut-locus/orbit, and topological complement channels.
8. Combine kernels, verify the strict threshold, test hostile histories, and
   finish with a theorem graph and frontier ledger.

## Mandatory falsifications

- Test `Q=[[0,q^2],[1,0]]` with weight `[1,1/q]`.
- Retain the anticorrelated two-site moment counterexample.
- Test negative-center boundaries and continuous incoherent collars.
- Compare local concentration with every global-ball certificate.
- Reject nonpositive weights, invalid kernels, critical thresholds, hidden
  volume factors, and weights defined using the desired gap.

## Evidence contract

Return the typed state/fiber disintegration, weight and bad subkernel, good and
complement inequalities, root moment, weighted ceiling, cluster sum,
counterexamples, ledgers, and first open implication. Never promote a finite
overlap window to RG, continuum, OS, or Hamiltonian-gap control.

