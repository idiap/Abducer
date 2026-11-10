# H2 independent stream: physical-length Lyapunov rigidity

## Executive conclusion

H2 survives, but only in a sharper form.  A positive mass cannot be identified
with contraction per RG label, with pointwise strict contraction, or with the
Lyapunov exponent of an arbitrarily normalized representation cocycle.  The
defensible statement is:

> A positive mass is a positive, cutoff-uniform Lyapunov rate per unit physical
> length of a cocycle that acts on a complete centered physical observable
> core, is connected to reflection-positive temporal correlations, and is
> invariant under all admissible changes of representation up to tempered
> endpoint distortion.

Stage 57 proves the finite positive-kernel composition law and states the
correct physical-length criterion.  Stage 58 proves that this law alone does
not constrain an independently chosen temporal transfer gap.  The new point
of the H2 stream is to expose the remaining **coboundary ambiguity**: changing
the weights or norms at successive descriptive scales can manufacture a
Lyapunov exponent unless the endpoint distortion is sublinear in accumulated
physical length.  This makes tempered representation transport, not merely a
product of numbers below one, part of the hypothesis.

The present claim ceiling is C2 for the finite cocycle and its countermodels,
with a C3 conditional OS handoff.  There is no constructed physical
Yang--Mills cocycle, no continuum theory, and no Hamiltonian mass-gap result.

## 1. Frozen hypothesis

Let \(\alpha=(a,\Lambda,g,\ldots)\) denote regulator, finite volume, bare
parameters, and any other construction data.  At stage \(n\), let
\(\mathcal B^0_{\alpha,n}\) be a centered or vacuum-quotiented observable
space, let

\[
 \mathcal R_{\alpha,n}:\mathcal B^0_{\alpha,n+1}
     \longrightarrow \mathcal B^0_{\alpha,n}
\]

be the backwards representation or defect-transport map, and attach a
positive physical increment \(\ell_{\alpha,n}\).  Write

\[
 L_{\alpha,N}=\sum_{n=0}^{N-1}\ell_{\alpha,n},\qquad
 \mathcal R_{\alpha,0:N}
 =\mathcal R_{\alpha,0}\cdots\mathcal R_{\alpha,N-1}.
\]

The candidate exponent is

\[
 m_{\mathrm{Lyap}}
 =\liminf_{L_{\alpha,N}\to\infty}
   -\frac{1}{L_{\alpha,N}}
    \log\left\|\mathcal R_{\alpha,0:N}
       \big|_{\mathcal B^0_{\alpha,N}}\right\|.
\]

For H2 to be physical, the lower bound on this quantity must be uniform in
\(a\), \(\Lambda\), admissible retained histories, and the chosen
representation chart.  The spaces must map to a dense centered core of the
OS-reconstructed theory.  None of those physical identifications is supplied
by the definition.

The liminf is intentional.  A limit need not exist for a nonstationary,
changing-state-space cocycle.  Additional subadditivity or stationarity may
later upgrade it to a limit.

## 2. Strongest finite theorem currently available

### Theorem H2-F: robust weighted physical-length composition

Let \(S_0,\ldots,S_N\) be finite state spaces, let
\(Q_n:S_n\to S_{n+1}\) be positive sub-Markov kernels, and let
\(V_n:S_n\to[1,\infty)\).  Suppose that for numbers \(m_0>0\),
\(\ell_n>0\), and real multiplicative defects \(\epsilon_n\),

\[
 Q_nV_{n+1}
 \leq \exp(-m_0\ell_n+\epsilon_n)V_n
 \quad\text{pointwise on }S_n.
\tag{H2.1}
\]

For every probability root law \(\nu_0\), positivity and \(V_N\geq1\) give

\[
 \nu_0 Q_0Q_1\cdots Q_{N-1}\mathbf1
 \leq \nu_0(V_0)
 \exp\left[-m_0L_N+E_N\right],
\quad
 E_N=\sum_{n<N}\epsilon_n.
\tag{H2.2}
\]

Consequently, if constants \(C<\infty\) and \(0\leq\theta<1\) satisfy

\[
 \log\nu_0(V_0)+E_N
 \leq C+\theta m_0L_N
\tag{H2.3}
\]

