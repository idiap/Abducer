# cycle-0162

This cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment, so future cycles can test whether the bridge is real rather than repeating generic strategy language.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`
- `marathon.branch.01ac559ac937`
- `marathon.branch.756192d048cd`
- `marathon.branch.cd0e087298e5`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology

## Candidate Lemma

If cutoff Schwinger functions whose positivity cone is closed under the limiting topology satisfies the stated uniformity and same-theory conditions, then the branch may transport information to physical Hilbert space, vacuum vector, and positive Hamiltonian without weakening the target object.

## Definitions

- source object: cutoff Schwinger functions whose positivity cone is closed under the limiting topology
- target object: physical Hilbert space, vacuum vector, and positive Hamiltonian
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- reflection-positive limiting Schwinger function family checkpoint: `\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)\ge 0`. Valid when: The test functions f_i are gauge-invariant positive-time observables and S is the continuum limiting Schwinger family.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from cutoff Schwinger functions whose positivity cone is closed under the limiting topology rather than from an untyped desired conclusion.
- State the core equation `\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)\ge 0` and its validity conditions.
- Ask whether the equation controls the interface `regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: Reflection positivity is not closed under the chosen cutoff-removal topology.

## Falsifiers

- Reflection positivity is not closed under the chosen cutoff-removal topology.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions` into a concrete source object (cutoff Schwinger functions whose positivity cone is closed under the limiting topology) and target object (physical Hilbert space, vacuum vector, and positive Hamiltonian). The next proof pressure is not to add vocabulary; it is to certify whether reflection-positive limiting Schwinger function family can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\sum_{i,j}\overline c_i c_j S(\Theta f_i,f_j)\ge 0` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.

# Gauge-Invariant Nontriviality Witness Selection

## Candidate Lemma

If OS-positive Schwinger functions with a surviving observable family satisfies the stated uniformity and same-theory conditions, then the branch may transport information to Hamiltonian spectral measure with support bounded away from zero without weakening the target object.

## Definitions

- source object: OS-positive Schwinger functions with a surviving observable family
- target object: Hamiltonian spectral measure with support bounded away from zero
- controlled interface: continuum gauge-invariant Schwinger functions -> non-Gaussian same-theory witness
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- gauge-invariant Euclidean two-point function checkpoint: `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)`. Valid when: O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from OS-positive Schwinger functions with a surviving observable family rather than from an untyped desired conclusion.
- State the core equation `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` and its validity conditions.
- Ask whether the equation controls the interface `continuum gauge-invariant Schwinger functions -> non-Gaussian same-theory witness` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.

## Falsifiers

- The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `continuum gauge-invariant Schwinger functions -> non-Gaussian same-theory witness` into a concrete source object (OS-positive Schwinger functions with a surviving observable family) and target object (Hamiltonian spectral measure with support bounded away from zero). The next proof pressure is not to add vocabulary; it is to certify whether gauge-invariant Euclidean two-point function can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.

# Gauge-Invariant Observable Density In The Excitation Sector

## Candidate Lemma

If OS-positive Schwinger functions with a surviving observable family satisfies the stated uniformity and same-theory conditions, then the branch may transport information to Hamiltonian spectral measure with support bounded away from zero without weakening the target object.

## Definitions

- source object: OS-positive Schwinger functions with a surviving observable family
- target object: Hamiltonian spectral measure with support bounded away from zero
- controlled interface: gauge-invariant observable algebra -> P_perp H_YM spectral determination
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- gauge-invariant Euclidean two-point function checkpoint: `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)`. Valid when: O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from OS-positive Schwinger functions with a surviving observable family rather than from an untyped desired conclusion.
- State the core equation `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` and its validity conditions.
- Ask whether the equation controls the interface `gauge-invariant observable algebra -> P_perp H_YM spectral determination` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.

## Falsifiers

- The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `gauge-invariant observable algebra -> P_perp H_YM spectral determination` into a concrete source object (OS-positive Schwinger functions with a surviving observable family) and target object (Hamiltonian spectral measure with support bounded away from zero). The next proof pressure is not to add vocabulary; it is to certify whether gauge-invariant Euclidean two-point function can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.

# Laplace-Transform Support From Uniform Euclidean Decay

## Candidate Lemma

If OS-positive Schwinger functions with a surviving observable family satisfies the stated uniformity and same-theory conditions, then the branch may transport information to Hamiltonian spectral measure with support bounded away from zero without weakening the target object.

## Definitions

