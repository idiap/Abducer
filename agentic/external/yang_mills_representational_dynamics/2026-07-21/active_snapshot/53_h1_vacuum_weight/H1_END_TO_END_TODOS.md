# H1 completed end-to-end TODOs

Completion here means closure of the finite/conditional H1 mechanism. It does
not mean closure of the Yang--Mills premise listed separately in
`H1_YM_HANDOFF_TODOS.md`.

## H1.1 -- freeze conventions

- [x] Separate temporal transfer, RG, and exploration kernels.
- [x] Type right vacuum amplitude, left vacuum amplitude, state dynamics, and
  forward Lyapunov weight.
- [x] Determine the correct forward-state orientation `V=1/psi`.
- [x] Prohibit automatic identification of an RG Perron vector with the
  physical vacuum.

## H1.2 -- positive transfer theorem

- [x] Define a finite irreducible nonnegative transfer amplitude.
- [x] Construct its principal left and right eigenvectors.
- [x] Prove the Doob kernel is stochastic.
- [x] Derive its stationary distribution.
- [x] Prove reversibility for symmetric transfer amplitudes.
- [x] Reject a transfer with a zero vacuum component.

## H1.3 -- inverse-amplitude theorem

- [x] Define a bad-edge mask and bad subkernel.
- [x] Prove exact inverse-amplitude cancellation.
- [x] Normalize the cost weight to `V>=1`.
- [x] Demonstrate that using `psi` instead of `1/psi` does not satisfy the same
  identity.
- [x] Interpret `-log psi` as retained boundary-state cost.

## H1.4 -- Perron optimality

- [x] State the Collatz--Wielandt positive-weight variational formula.
- [x] Compute the positive Perron vector of a finite bad subkernel.
- [x] Verify that arbitrary positive weights cannot beat the spectral radius.
- [x] Reject superprobability bad rows.
- [x] Distinguish the optimal defect weight from a vacuum-derived weight.

## H1.5 -- multichannel application

- [x] Reconstruct the four-channel star kernel.
- [x] Prove algebraically that `V=(1,1/q,...,1/q)` is an eigenweight.
- [x] Prove the eigenvalue and optimum equal `q`.
- [x] Verify scalar ceiling one and weighted ceiling `q`.
- [x] Cross-check parameters with Stages 19, 24, and 25.

## H1.6 -- iteration and cluster conversion

- [x] Prove positive-kernel chain iteration.
- [x] Include the initial root-state moment.
- [x] Enumerate exact bad-chain masses through length twelve.
- [x] Reproduce the degree-18 cluster branching constant.
- [x] Verify strict subcriticality.
- [x] Reject equality at the critical threshold.

## H1.7 -- hostile uniformity tests

- [x] Construct a positive finite-volume vacuum with exponentially growing
  inverse cost weight.
- [x] Show finite Perron positivity does not imply a uniform Harnack bound.
- [x] Expose the missing root-moment estimate.
- [x] Preserve all RG, continuum, and gap guardrails.

## H1.8 -- packaging and verification

- [x] Store canonical machine-readable results.
- [x] Run fifteen dependency-free regression tests.
- [x] Write the modular LaTeX theorem note.
- [x] Compile, render, and visually inspect the PDF.
- [x] Emit the theorem graph, frontier ledger, and physical handoff.