uniformly over the declared regulator family, then

\[
 \nu_0 Q_{0:N}\mathbf1
 \leq e^C e^{-(1-\theta)m_0L_N}.
\tag{H2.4}
\]

The proof is exact induction: apply positivity to (H2.1) at every step and
retain the root moment.  This extends the Stage 57 statement by recording the
only multiplicative error budget compatible with a positive physical rate.
It remains a finite positive-kernel theorem.  In particular, it does not say
that \(Q_n\) is a Yang--Mills kernel or that its surviving mass bounds a
temporal correlation.

### Corollary H2-R: rate criterion

For a fixed positive chain, a positive liminf physical rate is equivalent to
the following: for every \(m\) strictly below that rate, there is a finite
\(C\) such that

\[
 \prod_{n<N}q_n\leq C e^{-mL_N}
\tag{H2.5}
\]

for all \(N\), up to a harmless finite initial segment.  For a regulator
family, uniformity of \(C\) and of the onset is an additional hypothesis; it
does not follow from a separate positive liminf at each cutoff.  Merely having
\(q_n<1\), or even \(q_n\leq q<1\), does not imply (H2.5) when one RG step can
represent an increasing physical distance.

## 3. Representation-gauge theorem

The exponent of a changing representation is not meaningful until the
normalization freedom is controlled.  If

\[
 \widetilde V_n=c_nV_n,\qquad c_n>0,
\]

then a step ceiling \(q_n\) transforms to

\[
 \widetilde q_n=q_n\frac{c_{n+1}}{c_n},
 \qquad
 \prod_{n<N}\widetilde q_n
 =\left(\prod_{n<N}q_n\right)\frac{c_N}{c_0}.
\tag{H2.6}
\]

Hence the finite-length rate transforms as

\[
 \widetilde m_N
 =m_N-\frac{\log c_N-\log c_0}{L_N}.
\tag{H2.7}
\]

For a weight bound that also uses \(V_N\geq1\), an admissible rescaling must
preserve the terminal domination or retain its endpoint factor explicitly.
The exponent is invariant under such a change only if

\[
 \frac{|\log c_N|+|\log c_0|}{L_N}\longrightarrow0
\tag{H2.8}
\]

uniformly along the continuum/volume family.  The same conclusion holds for
two families of norms whose endpoint equivalence constants have sublinear
logarithms.  Condition (H2.8) is the **tempered representation condition**.
It is the minimal coherence requirement preventing descriptive normalization
from creating or erasing a physical mass.

This is an elementary coboundary calculation, not a claimed novel theorem.
Its importance here is diagnostic: Stage 57's root moment and the endpoint
weight cannot be treated as prefactors unless their logarithms are
sublinear in physical length, uniformly in the cutoff.

## 4. Decisive countermodels

### CM1: strict contraction with zero rate

Take \(\ell_n=1\) and \(q_n=\exp[-1/(n+1)]\).  Every step contracts strictly,
but

\[
 -\frac1N\log\prod_{n<N}q_n
 =\frac1N\sum_{k=1}^{N}\frac1k\longrightarrow0.
\]

Pointwise strictness is insufficient.

### CM2: uniform contraction per geometric RG level

Take \(q_n=q<1\) and \(\ell_n=b^n\), \(b>1\).  Then

\[
 m_N=\frac{N(-\log q)}{(b^N-1)/(b-1)}\longrightarrow0,
\qquad
 q^N=R_N^{-\gamma},\quad
 \gamma=-\frac{\log q}{\log b}.
\]

This is power-law suppression in the terminal scale, not exponential decay
in physical distance.

### CM3: a fake exponent from representation rescaling

Let the physical transport be the identity on a one-dimensional space.  On a
finite horizon choose positive weights

\[
 V_n=e^{m(L_N-L_n)}.
\]

For the identity kernel, \(Q_nV_{n+1}=e^{-m\ell_n}V_n\), so its weighted
product appears to have mass \(m\).  The root moment is
\(V_0=e^{mL_N}\) and cancels the entire contraction.  The operator-norm
analogue uses \(\|x\|_n=e^{mL_n}|x|\): the backwards identity has norm
\(e^{-m\ell_n}\), while the endpoint norm distortion is \(e^{mL_N}\).
A Lyapunov exponent without (H2.8) is therefore a coordinate artifact.

