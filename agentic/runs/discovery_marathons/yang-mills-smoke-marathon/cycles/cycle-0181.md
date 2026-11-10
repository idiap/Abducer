# cycle-0181

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: finite OS-matrix boundary-defect factorization

## Candidate Lemma

Finite reflected Wilson-product boundary defects are harmless for OS positivity only when they are induced by an invertible congruence on the finite observable span; in the locked same-theory interface they must in fact be absent, or be exactly a predeclared observable renormalization. More precisely, for every finite family F_1,...,F_n in the positive-time gauge-invariant algebra, if the collar limits satisfy N(F) = lim_{delta downarrow 0} M_delta(F) = R(F)^* M(F) R(F) with R(F) invertible and compatible under restriction of finite families, then positivity of all collar matrices N(F) implies OS positivity of the intended target matrices M(F). If instead N(F)=M(F)+E(F) with a pair-dependent mixed boundary defect E(F) not representable by such a congruence, the closed-cone argument is valid only for the boundary-renormalized theory N, not for the intended continuum Yang-Mills Schwinger functions M.

## Definitions

- source object: a net of cutoff/collar Schwinger functionals S_{a,L,delta} on a locked gauge-invariant positive-time test algebra, including Wilson loop observables T_delta F supported in t>=delta and satisfying lattice/reflection positivity before cutoff removal.
- target object: continuum Schwinger distributions S on the same gauge-invariant observable algebra, with OS matrices M(F)_{ij}=S(Theta F_i · F_j) required to be positive semidefinite for all finite positive-time families.
- controlled interface: RG convergence first at fixed collar delta for every reflected finite OS matrix entry, followed by a trace/collar limit delta downarrow 0 whose defect must be identified at the matrix level, not merely observable by observable.
- same-theory condition: the collar trace map is the identity on the locked renormalized observables, or an already fixed invertible congruence coming from the same observable renormalization; no pair-dependent Wilson cusp, hairpin, or boundary-contact factor may be inserted after the target theory has been specified.

## Assumptions

- For each fixed delta>0 and finite family F, the cutoff matrices M_{a,L,delta}(F) with entries S_{a,L}(Theta T_delta F_i · T_delta F_j) are positive semidefinite.
- The cutoff-removal topology is strong enough that M_{a,L,delta}(F) converges entrywise to M_delta(F) for every finite reflected collar family; hence M_delta(F) is positive semidefinite.
- For the finite span V_F=span{F_1,...,F_n}, the trace limit N(F)=lim_{delta downarrow 0} M_delta(F) exists entrywise.
- There is either no defect, N(F)=M(F), or a compatible invertible finite-span operator R(F) with N(F)=R(F)^*M(F)R(F). Compatibility means that passing to a subfamily restricts R(F), so the construction does not depend on an artificial enlargement of the test algebra.

## Equations

- finite OS matrix: `M_S(F)_{ij}=S(\Theta F_i\cdot F_j),\qquad Q_S(F,c)=c^*M_S(F)c`. Valid when: F_i belong to the positive-time gauge-invariant test algebra and the reflected product is a valid Schwinger distributional pairing.
- collar positivity after RG limit: `M_{a,L,\delta}(F)\ge 0,\quad M_{a,L,\delta}(F)\to M_\delta(F)\quad\Longrightarrow\quad M_\delta(F)\ge 0`. Valid when: delta>0 is fixed and the RG topology controls every reflected collar matrix entry.
- trace defect decomposition: `N(F)_{ij}:=\lim_{\delta\downarrow0}S(\Theta T_\delta F_i\cdot T_\delta F_j)=M(F)_{ij}+E(F)_{ij}`. Valid when: The collar trace limit exists; E(F)=0 is the strict same-theory case, while nonzero E(F) must be justified as an already locked renormalization rather than an added boundary theory.
- congruence-safe defect: `N(F)=R(F)^*M(F)R(F),\quad R(F)\in GL(V_F)\quad\Longrightarrow\quad M(F)\ge0\ \text{if}\ N(F)\ge0`. Valid when: The defect is induced by an invertible observable reparametrization compatible across all finite OS matrices.
- rank-one multiplicative Wilson-factor test: `B_{ij}=\frac{N_{ij}}{M_{ij}},\qquad B_{ij}B_{kl}=B_{il}B_{kj}\ \text{for all}\ i,j,k,l`. Valid when: All relevant M_{ij} are nonzero and the suspected Wilson boundary anomaly is multiplicative; the displayed vanishing of all 2-by-2 minors is the finite-family test for B_{ij}=\overline z_i z_j, hence for a diagonal congruence.

