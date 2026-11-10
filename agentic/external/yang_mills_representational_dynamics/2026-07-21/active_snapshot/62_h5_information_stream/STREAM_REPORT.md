# H5 information-theoretic stream report

## Hypothesis and scope

H5 proposes that **free-energy rigidity is more fundamental than action rigidity**. The useful object is not a pointwise action cost by itself, but the information cost of forcing the normalized nonlinear Yang--Mills measure into a declared bad event. This is an independent stream: it can be developed without assuming that the vacuum-weight, topology, or spectral-gap programs have closed. Its finite mathematical core is exact; its physical, boundary-uniform implication is open.

Fix a finite lattice region `Lambda`, boundary data `eta`, and a positive-mass retained history `h`. Write the actual conditional nonlinear measure as

`mu(dU) = Z^(-1) exp(-S(U)) rho(dU)`

and let `B` be a measurable bad event (for example, a specified defect or failed good-channel condition). All normalizers, constraints, gauge reductions, and history dependence are part of `mu`; omitting any of them changes the question.

## Exact event-KL theorem

For every probability measure `nu` supported on `B` and absolutely continuous with respect to `mu`, the relative-entropy chain rule gives

`D(nu || mu) = D(nu || mu(.|B)) - log mu(B)`.

Consequently,

`inf { D(nu || mu) : nu(B)=1 } = -log mu(B)`,

with unique minimizer `nu = mu(.|B)` up to null sets. Thus bad-event suppression and the least information required to force the bad event are exactly the same quantity. This is an identity, not an asymptotic approximation and not a claim about a continuum theory.

The indicator map `T(U)=1_B(U)` also gives the data-processing inequality

`D(nu || mu) >= d(nu(B) || mu(B))`,

where `d` is binary relative entropy. More generally, every coarse retained map `T` obeys `D(nu || mu) >= D(T#nu || T#mu)`. The recorded finite probe verifies these statements numerically: for `mu(B)=0.8`, the conditional divergence is `0.22314355131420976`, agreeing with `-log(0.8)=0.2231435513142097` to error `5.55e-17`; a tested coarse graining reduces relative entropy from `0.10644013528622318` to `0.08228287850505184`.

These facts identify the correct scalar target, but do not provide a lower bound on it for the physical measure.

## Why action-only bounds fail

There are two distinct obstructions.

**Multiplicity.** Suppose there is one good state of weight `1` and 1,000 bad states, each with action penalty `5` and hence weight `exp(-5)`. Then

`mu(B) = 1000 exp(-5) / (1 + 1000 exp(-5)) = 0.8707667550426246`.

Every bad microstate is individually expensive, yet the bad macro-event is overwhelmingly likely because its entropy `log(1000)` exceeds the energetic penalty. The probe therefore falsifies the inference “charge/action 5 implies rare event” unless multiplicity is included.

**Normalizer.** Pointwise improvement of the bad action still need not improve its probability. On `{g,b}`, start with `S_0(g)=S_0(b)=0`, so `mu_0(b)=1/2`. Set `S_1(b)=1` but `S_1(g)=10`. The bad state has acquired a positive action penalty, while

`mu_1(b) = exp(-1)/(exp(-1)+exp(-10)) > 0.9998`.

The probability rises because the good-sector partition function collapses more strongly. Equivalently, an unnormalized numerator estimate has no probabilistic content without a compatible lower bound on the total or good-sector normalizer. Additive action constants make the same warning unavoidable. H5 must therefore be stated as a normalized free-energy or partition-ratio assertion.

## Exact target to prove

Define the restricted partition functions

`Z_B = integral_B exp(-S(U)) rho(dU)` and `Z_G = integral_(B^c) exp(-S(U)) rho(dU)`.

The exact identity is

`mu(B) = Z_B/(Z_B+Z_G)`,

so, for every `0 < epsilon < 1`,

`mu(B) <= epsilon` if and only if `Z_B/Z_G <= epsilon/(1-epsilon)`.

The primary H5 target is a boundary-, cutoff-, volume-, and positive-mass-history-uniform estimate for the actual nonlinear conditional measure: for every admissible separated defect family `J`,

`Z_bad(J; eta,h) / Z_good(J; eta,h) <= C_0 exp(-kappa |J|)`,

with `kappa>0` and controlled `C_0` independent of `Lambda`, `eta`, cutoff, and `h`. Here the two restricted sectors must be defined on one common constrained configuration space; `Z_good` cannot be replaced by a convenient Gaussian or unnormalized surrogate.

An information-theoretic route to the same endpoint is the following defect quasi-factorization. Choose local observation maps `T_j` and prove, for every `nu << mu`,

`D(nu || mu) >= c_QF sum_(j in J) D(T_j#nu || T_j#mu)`,

with `c_QF>0` uniform in the same parameters. If `nu=mu(.|B_J)` and the definition of `B_J` yields a uniform local witness lower bound `D(T_j#nu || T_j#mu) >= delta`, then the event-KL identity gives

`mu(B_J) <= exp(-c_QF delta |J|)`.

This implication is exact once its hypotheses are established. The difficult step is proving the quasi-factorization and local witness for the interacting, gauge-constrained, nonlinear measure, not manipulating the KL identity.

## First open implication and research program

The first open physical implication is: **prove either the uniform restricted partition-ratio estimate or the stated defect quasi-factorization for the actual finite-volume nonlinear Yang--Mills conditional measure, uniformly over admissible boundary data and positive-mass retained histories.** Only then may H5 supply a strict bad-channel numerator bound to a normalized retained-state kernel.

The shortest route is to define one concrete block event and its good comparator on the same fiber; compute exact finite restricted normalizers; isolate a local free-energy gap including orbit/Jacobian factors; and prove that interactions and shared constraints do not erase that gap when blocks are composed. A successful theorem must track constants explicitly and show that boundary influence is absorbed without degrading `kappa` to zero.

## Claim and Clay guardrails

At **C1**, H5 consists of the exact finite probability identities, the data-processing check, and the multiplicity and normalizer counterexamples. These are complete but toy/structural results. A **C2** claim requires a theorem for the declared finite lattice Yang--Mills measure with the real nonlinear action, constraints, retained histories, and uniform constants; a calculation on a surrogate measure does not qualify.

No H5 result currently proves a continuum limit, nontriviality, Osterwalder--Schrader reconstruction, exponential temporal clustering, or a positive physical mass gap. Even a C2 exponential defect bound is only an input to those bridges. A Clay-level claim would additionally require a rigorously constructed four-dimensional quantum Yang--Mills theory satisfying the required axioms and a volume- and cutoff-uniform spectral/mass-gap conclusion that survives continuum reconstruction. H5 must not be advertised as that conclusion, nor may data processing alone be used to infer it.
