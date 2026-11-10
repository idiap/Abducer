# cycle-0352

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.01ac559ac937`
- `marathon.branch.756192d048cd`

## Branch Outputs

# Finite OS spectral-support theorem with Wilson-density gate quarantine

## Candidate Lemma

Finite OS support-exclusion theorem: for one reconstructed OS Hilbert space, if the connected covariance of a vacuum-orthogonal gauge-invariant Wilson observable has a positive Laplace representation and obeys C_A(t) <= C_0 exp(-m t) for all large t, then the spectral measure of v_A has no support in [0,m).

## Definitions

- source object: same-theory OS-positive Euclidean Schwinger family S with a time-zero gauge-invariant Wilson observable A and connected covariance C_A(t).
- target object: reconstructed OS Hilbert-space vector v_A=P_perp A\Omega and its Hamiltonian spectral measure \mu_A(B)=\langle v_A,E_H(B)v_A\rangle.
- controlled interface: Laplace-transform decay of the physical carrier C_A(t) is converted into support exclusion for \mu_A only after OS positivity and vacuum subtraction.
- same-theory condition: S, A, the recovery map from the regulator, \Omega, H, and \mu_A arise from one continuum theory, not from mixed approximants.
- physical carrier: the gauge-invariant Wilson covariance viewed as an OS Hilbert spectral measure witness.

## Assumptions

- Model: four-dimensional Euclidean Yang-Mills candidate after OS reconstruction on the gauge-invariant observable algebra.
- Regime: the lemma is Hilbert-spectral and finite; it does not construct the continuum Yang-Mills measure.
- Uniformity: for continuum use, m and C_0 must be in fixed physical units and independent of cutoff and volume.
- Same-theory: the observable, Schwinger functions, OS vector, and Hamiltonian are recovered from the same limiting family.
- Validity: C_A(t)=<v_A,exp(-tH)v_A> is a positive covariance, so no sign cancellation is used.

## Equations

- connected spectral representation: `C_A(t)=\langle v_A,e^{-tH}v_A\rangle=\int_{0}^{\infty}e^{-t\lambda}\,d\mu_A(\lambda)`. Valid when: Valid when A is a time-zero gauge-invariant observable whose vacuum-orthogonal OS vector exists in the reconstructed Hilbert space.
- low interval squeeze: `\mu_A([0,a])e^{-at}\le C_A(t)\le C_0e^{-mt}\quad(0\le a<m)`. Valid when: Applies for every low-energy cutoff a below m after reflection positivity gives a positive Laplace transform.
- support exclusion: `\forall a<m:\ \mu_A([0,a])=0\quad\Longrightarrow\quad E_H([0,m))v_A=0`. Valid when: Requires the preceding large-time bound with finite C_0 in the same physical units for the same vector.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Laplace-Transform Support From Uniform Euclidean Decay; source object: same-theory OS-positive Euclidean Schwinger family S with a time-zero gauge-invariant Wilson observable A and connected covariance C_A(t).; target object: reconstructed OS Hilbert-space vector v_A=P_perp A\Omega and its Hamiltonian spectral measure \mu_A(B)=\langle v_A,E_H(B)v_A\rangle.; Model: four-dimensional Euclidean Yang-Mills candidate after OS reconstruction on the gauge-invariant observable algebra..
- Freeze the Clay target: assume, only for this local theorem, a same-theory OS-positive continuum Schwinger family, OS reconstruction, vacuum \Omega, Hamiltonian H>=0, and recovered gauge-invariant Wilson observable A.
- Set v_A=P_perp A\Omega. Reflection positivity and time translation give C_A(t)=<v_A,e^{-tH}v_A>, hence by the spectral theorem C_A(t)=int exp(-t lambda)d mu_A(lambda).
- For any a<m, positivity gives mu_A([0,a])e^{-at} <= C_A(t). The assumed large-time decay gives mu_A([0,a]) <= C_0 exp(-(m-a)t), so t->infinity forces mu_A([0,a])=0.
- Since [0,m) is the countable union of [0,a] with rational a<m, mu_A([0,m))=0 and E_H([0,m))v_A=0.
- If a set D of such Wilson vectors is dense in P_perp H and the same m applies to all v in D, closedness of E_H([0,m)) gives E_H([0,m))P_perp=0.
- Compare abstractions: the scalar Laplace lemma is sharp but too weak to remember density, regulator recovery, and error budgets; a Wilson-Schwinger spectral-carrier packet is the minimal efficient representation for further investment.

Blocking gap: The analytic proof is complete locally, but the Clay-facing gap is gauge-invariant observable density with cutoff-uniform decay and same-theory recovery. The current branch has no independent continuum Schwinger construction, RG basin entry, large-field/topology summability, or nontrivial connected cumulant witness.

## Falsifiers

- falsifier: the covariance decay is proved only at fixed cutoff or finite volume and the constants degenerate in the continuum limit, confirming uniformity_gap and forcing demotion to artifact_sprint.
- falsifier: the decaying observable is a proxy not recovered by the same Schwinger family, confirming definitional_transfer and forcing reframe or quarantine.
- falsifier: Wilson observables are not dense in the vacuum-orthogonal OS Hilbert sector, so the result remains a visible-sector spectral measure witness only.
- falsifier: a nontrivial continuum family exists but connected Wilson cumulants vanish in the limit, removing the nontriviality physical carrier.
- falsifier: OS positivity fails after the proposed regulator/RG limit, so the Laplace measure is not positive and support exclusion is invalid.
- Stress case: spectral mass accumulates at zero in vectors outside the Wilson closure while every fixed Wilson loop decays exponentially; this demotes the route to gauge-invariant observable density work.

## Learning

Conceptual pressure attacked: the route must convert Euclidean correlation decay into Hamiltonian spectral support without smuggling in the mass gap through definitions. Declarative tension: OS positivity, same-theory continuum recovery, gauge-invariant observable density, nontriviality, and uniform decay must hold simultaneously; the missing mediator is a representation that tracks all five through limits. The current scalar Laplace concept is sharp and valid for one vector but representation-limited: it forgets recovery maps, density, large-field/topology errors, and noncommuting limits. Compared with finite Route A endpoint cumulants, this OS route touches the positive spectral mass gap gate directly but has less finite calculability; Route A gives a connected cumulant witness but not spectral transfer. Efficient representation requirements: encode regulator Wilson observables, connected Schwinger cumulants, OS reflection forms, recovery maps, RG morphisms, error budgets, equivalence only by identical continuum Schwinger data, primitive operations of restriction/reflection/RG pushforward/spectral-window testing, locality budget by collar diameter, and falsifiers for proxy_shift and uniformity_gap. physical relevance is support-only pending handoff: the physical carrier is a gauge-invariant Wilson covariance as an OS Hilbert spectral-measure object. The touched Clay gate is OS spectral transfer toward a positive spectral mass gap; untouched gates are same-theory continuum construction, OS/Wightman reconstruction proof, observable density, and nontriviality. general impact: success would clarify exactly which Euclidean decay estimates are physics-bearing; failure would show that exponential Wilson decay alone can be spectrally invisible. unification power: one spectral-carrier packet compresses Wilson observables, Schwinger functions, OS positivity, density, and decay constants, exposing the new proof obligation of density-uniformity compatibility. Visual metaphor: a sieve placed after OS reconstruction catches low spectral sand only for grains poured through recovered Wilson channels; it preserves positivity, order, locality of channels, limiting flow, and the spectral physical carrier. Distortion ledger: the image hides RG topology and may make density too easy, encouraging finite_to_global_gap or definitional_transfer; use it as explanation_only unless it yields the alpha-refinement falsifier above.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and representation artifact sprint, not as broad exploration.`
- Rationale: The branch has repeated the OS spectral bridge many times; the decisive issue is whether a concrete Wilson family can carry density and uniform decay in the same theory.
- Situation seed: SU(3) heat-kernel lattice Yang-Mills on a four-torus with reflection plane t=0; take vacuum-subtracted rectangular Wilson loops W_{gamma,epsilon}-<W_{gamma,epsilon}> in a time-zero collar and follow a fixed continuum subsequence with OS-positive Schwinger functions.
- Varied variable: alpha, the observable-net refinement exponent in the maximal physical loop diameter r(epsilon)=epsilon^alpha used to approximate the Wilson algebra closure.
- Held-fixed controls: Gauge group SU(3), heat-kernel regulator, reflection plane, and gauge-invariant Wilson observables are fixed., The continuum subsequence, physical scale setting, vacuum subtraction, and same-theory recovery map are fixed., The target remains the Clay same-theory OS/Wightman Yang-Mills construction with positive spectral mass gap; no proxy scalar theory is allowed.
- Expected observation: If C_gamma(epsilon) and m_gamma have alpha-uniform physical bounds while the Wilson net becomes Hilbert-dense, the spectral measure witness can promote to an OS spectral-transfer obligation. If constants blow up as alpha approaches density, the earliest decisive failure is uniformity_gap and the branch must demote.
- Transfer certificate needed: A validator-facing certificate for gauge-invariant observable density, cutoff-uniform connected covariance decay, OS positivity in the continuum topology, nontrivial connected cumulant witness, and regulator/RG basin entry with large-field and topology tails.

