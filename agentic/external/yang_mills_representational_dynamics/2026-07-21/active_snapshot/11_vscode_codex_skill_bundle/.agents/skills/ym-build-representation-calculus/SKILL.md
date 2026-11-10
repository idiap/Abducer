---
name: ym-build-representation-calculus
description: Build and audit typed, phenomenon-preserving representation packages and morphisms for Yang--Mills and constructive QFT. Use when relating lattice, Euclidean, Hamiltonian, observable-algebraic, renormalization-group, probabilistic, or dual descriptions and when exact equivalence must be separated from approximation, coarse-graining, or conjectural correspondence.
---

# Build a Representation Calculus

## Representation package

Use
`R = (K, A_phys, S, D, G, L, Q)`
for carrier, physical observables, states, dynamics/correlations, symmetries and redundancies, scale/limit structure, and quantitative controls. Type every component and parameter.

## Workflow

1. Define source and target packages independently of their presentation variables.
2. Define observable pullback and state pushforward; state their compatibility equation.
3. Label the map as exact equivalence, quotient, embedding, regularization, coarse-graining, asymptotic equivalence, reconstruction, continuum limit, duality, or heuristic correspondence.
4. For approximate maps, give observable-indexed errors with cutoff, volume, scale, and support dependence.
5. Attach certificates for positivity, locality, symmetry, theory identity, nontriviality, scaling, and spectral information.
6. Prove identities, composition, and accumulated-error bounds.
7. Test hostile examples: small observable classes, nonuniform limits, lost positivity, hidden sectors, and noncommuting limits.
8. Emit a commutative-diagram obligation ledger and the strongest proved relation.

## Guardrails

- Never call numerical agreement or shared perturbation series an equivalence.
- Do not treat an irreversible coarse-graining map as invertible.
- Require recovery theorems for temporarily lost locality or covariance.
- Keep physical time evolution distinct from gauge change, RG flow, and reconstruction.
- Drop categorical language that does not sharpen a theorem or error bound.

## Output contract

Return formal packages, typed morphisms, composition laws, certificate table, countermodels, exact uniformity domain, and unresolved analytic obligations.