### CM4: positive regulated gaps with zero continuum mass

At time spacing \(a\), choose a positive symmetric transfer matrix whose
nontrivial eigenvalue ratio is \(e^{-a^2}\).  Every cutoff theory has a
positive transfer gap, but the physical gap is

\[
 -a^{-1}\log(e^{-a^2})=a\longrightarrow0.
\]

Cutoff uniformity in physical units is indispensable.

### CM5: an auxiliary cocycle does not determine temporal spectrum

Keep the Stage 53/57 weighted defect ceiling fixed at
\(0.002430277501841998\).  Independently choose the positive symmetric
temporal transfer matrix with eigenvalues \(1\) and \(e^{-\varepsilon}\).
Its temporal gap is \(\varepsilon\), which can approach zero without changing
the defect ceiling.  Therefore a comparison theorem between defect survival
and centered temporal correlations is logically necessary.

### CM6: an incomplete observable core hides a low mode

A Hamiltonian with spectrum \(\{0,0.4,1.2\}\) can look gapped by \(1.2\) on a
core that sees only the last mode.  Decay on a retained observable class gives
a full gap only after that class is dense in the vacuum complement.

Together these countermodels falsify six tempting shortcuts: strictness,
per-level uniformity, normalization-dependent exponents, finite-cutoff gaps,
auxiliary mixing, and sectorially incomplete decay.

## 5. The exact next physical inequality

The next H2-specific target should not assume a Hamiltonian gap or continuum
clustering.  For the **independently constructed and normalized** physical
retained-state/disagreement kernels
\(Q^{a,\Lambda,h}_n\), prove that there are constants
\(m_0>0\), \(C<\infty\), and \(0\leq\theta<1\), independent of cutoff,
volume, admissible positive-mass history \(h\), and chain length, such that

\[
 Q^{a,\Lambda,h}_nV^{a,\Lambda,h}_{n+1}
 \leq
 e^{-m_0\ell^{a,h}_n+\epsilon^{a,\Lambda,h}_n}
 V^{a,\Lambda,h}_n,
\tag{H2-P1}
\]

and

\[
 \log\nu^{a,\Lambda,h}_0(V^{a,\Lambda,h}_0)
 +\sum_{n<N}\epsilon^{a,\Lambda,h}_n
 \leq C+\theta m_0
       \sum_{n<N}\ell^{a,h}_n.
\tag{H2-P2}
\]

The physical increments must be defined from actual Euclidean separation,
not from the number of descriptive RG levels.  Admissible changes of
retained representation must satisfy the tempered endpoint condition
(H2.8).

Equations (H2-P1)--(H2-P2) imply a uniform positive rate
\(m_*=(1-\theta)m_0\) for the declared defect cocycle.  They do **not** yet
imply a Hamiltonian gap.  The second, logically independent target is an
observable domination theorem of the form

\[
 \left|
  \langle F,\tau_{L_N}G\rangle_{a,\Lambda}^{\mathrm{conn}}
 \right|
 \leq C_{F,G}
 \sup_h\nu^{a,\Lambda,h}_0
 Q^{a,\Lambda,h}_{0:N}\mathbf1
 +\delta_{a,\Lambda,N}(F,G),
\tag{H2-P3}
\]

where \(F,G\) range over a gauge-invariant temporal core, the prefactors are
uniform for each fixed local pair, and

\[
 \limsup
 \frac{1}{L_N}\log
 \delta_{a,\Lambda,N}(F,G)<-m_*
\tag{H2-P4}
\]

uniformly in the limit order used.  P3 is where OS compatibility, locality,
support growth, and observable completeness enter.  Calling \(Q\) a
"physical cocycle" before proving P3 would be an unsupported identification.

## 6. Conditional OS spectral handoff

Suppose a nontrivial continuum theory satisfying the required OS axioms has
already been constructed and identified as pure Yang--Mills.  Let \(H\geq0\)
be its reconstructed Hamiltonian, \(\Omega\) its vacuum, and
\(\mathcal D\subset\Omega^\perp\) a dense set generated by the temporal
observable core.  If for every \(\psi\in\mathcal D\),