- source object: OS-positive Schwinger functions with a surviving observable family
- target object: Hamiltonian spectral measure with support bounded away from zero
- controlled interface: Euclidean time correlation decay -> Hamiltonian spectral support exclusion
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- gauge-invariant Euclidean two-point function checkpoint: `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)`. Valid when: O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from OS-positive Schwinger functions with a surviving observable family rather than from an untyped desired conclusion.
- State the core equation `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` and its validity conditions.
- Ask whether the equation controls the interface `Euclidean time correlation decay -> Hamiltonian spectral support exclusion` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.

## Falsifiers

- The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `Euclidean time correlation decay -> Hamiltonian spectral support exclusion` into a concrete source object (OS-positive Schwinger functions with a surviving observable family) and target object (Hamiltonian spectral measure with support bounded away from zero). The next proof pressure is not to add vocabulary; it is to certify whether gauge-invariant Euclidean two-point function can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.

# Cutoff-Uniform Mass Scale Nonvanishing

## Candidate Lemma

If OS-positive Schwinger functions with a surviving observable family satisfies the stated uniformity and same-theory conditions, then the branch may transport information to Hamiltonian spectral measure with support bounded away from zero without weakening the target object.

## Definitions

- source object: OS-positive Schwinger functions with a surviving observable family
- target object: Hamiltonian spectral measure with support bounded away from zero
- controlled interface: regulated decay scales m_{a,L} -> positive continuum lower bound m0
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- gauge-invariant Euclidean two-point function checkpoint: `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)`. Valid when: O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from OS-positive Schwinger functions with a surviving observable family rather than from an untyped desired conclusion.
- State the core equation `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` and its validity conditions.
- Ask whether the equation controls the interface `regulated decay scales m_{a,L} -> positive continuum lower bound m0` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.

## Falsifiers

- The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `regulated decay scales m_{a,L} -> positive continuum lower bound m0` into a concrete source object (OS-positive Schwinger functions with a surviving observable family) and target object (Hamiltonian spectral measure with support bounded away from zero). The next proof pressure is not to add vocabulary; it is to certify whether gauge-invariant Euclidean two-point function can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.

# No-Gap Reductio Low-Energy Carrier

## Candidate Lemma

If OS-positive Schwinger functions with a surviving observable family satisfies the stated uniformity and same-theory conditions, then the branch may transport information to Hamiltonian spectral measure with support bounded away from zero without weakening the target object.

## Definitions

- source object: OS-positive Schwinger functions with a surviving observable family
- target object: Hamiltonian spectral measure with support bounded away from zero
- controlled interface: negated Hamiltonian gap -> low-energy spectral or observable carrier
- same-theory condition: construction, observables, reconstruction, and witnesses must refer to one limiting object.

## Assumptions

- The target commitments remain existence, nontriviality, OS/Wightman adequacy, continuum limit, and positive mass gap unless an accepted weakening is recorded.
- All limiting operations are typed by their source cutoff family and target continuum object.
- Observable claims use gauge-invariant observables that survive into the reconstructed theory.

## Equations

- gauge-invariant Euclidean two-point function checkpoint: `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)`. Valid when: O belongs to the reconstructed gauge-invariant observable algebra and the OS semigroup identifies Euclidean time with e^{-tH}.
- same-theory transfer constraint: `(S_n,\mathcal H,H,\Omega,O)\ \text{arise from one limiting construction}`. Valid when: The construction packet names S_n, the reconstruction theorem names H and Omega, and O is in the reconstructed observable algebra.

## Attempted Derivation

- Start from OS-positive Schwinger functions with a surviving observable family rather than from an untyped desired conclusion.
- State the core equation `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` and its validity conditions.
- Ask whether the equation controls the interface `negated Hamiltonian gap -> low-energy spectral or observable carrier` without importing another theory.
- Route the missing premise through obligation gating before promotion.

Blocking gap: The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.

## Falsifiers

- The observable family fails to be spectrally determining or the decay constants vanish under cutoff removal.
- The branch can only state an analogy, simulation result, or fixed-regulator observation without a transfer certificate.
- The generated lemma drops an essential target commitment or changes the observable algebra.

## Learning

The branch sharpened the interface from `negated Hamiltonian gap -> low-energy spectral or observable carrier` into a concrete source object (OS-positive Schwinger functions with a surviving observable family) and target object (Hamiltonian spectral measure with support bounded away from zero). The next proof pressure is not to add vocabulary; it is to certify whether gauge-invariant Euclidean two-point function can carry the bridge without changing the theory.

## Next Experiment

Certify the weakest condition under which `\langle O(t)O(0)\rangle_c=\int_0^\infty e^{-t\lambda}\,d\mu_O(\lambda)` is valid for the branch source object, then ask the entailment-gap auditor whether it reaches the target object without hidden proxy shifts.