## Attempted Derivation

- Fix a finite positive-time family F=(F_1,...,F_n) in the locked gauge-invariant algebra and choose collar representatives T_delta F_i supported a positive distance delta from the reflection plane.
- At the regulated level, reflection positivity gives c^*M_{a,L,delta}(F)c >= 0 for all c in C^n. This is valid because the reflection plane separates Theta T_delta F_i from T_delta F_j and the lattice/regulated transfer-matrix positivity applies to the gauge-invariant algebra.
- Use the RG-to-continuum topology at fixed delta to pass a,L to the continuum entrywise. Since the positive semidefinite cone in finite Hermitian matrices is closed, M_delta(F)>=0.
- Assume the trace limit N(F)=lim_{delta downarrow 0}M_delta(F) exists entrywise. Again by finite-dimensional closedness, N(F)>=0.
- If the trace theorem proves N(F)=M(F), then M(F)>=0 and OS positivity for this finite family follows immediately. This is the strict no-defect same-theory case.
- More generally, if the trace theorem proves N(F)=R(F)^*M(F)R(F) with R(F) invertible and already induced by locked observable renormalization, then for any x choose y=R(F)^{-1}x; x^*M(F)x=y^*N(F)y>=0. Thus positivity transfers through an invertible congruence.
- Now test why a merely positive collar limit is insufficient. Let M=[[1,2],[2,1]], which is not positive because it has eigenvalue -1. Let a pair-dependent boundary defect E=[[0,-2],[-2,0]], so N=M+E=I is positive. The collar theory would be OS-positive, but it gives no proof that the intended target M is positive. This model captures the logical risk of a nonfactorizing mixed Wilson cusp/contact defect.

Blocking gap: The missing Yang-Mills theorem is the finite OS-matrix trace theorem for reflected Wilson products: as collars collapse to t=0, prove E(F)=0, or prove an invertible compatible congruence already locked into the observable renormalization. Existing RG compactness and single-loop convergence do not by themselves control mixed reflected cusp, hairpin, or contact terms.

## Falsifiers

- A concrete mixed Wilson block with anomaly ratios B_{ij} satisfying B_{11}B_{22} != B_{12}B_{21}; this is a falsifier because no individual loop renormalization can turn the collar-positive matrix into the intended target OS matrix by congruence.
- A reflected hairpin family whose cusp anomalous factor depends on the pair of loops rather than on each loop separately, producing an additive or multiplicative matrix defect E(F) that is not compatible under restriction of finite families.
- A boundary contact term supported at t=0 in the product Theta W(C_delta) · W(D_delta) that survives the delta downarrow 0 limit and is not part of the predeclared continuum Schwinger functional.
- A cutoff-removal topology that is valid for fixed collars but not uniform enough to take the trace limit over the finite OS matrix entries.
- An observable-algebra change in which boundary-renormalized Wilson products are silently added; this may preserve reflection positivity but is a falsifier of the same-theory condition.

## Learning

Cycle 181 converts the Wilson obstruction into a finite-dimensional linear algebra criterion. The closed-cone passage proves positivity for the collar limit N, but the intended target M inherits positivity only if the boundary trace defect is zero or an invertible congruence already built into the same theory. This yields a sharp falsifier: a nonfactorizing mixed Wilson anomaly detected by a nonzero 2-by-2 multiplicative minor. The local mirror-flat sector still looks valid by distributional continuity, so the remaining hard Yang-Mills estimate is specifically a finite OS-matrix no-new-boundary-renormalization theorem for reflected Wilson products.

## Next Experiment

Work out a 2-by-2 mixed Wilson block for mirror-symmetric hairpin/cusp loop families approaching t=0. Compute or bound the anomaly ratios B_{ij}; test whether the rank-one identity B_{11}B_{22}=B_{12}B_{21} is forced by locality/multiplicative renormalization or can fail through a genuine pair-dependent boundary contact.