## Next Experiment

Route to abstraction refit plus validator-facing falsifier sprint: instantiate the spectral-carrier packet for the SU(3) heat-kernel Wilson-net thought experiment, varying only alpha, and record recovery errors, OS positivity margins, connected cumulant witness/non-Gaussian Schwinger family marker, gauge-invariant observable density status, and physical-unit decay constants. Promote if a dense spectral measure witness with common m survives; demote or quarantine on uniformity_gap, proxy_shift, missing_carrier, or noncommuting_limits.

# Post-H,K endpoint polarization R as a heat-kernel Wilson cumulant screen

## Candidate Lemma

In finite SU(N) heat-kernel lattice Yang-Mills with fixed reflected H,K endpoint geometry, the post-H,K endpoint polarization R_ij can be represented as a renormalized connected cumulant of gauge-invariant plaquette-sheet endpoint sources. Its first calculable term is a signed weighted sum of squared two-gluon plaquette kernels, with explicit sixth-order, recovery, large-field, and topology remainders. This is a finite artifact-sprint theorem candidate, not a Clay mass-gap theorem.

## Definitions

- source object: finite-volume SU(N) heat-kernel lattice Yang-Mills measure mu_{a,L,beta}^{HK} on a reflected four-dimensional hypercubic torus, with gauge-invariant Wilson endpoint sources J_i built from plaquette sheets in the fixed H,K collar/hairpin endpoint boxes.
- target object: an outward-rounded interval certificate I_{ij}(a,L,beta) containing the renormalized endpoint connected cumulant R_{ij}^{ren} and deciding its sign or size after H,K Schur-Feshbach elimination.
- controlled interface: R_{ij}^{ren} is observed only through gauge-invariant Wilson cumulants and recovery maps from plaquette-sheet sources to the same endpoint Wilson observables; the error budget is E_6, E_rec, T_tail, and E_top.
- same-theory condition: the source Wilson observables, reflection map, renormalization factors, and continuum subsequence are fixed independently of the sign test, so the interval is not a proxy-theory or toy-observable transfer.
- physical carrier: the gauge-invariant connected Wilson cumulant witness R_{ij}^{ren}=kappa(delta J_i,Theta delta J_j,Q_HK), where Q_HK is the fixed H,K collar polynomial left by the finite Schur-Feshbach reduction.
- endpoint source: J_i=sum_{p in E_i} omega_{i,p} X_p with X_p=1-N^{-1} Re Tr U_p, signed geometric weights omega_{i,p}, and endpoint plaquette set E_i.
- cancellation used: disconnected products, one-plaquette tadpoles, and diagonal Schur-Feshbach counterterms are subtracted before the cross-endpoint polarization is read.

