# H10 observable-recovery stream report

## Status and claim ceiling

H10 isolates a representational requirement that is weaker than recovering a gauge field and stronger than reproducing a few selected moments: invariant observables should be recovered exactly, or with a controlled error that vanishes in the relevant limits, while directions that only distinguish gauge copies should be erased. The present evidence is toy support only. It establishes the mechanism in a simplified setting, but it does not establish an actual Yang--Mills block-map theorem. The current ceiling is therefore C1. No C3 physical conclusion may be drawn from observable recovery alone.

## Core formulation

Let (X_a) be a regulated fine configuration space, (Y_a) a retained space, (B_a:X_a\to Y_a) a block map, and (R_a:Y_a\to X_a) a reconstruction rule. Let (mathcal O_a^{\mathrm{inv}}) be a declared class of bounded gauge-invariant observables, equipped with a complexity index (m(O)), support (S(O)), and norm (\|O\|_{\mathcal O}). Recovery is observable-indexed, not field-indexed. For a fine state (x), define

\[
e_{a,O}(x)=|O(R_aB_ax)-O(x)|,
\]

and, for a measure (\mu_a),

\[
E_{a,O}^{(p)}=\bigl\|O\circ R_a\circ B_a-O\bigr\|_{L^p(\mu_a)}.
\]

The normalized class error is

\[
\mathfrak E_a(M,L,p)=
\sup_{\substack{O\in\mathcal O_a^{\mathrm{inv}}\\m(O)\le M,\;\operatorname{diam}S(O)\le L}}
\frac{E_{a,O}^{(p)}}{1+\|O\|_{\mathcal O}}.
\]

This quantity separates exact finite recovery, where every indexed error is zero, from approximate recovery, where the supremum is controlled uniformly. It also prevents a finite test list from masquerading as recovery of an observable algebra.

The observable declaration must include its algebraic operations. If sums, products, adjoints, or support unions are used later, their recovery errors need explicit stability estimates. For example, product recovery follows from individual recovery only with uniform bounds on both factors; an unbounded amplification can invalidate the implication. The class should also separate physical orbit classes on the domain actually carrying measure. Separation is not assumed merely because Wilson-type probes are present. These bookkeeping requirements make the claim falsifiable: every promised observable has an index, every index has a norm, and every closure operation has a stated cost.

Gauge-copy erasure requires a second, logically independent statement. If (x' = g\cdot x), the retained or reconstructed representation may forget the difference between (x) and (x'): ideally (B_a(g\cdot x)=B_a(x)), or more generally the retained discrepancy (d_{Y_a}(B_a(g\cdot x),B_a(x))) is zero in the quotient metric. The required asymmetry is therefore

\[
O(R_aB_a(g\cdot x))=O(x)
\quad\text{for invariant }O,
\]

without requiring (R_aB_a(g\cdot x)=g\cdot x). Exact recovery concerns the observable quotient; erasure concerns vertical gauge-orbit directions.

## Composition and uniform continuum limits

For successive blocking levels, write (B_{a\to b}), (R_{b\to a}), and (T_{a\to b}=R_{b\to a}B_{a\to b}). A usable theorem needs a composition inequality. For an observable transported through levels (a_0<a_1<\cdots<a_n), the total defect should be bounded by a sum of one-step defects multiplied only by controlled observable-transport constants. Schematic bounds of the form

\[
E_{a_0,O}(T_{0:n})\le
\sum_{j=0}^{n-1} C_{j,n}(O)\,E_{a_j,O_j}(T_{j:j+1})
\]

are acceptable only when (C_{j,n}) is uniform in volume, cutoff, retained history, and the number of blocking steps at fixed physical scale. Otherwise tiny local errors can accumulate into an order-one continuum failure. This is the H10 interface with the H6 composition-defect calculus.

The continuum target is not pointwise convergence for one observable. For each fixed physical support bound (L) and complexity bound (M), require

\[
\lim_{a\downarrow0}\sup_{V,\,h}\mathfrak E_{a,V,h}(M,L,p)=0,
\]

where the supremum ranges over admissible finite volumes and positive-mass retained histories. Exceptional chart sets, boundary effects, and reconstruction failures must enter the same estimate, with their measure controlled uniformly. H7-style atlas control may supply part of this estimate, but an SU(2) toy atlas is not itself the needed history-uniform theorem.

## Separating counterexamples

Four failures must remain visible. First, reconstruction can preserve one Wilson loop while corrupting another; agreement on a finite probe family does not imply algebra recovery. Second, a map can be gauge invariant but collapse physically distinct orbits, giving perfect gauge-copy erasure and unacceptable observable loss. Third, a gauge-fixed reconstruction can recover invariant observables yet retain arbitrary copy labels, so recovery does not imply erasure. Fourth, every finite-volume error can vanish while the supremum over volumes or blocking depth stays positive; this defeats the uniform continuum statement. A fifth warning comes from H9: recovery of a sparse observable core does not establish density, so spectral or Hilbert-space conclusions remain unavailable.

## Next theorem

The decisive next result is a one-block observable-recovery theorem for a real regulated Yang--Mills block map. It should specify the fine and retained gauge actions, an explicit reconstruction rule, a separating gauge-invariant observable class, and a normed error functional. It must prove: exact covariance or quotient-level gauge-copy erasure; a quantitative (E_{a,O}^{(p)}) bound for every observable in the declared class; uniformity in volume, boundary condition, and positive-mass retained history; and a one-step composition estimate stable under iteration. The first target may be finite and C1, but its constants must be organized for a later cutoff limit.

## C1/C3 guardrails

At C1, one may claim a typed finite-lattice quotient/reconstruction theorem, explicit observable errors, and verified composition constants. One may not infer an OS Hilbert-space isometry, density of the recovered observable core, a physical mass gap, continuum measure existence, or equality of continuum Yang--Mills theories. Those require the H9 density and temporal bridge, H2 uniform physical-length decay, and the broader normalized retained-kernel program. H10 is a necessary representational control layer, not a standalone C3 bridge.