\[
 \langle\psi,e^{-tH}\psi\rangle
 \leq C_\psi e^{-m_*t}\qquad(t\geq0),
\tag{H2-OS}
\]

then the spectral measure of every \(\psi\in\mathcal D\) has no support below
\(m_*\).  Density and boundedness of spectral projections then give

\[
 \operatorname{spec}(H)\cap(0,m_*)=\varnothing.
\]

This is a conditional spectral-measure argument.  The package has not proved
the premises: a continuum OS Yang--Mills theory, P3 for a dense core, and
uniform passage of the exponential estimate through the limits.

## 7. Parameter and limit ledger

| Quantity | Required quantifier | Current status |
|---|---|---|
| lattice spacing \(a\) | all sufficiently small \(a\), uniform constants | open |
| volume \(\Lambda\) | all volumes or thermodynamic family, uniform constants | open |
| history \(h\) | every admissible retained boundary history | open |
| physical increments \(\ell_n\) | positive and tied to Euclidean separation | abstractly defined only |
| weight/root moment | uniform or subexponential logarithm | finite criterion only |
| defects \(\epsilon_n\) | cumulative budget below \(m_0L_N\) | criterion only |
| representation change | tempered endpoint distortion | newly isolated condition; unproved physically |
| observable support | controlled under pullback | open |
| temporal core | gauge invariant and dense after reconstruction | open |
| reflection positivity | preserved by the relevant temporal construction | open |
| limit order | volume, cutoff, reconstruction, density | specified; no interchange theorem |
| gauge groups | every compact simple group for Clay target | not addressed by H2 stream |

## 8. Pass/fail audit

| Gate | Verdict | Reason |
|---|---|---|
| finite changing-state-space composition | pass, C2 | exact positivity induction in Stage 57 |
| physical-length normalization | pass as definition | no physical increments constructed |
| multiplicative-error budget | pass as finite theorem | follows from exact composition |
| invariance under tempered scalar renormalization | pass as algebraic theorem | endpoint coboundary cancels |
| actual nonlinear Yang--Mills kernel | fail/open | upstream normalized kernel remains unconstructed |
| cutoff-/volume-/history-uniform P1--P2 | fail/open | first H2 physical inequality |
| observable domination P3 | fail/open | defect cocycle and temporal transfer remain independent |
| reflection-positive temporal preservation | fail/open | not supplied by finite kernel algebra |
| dense observable core | fail/open | hidden-sector countermodel applies |
| continuum OS pure Yang--Mills identity | fail/open | construction and universality absent |
| Hamiltonian mass gap | fail/open | conditional handoff premises absent |

## 9. Strategy and reward assessment

The highest-value H2 work is not another scalar product calculation.  It is a
small reflection-positive calibration in which the physical time direction,
the disagreement kernel, and the observable correlation are derived from the
same measure.  Such a model can test P3 without pretending to solve the
nonlinear four-dimensional problem.  If P3 fails even there, H2 needs a
different carrier than bad-chain survival.  If it succeeds, the exact
comparison constants reveal what the nonlinear Yang--Mills construction must
control.

The next reward point is therefore a **same-measure OS comparison theorem**,
not a stronger abstract Lyapunov definition.  The physical SU(2) inequality
P1--P2 remains upstream-dependent on the H1/H4/H5/H8 retained-kernel
programme, but the reflection-positive calibration and the representation-
gauge theorem can proceed independently.

## 10. Claim language

Permitted:

- “The finite weighted cocycle has an exact physical-length criterion.”
- “The exponent is invariant under representation rescalings with tempered
  endpoint distortion.”
- “A uniform physical inequality plus observable domination would imply
  temporal exponential decay.”
- “Dense-core OS decay conditionally implies a Hamiltonian gap.”

Not permitted:

- “The Stage 53 ceiling is a Yang--Mills mass.”
- “Contraction at every RG level gives exponential physical clustering.”
- “The Perron/Lyapunov norm is automatically physical.”
- “A finite-cutoff transfer gap survives the continuum limit.”
- “Decay on a selected observable sector proves the full mass gap.”
- “H2 proves or nearly proves the Clay problem.”
