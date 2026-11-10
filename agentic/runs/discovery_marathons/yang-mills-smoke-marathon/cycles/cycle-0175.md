# cycle-0175

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`

## Branch Outputs

# Reflection-Positivity Closed-Cone Topology: boundary trace modulus and same-theory obstruction

## Candidate Lemma

Boundary-defect-free collar trace bridge. Let \(S_{a,L}\) be regulated reflection-positive Schwinger functionals on a locked gauge-invariant positive-time algebra \(\mathcal A_+\), and suppose \(S_{a,L}\to S\) in a cutoff-removal topology that is valid for every fixed positive collar. If, for every finite family \(F_1,\ldots,F_N\in\mathcal A_+\) and coefficients \(c\in\mathbb C^N\), the collar translations \(T_\delta F_i\) satisfy a trace modulus \(Q_S(T_\delta F,c)\to Q_S(F,c)\) as \(\delta\downarrow0\), with no new reflection-plane renormalization, then \(S\) is OS-positive on \(\mathcal A_+\). If the estimate first holds on a core \(\mathcal A_+^{\mathrm{core}}\), it extends to the full algebra exactly when that core is dense for the resulting OS seminorm without changing the observable identifications.

## Definitions

- source object: a directed family \((S_{a,L},\mathcal A_{a,+},\iota_{a,L})\) of finite-cutoff gauge-invariant Schwinger forms, each satisfying regulated reflection positivity on the same abstract positive-time observable labels after embedding \(\iota_{a,L}:\mathcal A_+\to\mathcal A_{a,+}\).
- target object: a continuum gauge-invariant Schwinger functional \(S\) on the locked positive-time algebra \(mathcal A_+\), equipped with the OS quadratic form \(Q_S(F,c)=\sum_{i,j}\overline c_i c_j S((\Theta F_i)^*F_j)\), from which the reconstructed physical Hilbert space and positive Hamiltonian would be obtained.
- controlled interface: the finite reflected quadratic forms \(Q_{a,L}(T_\delta F,c)\to Q_S(T_\delta F,c)\) for collar translations \(T_\delta\) moving supports a distance \(\delta>0\) away from the reflection plane, together with the boundary trace limit \(Q_S(T_\delta F,c)\to Q_S(F,c)\).
- same-theory condition: the embeddings, collar translations, and renormalization maps commute in the OS seminorm up to errors vanishing as \(a\to0,L\to\infty,\delta\downarrow0\), and no \(\delta\)-dependent boundary counterterm, cusp factor, plane observable, or changed Wilson-loop normalization is introduced at the reflection plane.

## Assumptions

- For each cutoff \((a,L)\), reflection positivity holds on the regulated gauge-invariant algebra: \(Q_{a,L}(G,c)\ge0\) for all \(G_i\in\mathcal A_{a,+}\).
- For each fixed collar \(\delta>0\), the RG/cutoff-removal topology controls the reflected probe: \(Q_{a,L}(T_\delta F,c)\to Q_S(T_\delta F,c)\).
- The family \(F_i\) belongs either to the full locked algebra or to a declared core that is later proved OS-dense in the full algebra.
- Trace modulus: for every finite \((F,c)\), there exists \(\omega_{F,c}(\delta)\downarrow0\) such that \(|Q_S(T_\delta F,c)-Q_S(F,c)|\le\omega_{F,c}(\delta)\).
- The trace modulus is same-theory: it is not achieved by rescaling observables with a boundary factor or by adding a reflection-plane defect functional.

## Equations

- fixed-collar positivity transfer: `Q_{a,L}(T_\delta F,c)\ge 0,\qquad Q_{a,L}(T_\delta F,c)\longrightarrow Q_S(T_\delta F,c)\quad\Longrightarrow\quad Q_S(T_\delta F,c)\ge0`. Valid when: Valid for each fixed \(\delta>0\) when the cutoff-removal topology includes the reflected finite quadratic form determined by the collar-separated observables.
- boundary trace modulus: `\left|Q_S(T_\delta F,c)-Q_S(F,c)\right|\le \omega_{F,c}(\delta),\qquad \omega_{F,c}(\delta)\xrightarrow[\delta\downarrow0]{}0`. Valid when: Valid only if reflected products approaching the plane have no uncancelled contact, cusp, or boundary-renormalization defect.
- OS positivity by collar limit: `0\le \liminf_{\delta\downarrow0} Q_S(T_\delta F,c)=Q_S(F,c)`. Valid when: Valid after fixed-collar positivity and the same-theory trace modulus have both been established for the chosen finite family.
- same-theory commutator condition: `\lim_{\delta\downarrow0}\limsup_{a,L}\,\big|Q_{a,L}(\iota_{a,L}T_\delta F,c)-Q_{a,L}(T_\delta\iota_{a,L}F,c)\big|=0`. Valid when: Valid when the cutoff observable embedding and the collar displacement represent the same continuum gauge-invariant observable, not two differently renormalized theories.

## Attempted Derivation

- Start with finite \(F_1,\ldots,F_N\in\mathcal A_+\) and coefficients \(c\). For each \(\delta>0\), set \(F_i^\delta=T_\delta F_i\), so all supports lie in the open positive-time collar \(t\ge\delta\).
- Use regulated reflection positivity: \(Q_{a,L}(F^\delta,c)=\sum_{i,j}\overline c_i c_jS_{a,L}((\Theta F_i^\delta)^*F_j^\delta)\ge0\).
- Invoke the fixed-collar part of the RG limit. Because the reflected supports are separated by distance \(2\delta\), the limiting topology is assumed strong enough to pass this finite quadratic form: \(Q_{a,L}(F^\delta,c)\to Q_S(F^\delta,c)\). Hence \(Q_S(F^\delta,c)\ge0\).
- For \(F_i\) in the mirror-smooth core, represent each reflected product by a full-space test tensor \(\Phi_{ij,\delta}\). The geometry is chosen so that \(\Phi_{ij,\delta}\to\Phi_{ij,0}\) in the same test topology on which \(S\) is continuous.
- Apply distributional continuity termwise: \(S(\Phi_{ij,\delta})\to S(\Phi_{ij,0})\), hence \(Q_S(F^\delta,c)\to Q_S(F,c)\). Since every \(Q_S(F^\delta,c)\ge0\), the limit gives \(Q_S(F,c)\ge0\).
- To extend beyond the mirror-smooth core, one would need to prove that every locked positive-time gauge-invariant observable is the OS-seminorm limit of mirror-smooth observables, with no extra boundary renormalization. This is precisely where cusp loops, intersection loops, and local curvature contact terms must be controlled.

Blocking gap: The unproved gap is the same-theory trace modulus outside the mirror-smooth core. Current RG compactness estimates may control separated reflected probes, but they do not yet rule out reflection-plane contact terms, Wilson-loop cusp/intersection renormalization, or composite-operator boundary mixing as \(\delta\downarrow0\).

## Falsifiers

- Cusp-loop falsifier: choose a family of positive-time Wilson loops \(\ell_\delta=T_\delta\ell\) whose reflected double develops a cusp or intersection at \(t=0\); if the continuum expectation contains a nontrivial \(Z_{\mathrm{cusp}}(\delta,\theta)\), the trace modulus is not same-theory valid.
- Curvature-contact falsifier: take smeared \(\operatorname{tr}F_{\mu\nu}F^{\mu\nu}\) observables whose supports approach the plane; if the OPE of \((\Theta O)O\) produces a surviving \(\delta(t)\)-supported counterterm, collar positivity does not transfer to the original OS form.
- Topology falsifier: the Balaban/RG convergence topology controls only separated ordinary Schwinger distributions but not the reflected tensors \(\Phi_{ij,\delta}\) uniformly as \(\delta\downarrow0\). Then fixed-collar closedness is valid but boundary passage is unproved.
- Algebra-change falsifier: if the proof obtains continuity only after restricting to mirror-smooth observables and this core is not OS-dense in the locked algebra, the resulting positivity is for a smaller theory.
- Renormalization-commutator falsifier: if \(\iota_{a,L}T_\delta F\) and \(T_\delta\iota_{a,L}F\) have different limiting renormalization constants near the plane, the source and target objects are not the same theory.

## Learning

Cycle 175 turns the trace-modulus slogan into a concrete two-layer program. The positivity passage is valid and short once \(Q_S(T_\delta F,c)\to Q_S(F,c)\) is known, but that estimate is exactly where Yang-Mills singular geometry enters. A mirror-smooth gauge-invariant core gives a plausible route because ordinary distributional continuity can prove the trace limit there. The real discovery is the obstruction criterion: cusp anomalous factors, curvature contact terms, or boundary counterterms are not minor technicalities; any one is a falsifier of the same-theory bridge. Thus the branch has isolated a precise analytic target: prove no-new-boundary-renormalization plus OS-density of the mirror-smooth core, or exhibit a concrete cusp/contact counterexample.

## Next Experiment

Work out one model boundary calculation: take a local gauge-invariant curvature composite smeared by \(\phi(t,x)\) with \(\phi\) nonflat at \(t=0\), compute the expected OPE scaling of \(S((\Theta T_\delta O_\phi)O_{T_\delta\phi})\), and determine whether the singular terms pair to an ordinary distributional limit or require a plane-supported subtraction. In parallel, formulate the analogous Wilson-loop test for a reflected double developing a cusp at the plane.
