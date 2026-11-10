# Independent addendum: Stages 76--77 (H9 and H10)

## Verdict

Stage 76 is a **qualified pass at C2**.  Its finite spectral theorem is
correct: the time-translation closure of a probe space is the direct sum of
its visible components in each eigenspace, full density requires every
multiplicity direction, and a norm-compatible decay bound on a dense core
extends to the full vacuum-orthogonal Hilbert space.  The implementation uses
floating-point eigendecomposition, so its numerical output is a
tolerance-certified calibration rather than an exact machine proof.

Stage 77 is a **pass at C2**.  On the fixed two-vertex, three-edge
\(\mathbb Z_2\) graph, the orbit quotient, reconstruction section, complete
rational invariant algebra, counterexamples, and composition estimates are
computed with exact signs and rational arithmetic.  The result is complete
for that finite declared model and no larger one.

The 20 Stage 76 tests and 23 Stage 77 tests pass.  Both stored result files
agree with fresh execution; all four result/dependency JSON files parse.
Stage 77's exhaustive check covers

\[
  256^2\cdot 4=262{,}144
\]

ordered map-pair--basis-observable instances and has minimum slack zero.

## Stage 76: theorem, implementation, and repair

Let \(H=H^\ast\geq0\), let \(\Omega\) be a normalized zero-energy vector,
let \(D\subseteq\Omega^\perp\) be the centered probe space, and let
\(P_\lambda\) denote the spectral projections of
\(H|_{\Omega^\perp}\).  In finite dimension,

\[
 K(D)=\operatorname{span}\{e^{-tH}D:t\geq0\}
     =\bigoplus_\lambda \operatorname{ran}(P_\lambda|_D).
\]

The equality follows by finite interpolation of the distinct functions
\(e^{-t\lambda}\).  Since \(H\) is scalar on each eigenspace, \(K(D)\) is
reducing.  Therefore

\[
 \dim K(D)=\sum_\lambda\operatorname{rank}(P_\lambda|_D),
 \qquad
 m_{\mathrm{vis}}=min\{\lambda:P_\lambda D\neq0\}.
\]

These are exactly the quantities computed by the code.  The hidden-mode
fixture correctly returns \(m_{\mathrm{vis}}=1.2\) while the full gap is
\(0.4\), and the multiplicity fixture correctly shows that seeing the value
\(0.4\) is insufficient when part of its eigenspace remains invisible.

For a dense linear core \(C\), continuity of the bounded bilinear form gives

\[
 |\langle x,e^{-tH}y\rangle|
 \leq e^{-mt}\|x\|\|y\|
 \quad (x,y\in C)
 \Longrightarrow
 \|e^{-tH}|_{\Omega^\perp}\|\leq e^{-mt}.
\]

In finite dimension, the latter is equivalent to
\(m\leq\min\operatorname{spec}(H|_{\Omega^\perp})\).

One executable defect was found and repaired.  Previously, the sampled
bilinear checker could accept any candidate rate when the only requested
sample was \(t=0\), because both sides equal one there.  The pass condition
now also checks the analytically decisive inequality
\(m\leq m_{\mathrm{vis}}\) (and, for the full space,
\(m\leq m_{\mathrm{true}}\)).  A hostile regression test uses candidate
mass nine and the sample set \(\{0\}\); it is now rejected.  The canonical
Stage 76 results are unchanged by the repair.

Two qualifications remain:

1. Eigenvalues, eigenspace grouping, and ranks are determined numerically
   with a declared tolerance.  The analytic theorem is exact, but the
   executable certificate is not exact arithmetic.
2. The field `state_separating` is an operational finite-Hilbert-space alias
   for \(K(D)=\Omega^\perp\).  It does not prove that a continuum observable
   algebra separates states before or after the OS null-space quotient.

## Stage 77: exact quotient and observable recovery

The effective gauge action sends

\[
 (e_0,e_1,e_2)\longmapsto s(e_0,e_1,e_2),\qquad s\in\{\pm1\},
\]

because the diagonal subgroup of \(\mathbb Z_2^2\) is the action kernel.
Thus every effective orbit has two points.  The pair

\[
 B(e_0,e_1,e_2)=(e_0e_1,e_1e_2)
\]