## Assumptions

- Model: pure SU(N) lattice Yang-Mills with heat-kernel plaquette action, finite L, cutoff a>0, and an exact Euclidean reflection Theta preserving the H,K endpoint geometry.
- Regime: the logarithmic plaquette expansion is used only on a small-field basin; the complement is not discarded but charged to T_tail with a validator-facing bound.
- Cutoff: all constants in the interval certificate are attached to the same a,L,beta regulator and cannot be imported from a different action or blocking map.
- Same-theory: J_i, Theta J_j, Q_HK, and Z_i are chosen before observing the sign of R_{ij}^{ren}; no observable replacement is allowed after the interval is computed.
- Uniformity: no continuum or mass-gap conclusion is valid unless E_6, E_rec, T_tail, and E_top have volume- and cutoff-uniform controls along a fixed directed limiting net.

## Equations

- endpoint-cumulant-definition: `\delta J_i=J_i-\langle J_i\rangle,\qquad R_{ij}^{ren}=Z_iZ_j\,\kappa_{\mu_{a,L,\beta}^{HK}}(\delta J_i,\Theta\delta J_j,Q_{HK})`. Valid when: Valid when J_i and Q_HK are the fixed endpoint Wilson sources in the finite heat-kernel lattice measure before any continuum inference is made.
- plaquette-small-field-input: `X_p=1-\frac{1}{N}\operatorname{Re}\operatorname{Tr}U_p=\frac{a^4}{4N}F_p^A F_p^A+O(a^6|F_p|^3)`. Valid when: Applies after choosing logarithmic plaquette fields inside the small-field basin and after the heat-kernel large-field complement is isolated as T_tail.
- first-cross-contraction: `R_{ij}^{(2)}=\frac{Z_iZ_j a^8}{8N^2}\sum_{p\in E_i}\sum_{q\in E_j}\omega_{i,p}\omega_{j,q}\,K_{pq}^{AB}K_{pq}^{AB}`. Valid when: Requires the disconnected product, one-plaquette tadpoles, and Schur-Feshbach diagonal counterterms to be subtracted in the connected endpoint cumulant.
- color-diagonal-specialization: `K_{pq}^{AB}=\delta^{AB}D_{pq}\quad\Longrightarrow\quad R_{ij}^{(2)}=\frac{Z_iZ_j a^8(N^2-1)}{8N^2}\sum_{p,q}\omega_{i,p}\omega_{j,q}D_{pq}^2`. Valid when: Valid in the gauge-fixed or gauge-invariant covariance representation where the plaquette-field two-point kernel is color diagonal on the chosen endpoint boxes.
- certified-interval-screen: `I_{ij}=\left[R_{ij}^{(2)}-E_6-E_{rec}-T_{tail}-E_{top},\;R_{ij}^{(2)}+E_6+E_{rec}+T_{tail}+E_{top}\right]`. Valid when: Valid when all four error terms are certified by outward-rounded interval arithmetic for the same regulator and endpoint geometry.
- route-decision-condition: `\inf I_{ij}>0\ \hbox{ or }\ \sup I_{ij}<0\quad\hbox{promotes the finite R screen;}\qquad 0\in I_{ij}\quad\hbox{quarantines it.}`. Valid when: Applies only to the finite post-H,K endpoint source screen and not to the positive Hamiltonian mass-gap claim.

