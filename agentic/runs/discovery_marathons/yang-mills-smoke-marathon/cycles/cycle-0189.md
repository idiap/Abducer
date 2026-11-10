# cycle-0189

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: Wilson Boundary Cross-Ratio Test

## Candidate Lemma

Finite OS-matrix same-theory transfer across the reflection plane is valid for Wilson-loop collars if and only if every boundary multiplicative anomaly is either absent or a rank-one diagonal congruence already included in the locked observable normalization; equivalently the logarithmic anomaly cross-ratio K vanishes on every finite reflected Wilson family. Any nonzero connected coincident-footprint boundary OPE coefficient gives a same-theory falsifier.

## Definitions

- source object: regulated reflection-positive Schwinger forms S_{a,L} on a locked gauge-invariant positive-time algebra A_+^{lock}, with Wilson-loop collar observables W(C_\delta) and mirror-flat local composites, converging on fixed-collar reflected probes.
- target object: continuum Schwinger functions S on the same locked algebra, satisfying OS positivity so that OS reconstruction yields a Hilbert space, vacuum vector, and positive time-translation generator.
- controlled interface: regulated reflection-positive Schwinger forms -> OS-positive continuum Schwinger functions, with the only delicate interface being the trace limit from positive-time collars to observables touching the reflection plane.
- same-theory condition: the cutoff embeddings and collar maps identify the same gauge-invariant observable before and after cutoff removal; one-body Wilson renormalizations are allowed as fixed diagonal congruences, but any pair-dependent boundary factor or boundary counterterm is a falsifier unless it has zero logarithmic cross-ratio.

## Assumptions

- For each fixed collar distance delta>0, RG convergence controls all finite reflected OS matrix entries for A_+^{lock}.
- Diagonal trace continuity is valid: each individual Wilson collar has the intended boundary limit after the predeclared one-body renormalization.
- Mixed reflected Wilson collar limits admit a finite boundary expansion N_{ij}=Gamma_{ij} M_{ij}+A_{ij}, where N is the collar-limit OS matrix, M is the intended target OS matrix, Gamma_{ij}!=0 is multiplicative, and A is additive contact.
- The additive contact part, when present as an independent boundary OPE contribution to a positive collar theory, is positive semidefinite as a finite OS kernel.

## Equations

- fixed-collar OS matrix: `N^{(\delta)}_{ij}=S(\Theta W(C_{i,\delta})\,W(D_{j,\delta})),\qquad N^{(\delta)}\ge 0`. Valid when: The collar supports stay in t>0 at distance delta from the reflection plane and the regulated reflection positivity plus RG convergence are valid for these reflected probes.
- boundary anomaly decomposition: `N_{ij}=\lim_{\delta\downarrow0}N^{(\delta)}_{ij}=\Gamma_{ij}M_{ij}+A_{ij},\qquad \Gamma_{ij}=e^{b_{ij}}`. Valid when: The Wilson collar trace has a finite boundary OPE expansion after fixed one-body renormalizations; M is the intended same-theory matrix entry.
- logarithmic cross-ratio obstruction: `K_{ik;j\ell}=b_{ij}+b_{k\ell}-b_{i\ell}-b_{kj}`. Valid when: All Gamma entries are nonzero and a consistent branch of log Gamma is chosen on the finite family; K=0 for all i,k,j,ell exactly means Gamma_{ij}=alpha_i\overline{alpha_j} on each connected component.
- Schur transfer criterion: `M=\Gamma^{[-1]}\circ (N-A),\qquad \Gamma^{[-1]}_{ij}=1/\Gamma_{ij}`. Valid when: The boundary anomaly decomposition is valid entrywise; positivity transfers from every positive N to M if A=0 and Gamma^{[-1]} is a positive Schur multiplier, with the same-theory case reducing to K=0 under positivity of Gamma.

## Attempted Derivation

- Fix a finite family of positive-time Wilson collar observables. For every delta>0, regulated reflection positivity and the fixed-collar RG-to-OS passage give a positive finite matrix N^{(delta)}; if every reflected entry converges, closedness of the positive cone gives N=lim_{delta downarrow 0}N^{(delta)}>=0.
- Insert the most general finite boundary trace expansion compatible with multiplicative Wilson renormalization plus additive contacts: N=Gamma circ M + A. Here M is the intended same-theory OS matrix; Gamma records pair-dependent boundary factors not already absorbed into one-body normalizations.
- Use diagonal trace continuity: A_{ii}=0 after the locked one-body normalization. If A is a positive additive contact kernel, Cauchy-Schwarz gives |A_{ij}|^2<=A_{ii}A_{jj}=0, so A=0. Thus a genuine positive additive boundary defect cannot survive once the diagonal trace is valid.
- With A=0, the intended matrix is M=Gamma^{[-1]} circ N. Schur product theory says positivity is preserved for all possible positive N if Gamma^{[-1]} is positive semidefinite. If Gamma is also a positive boundary kernel with normalized diagonal, then positivity of both Gamma and Gamma^{[-1]} forces |Gamma_{ij}|=1 in every 2-by-2 minor, hence Gamma_{ij}=alpha_i overline{alpha_j}; this is exactly K=0.
- Therefore the substantive Yang-Mills estimate is not the formal closed-cone passage but the assertion that the connected coincident-footprint boundary OPE has no multiplicative cross-ratio contribution for the locked Wilson algebra.

Blocking gap: No current constructive Yang-Mills estimate proves that reflected Wilson collar products have zero connected coincident-footprint boundary OPE after one-body perimeter/area/cusp renormalization. The gap is especially sharp for hairpin or cusp degenerations at t=0, where a pair-dependent anomalous dimension could produce K!=0.

## Falsifiers

- Nonzero logarithmic cross-ratio K_{ik;jl} computed for four reflected Wilson hairpin collars with the same boundary footprint.
- A pair-dependent multiplicative damping Gamma_{ij} with normalized |Gamma_{ij}|<1 for some mixed Wilson entry; the reciprocal multiplier then fails the 2-by-2 positivity test.
- Failure of RG convergence for mixed reflected Wilson products even though single Wilson-loop collars converge; this would show the cutoff-removal topology is not valid for OS probes.
- A boundary counterterm required only for reflected products, not for individual Wilson observables; this changes the test algebra and is a same-theory falsifier.
- An additive contact matrix with zero diagonal but nonzero off-diagonal contribution, contradicting positive contact compatibility and indicating an uncontrolled indefinite boundary OPE term.

## Learning

Cycle 189 identifies the next invariant more locally: K is not just an abstract finite-matrix obstruction but the polarization of a connected boundary OPE kernel for reflected Wilson hairpins. The valid linear-algebra bridge says positivity survives the collar limit only through zero/rank-one multiplicative anomaly after additive contacts vanish. Thus the analytic Yang-Mills target is precise: prove the connected coincident-footprint boundary kernel is zero on the locked Wilson core, or compute a nonzero hairpin K as a falsifier.

## Next Experiment

Work out the infinitesimal hairpin expansion in a controlled model or perturbative Yang-Mills gauge-invariant regularization: isolate one-body cusp/perimeter terms, compute the connected boundary bilinear B(J,J'), and test whether its polarized cross-ratio K vanishes.