is constant on orbits and has four fibres, exactly the four orbits.  The
section

\[
 R(y_1,y_2)=(1,y_1,y_1y_2)
\]

satisfies \(B R=\mathrm{id}\), while \(RBx\) is gauge-equivalent to \(x\).
The code enumerates every fine configuration and gauge element, so the
quotient and erasure claims match the theorem exactly.

The four characters

\[
 1,\quad W_{01},\quad W_{12},\quad W_{01}W_{12}=W_{02}
\]

form the \(4\times4\) Hadamard character table.  Its exact rational rank is
four; hence it is a basis for all \(\mathbb Q\)-valued functions on the
four-point quotient.  Product closure and coefficient-\(\ell^1\)
submultiplicativity are correctly implemented.

For any function \(O:Y\to\mathbb Q\) and endomaps \(f,g:Y\to Y\),

\[
 e_O(g\circ f)
 \leq e_O(f)+e_O(g),
 \qquad
 e_O(f)=\max_y|O(f(y))-O(y)|,
\]

because the first increment is evaluated at \(f(y)\in Y\).  This theorem is
analytic for every declared observable.  The exhaustive computation checks
the four basis functions, while the rational equality fixture checks a
non-basis linear combination.  The distinction is accurately stated: the
enumeration supports the theorem but is not its proof.

The three countermodels are also logically sound:

- a constant invariant block erases gauge copies but destroys physical
  labels;
- retaining an explicit gauge-copy sign recovers all invariants but does not
  erase the copy;
- preserving the nonseparating family \(\{1,W_{01}\}\) leaves errors of two
  on \(W_{12}\) and \(W_{02}\).

No local code correction was required in Stage 77.

## Cross-consistency with Stage 68

There is no contradiction and, more importantly, no completed bridge.
Stage 68 proves with one temporal measure that a masked bad-channel ceiling
can tend to zero while the full temporal gap also tends to zero.  Stage 76
does not negate this obstruction: it proves a gap only after a dense temporal
core is shown to obey a uniform physical-time decay estimate.  It does not
show that the Stage 68 bad mask controls that core.  Its hidden \(0.4\) mode
is a direct finite analogue of the same missing-observability problem.

Stage 77 supplies neither a temporal transfer operator nor a measure.  Exact
recovery on its finite orbit quotient therefore cannot imply spectral
coercivity.  Its incomplete-probe counterexample reinforces the same warning
at the representational level: agreement on selected probes need not see all
physical directions.  Finite quotient separation must not be promoted to
density in the OS physical norm.

The valid combined implication is only conditional:

```text
exact finite quotient/recovery (H10)
  + regulator-to-continuum identification of the same observables [open]
  + OS-norm temporal density, including multiplicities [open]
  + uniform decay in physical time on that dense core [open]
  -> reconstructed spectral gap (H9 analytic bridge)
```

The Stage 68 obstruction adds a further required input: if decay is inferred
from selected rare defects, one needs a same-measure observability or
coercivity inequality proving that those defects see every nonvacuum temporal
mode.

## Claim and frontier ledger

| Implication | Status |
|---|---|
| H9 finite spectral closure/rank theorem | proved analytically; numerically calibrated |
| H9 dense-core decay to finite spectral gap | proved conditionally on the dense-core bound |
| H10 exact finite \(\mathbb Z_2\) orbit quotient and recovery | proved exactly |
| H10 same-space two-step defect inequality | proved exactly |
| link from Stage 68 bad mask to H9 dense temporal core | open |
| nonlinear normalized SU(2) retained-state map | open |
| changing-lattice observable composition with uniform constants | open |
| continuum observable identity and OS-norm density | open |
| uniform physical-time decay | open |
| OS reconstruction and Yang--Mills theory identity | open |
| Yang--Mills mass gap | not claimed |

The best next joint target is a typed regulator-level diagram connecting one
normalized nonlinear SU(2) retained kernel, a separating temporal observable
class, and its reconstructed OS vectors.  It must include two quantitative
estimates: uniform observable-recovery error under changing scales and a
same-measure coercivity/Gram lower bound that prevents invisible temporal
modes.  Without both, H9 and H10 remain correct but disconnected finite
modules.