## Attempted Derivation

- Attacked conceptual pressure: the branch has repeated the decay-to-gap bridge without a same-theory physical carrier; the finite route must now compute or falsify the endpoint R term carried by a connected Wilson cumulant.
- Fix SU(N) heat-kernel lattice Yang-Mills on a reflected four-torus and freeze H,K endpoint boxes, reflection plane, Wilson normalizations, and Q_HK before any sign decision.
- Represent endpoint observables by signed plaquette-sheet sources J_i=sum omega_{i,p}X_p; this preserves gauge invariance and exposes color/geometric factors instead of using a symbolic R_ij parameter.
- Use X_p=1-N^{-1}ReTr U_p=(a^4/4N)F_p^AF_p^A+O(a^6) on the small-field basin; the traced Wilson variable has no one-gluon term because Tr T^A=0.
- Subtract disconnected products, local tadpoles, and diagonal Schur-Feshbach counterterms; the first cross-endpoint term is therefore the F^2-F^2 connected contraction.
- For the Gaussian heat-kernel covariance core, Wick contraction gives Cov(X_p,X_q)=a^8(8N^2)^{-1}K_{pq}^{AB}K_{pq}^{AB}+higher terms, with color-diagonal specialization (N^2-1)a^8D_{pq}^2/(8N^2).
- Aggregate signed geometric weights omega_{i,p}omega_{j,q} over the endpoint annuli before clipping errors; this is where the sign of R can change despite each squared kernel being nonnegative.
- Split the uncomputed terms into E_6 for sixth-order Wilson expansion, E_rec for recovery from endpoint loops to plaquette sheets, T_tail for large fields and distant annuli, and E_top for topological-sector leakage across RG steps.

Blocking gap: No outward-rounded SU(3) H,K endpoint table is yet available for G_{++}^-, C_{s,0:J}^+, A_{s,J}^+, E_rec^+, E_6^+, q_s, T_tail, and E_top. The current derivation identifies the calculand and cancellations but does not certify the sign.

## Falsifiers

- falsifier: the interval I_{ij} contains zero after outward rounding for the fixed SU(3) H,K endpoint geometry, so the post-H,K R screen cannot decide the route.
- falsifier: E_6+E_rec+T_tail+E_top is larger than the signed leading annular aggregate, showing artifact_debt rather than a physical carrier.
- falsifier: changing the endpoint smearing or recovery map after seeing the sign changes R, exposing proxy_shift and invalid same-theory witness selection.
- falsifier: the R sign is stable at fixed cutoff but disappears when a decreases or L increases, exposing noncommuting_limits and finite_to_global_gap.
- falsifier: the annular representation fails to preserve reflection pairing or gauge-invariant Wilson observables, so the claimed efficient representation is merely convenient bookkeeping.
- falsifier: prior art already gives the same endpoint cumulant interval with the same reflection-positive transfer interface, causing literature_collision and demotion.

## Learning

Declarative tension: a Clay-valid route must keep gauge-invariant Wilson observables, OS positivity, continuum same-theory limits, nontriviality, and positive spectral mass gap simultaneously, but the current mass-scale concept is too weak and fragmented because m_{a,L} can be named without a carrier that survives cutoff removal. Compared with another abstract OS spectral bridge, the annular endpoint-R representation is sharper because it makes the physical carrier, sign, locality, and error budget computable. Efficient representation requirements are: encode endpoint Wilson sheets and annuli; preserve gauge invariance, reflection pairing, color/tensor contraction, locality, and same-theory normalization; allow primitive operations of reflection, annular summation, cumulant subtraction, interval contraction, and tail clipping; identify equivalence by induced Wilson cumulants; keep finite locality complexity plus summable tails; expose transfer through Schwinger convergence and OS positivity; and fail under proxy_shift, finite_to_global_gap, uniformity_gap, or no_falsifier. Visual metaphor: R is a reflected polarizing gasket between two Wilson endpoint boxes; the image preserves symmetry, locality, positivity/sign bookkeeping, and limiting-pressure through gasket leaks, but it hides nonabelian topology and can make finite-to-global transfer look too easy, so it is hypothesis_seed requiring preservation audit. Physical relevance is conditional: success changes the connected-cumulant physical carrier and the nontriviality gate; failure teaches that post-H,K endpoint polarization is not the unifying mechanism. General impact would be a clear finite obstruction or witness selection rule recognizable to constructive-QFT readers. Unification power is the compression of endpoint Schur complements, Wilson OPE recovery, reflection positivity, and large-field remainders into one interval certificate; the exposed new obligation is cutoff-uniform same-theory Schwinger transfer. Failure signature anticipated: finite_to_global_gap; if confirmed, run falsifier_sprint then quarantine rather than broad proof search.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a concrete falsifier probe and artifact sprint.`
- Rationale: The branch is looping on the abstract mass-scale bridge. A target-preserving SU(3) endpoint cumulant computation is the smallest valid move that can change the finite OS obstruction proof state without claiming the Clay theorem.
- Situation seed: SU(3) heat-kernel lattice Yang-Mills on a reflected four-dimensional torus with fixed H,K endpoint boxes; compute the connected cumulant witness R_{++}^{ren}=kappa(delta J_+,Theta delta J_+,Q_HK) by annular plaquette-sheet contractions and outward-rounded interval arithmetic.
- Varied variable: endpoint smearing exponent zeta in the fixed plaquette-sheet recovery map.
- Held-fixed controls: Gauge group SU(3), heat-kernel action, reflection plane, H,K endpoint geometry, and Wilson trace normalization are fixed., The source Wilson observable family, recovery map template, continuum subsequence policy, and Q_HK collar polynomial are fixed before reading the sign., Large-field basin cutoff, topology bookkeeping rule, and interval rounding convention are fixed across all zeta values.
- Expected observation: Either the signed annular aggregate Delta_R^- remains separated from zero after E_6, E_rec, T_tail, and E_top for a stable zeta window, or every valid window is swallowed by remainders and the endpoint-R route is quarantined.
- Transfer certificate needed: Before the intuition may affect Clay proof obligations, one needs regulator-independent Schwinger convergence for the same Wilson observables, OS positivity in the continuum topology, large-field/topological summability across RG steps, and a nonzero same-theory nontriviality witness.

## Next Experiment

Proof-search artifact sprint: construct the SU(3) heat-kernel H,K endpoint annular table for the connected cumulant witness R_{++}^{ren}, varying only zeta, and output G_{++}^-, C_{s,0:J}^+, A_{s,J}^+, E_rec^+, E_6^+, q_s, T_tail, E_top, Delta_R^-, and I_{++}. Include a physical-relevance pass/fail line: stable nonzero same-theory nontriviality witness promotes to transfer-boundary work; zero-containing or proxy-dependent intervals quarantine the branch.

