# H3 stream report: collective repair and a polymer boundary law

## Executive conclusion

H3 is a viable independent research stream, but its current positive evidence
is a finite linear-algebra signal rather than a boundary-law theorem.  The
orientation-correct one-star problem is exactly understood and is strictly
anti-local: every nonzero centered one-star displacement exports curvature.
On the same open side-two four-cube, coordinated four- and eight-link systems
instead exhibit, numerically, four and seven zero-spill directions.  This is
the first evidence that compatibility between neighboring stars can repair
the one-star obstruction.

The signal is not yet the desired result.  It establishes neither that the
nullspace grows extensively on polymers, nor that the nonzero spill is carried
only by the polymer boundary, nor that the zero-spill sector covers the bad
directions that a repair must contract.  It also does not construct a
nonlinear, gauge-covariant, injective change of variables with a controlled
Jacobian.  The H3 claim therefore remains **C1**, using a **C2 exact one-star
obstruction** as its foundation.

The highest-reward next theorem is an orientation-correct relative-Hodge
factorization of the multi-star spill form on a growing polymer family.  In a
strong form it would show that all spill is determined by boundary trace data;
in a weaker but still useful form it would show that the number and total cost
of nonzero spill modes are boundary-sized, with quantitative coverage of the
bad-event displacement.

## 1. Frozen formulation

Let \(K\) be a finite oriented cubical two-complex, let
\(d_1:C^1(K;\mathbb R)\to C^2(K;\mathbb R)\) be its link-to-plaquette
coboundary, and let \(P\) be a connected set of rooted links.  For every
\(\ell\in P\), let \(S_\ell\) select the six incident plaquettes, let
\(O_\ell\) put them into the common rooted-link orientation, and let
\(C_6=I-\frac16\mathbf1\mathbf1^{\mathsf T}\) remove the common mode.  Define

\[
 R_P=\bigoplus_{\ell\in P} C_6O_\ell S_\ell d_1.
\]

Let \(U(P)\) be the union of the selected incident plaquettes and let
\(B_P=E_{U(P)^c}d_1\) record curvature outside that union.  For realizable
stacked star data \(y\in\operatorname{im}R_P\), define

\[
 h_P(y)=\inf_{R_Px=y}\|B_Px\|_2^2.
\]

This is a positive-semidefinite quadratic form.  Its kernel is exactly

\[
 \ker h_P=R_P(\ker B_P),
\]

and therefore

\[
 \dim\ker h_P
 =\operatorname{rank}\!\begin{pmatrix}R_P\\B_P\end{pmatrix}
  -\operatorname{rank}B_P.
\]

The rank identity is exact over \(\mathbb Q\) once the oriented incidence
matrices are frozen.  It is the preferred certificate for zero modes; a small
floating eigenvalue is not a proof of a kernel.

### Precise H3

There should exist a growing class of regular connected polymers \(P\), a
boundary trace space \(T_{\partial P}\), and uniformly controlled maps such
that the spill form factors through the boundary, exactly or up to a
quantified remainder:

\[
 h_P(y)\le C_{\partial}\|T_{\partial P}y\|^2
          +\varepsilon_P\|y\|^2,
 \qquad \varepsilon_P\longrightarrow0.
\]

For repair-relevant data with bulk amplitude \(d_P(y)^2\), the operational
version is

\[
 h_P(\delta y)\le
 C_{\partial}|\partial P|d_P(y)^2,
 \qquad
 \text{internal action drop}\ge
 c_{\mathrm{bulk}}|P|d_P(y)^2.
\]

This is the boundary-law statement that would make coordinated repair useful:
bulk gain must dominate boundary spill, volume-extensive entropy losses, and
polymer counting.  The statement must specify which subspace of bad data is
repaired.  A result merely asserting that \(\ker h_P\ne0\) is much weaker.

## 2. Strongest established results

### 2.1 Exact one-star obstruction

The orientation-correct Paper 05 certificate proves, for every one of the
eight interior links of the open side-two four-cube,

\[
 \operatorname{spec}(h_{\{\ell\}})=
 \left\{
   \left(\frac{37}{33}\right)^{\!\times3},
   \left(\frac{391}{239}\right)^{\!\times2}
 \right\}.
\]

The spectrum is exact, relative to the centered-coordinate metric
\(G=I+\mathbf1\mathbf1^{\mathsf T}\), and was proved by rational KKT
substitution and an exact generalized characteristic polynomial.  Hence

\[
 h_{\{\ell\}}(y)\ge\frac{37}{33}\|y\|^2
 \quad\text{for all nonzero centered one-star data }y.
\]

This is the strongest exact result directly relevant to H3.  It rules out
zero-spill single-star smoothing and makes collective support necessary.

### 2.2 Exact conditional free-energy frontier

For contraction \(a\), bad-event quadratic scale \(D_0\), heat time \(t\),
spill coefficient \(\lambda\), fixed losses \(J\), and desired gain \(F_*\),
Stage 45 proves the algebraic sufficient condition

\[
 \lambda<
 \frac{(1-a^2)-\frac{2t}{D_0}
  \bigl(15\log(1/a)+J+F_*\bigr)}{(1-a)^2}.
\]

At the upper calibrated split, the admissible value is
\(0.9683231479404556\).  The orientation-correct worst one-star eigenvalue is
still \(391/239=1.635983263598\ldots\), so the earlier numerical worst-mode
comparison survives the orientation correction: a coordinated construction
must reduce the effective worst coefficient by at least the recorded factor
\(0.5918906198409593\) in that frozen budget.  This is a design criterion,
not a constructed repair and not a measure estimate.

### 2.3 Multi-star signal

The current oriented floating-point probe gives:

| Polymer | \(\operatorname{rank}R_P\) | numerical zero modes | positive spectral groups |
|---|---:|---:|---|
| one star | 5 | 0 | \((37/33)^{\times3},(391/239)^{\times2}\) |
| adjacent pair | 10 | 0 | candidates \((16/19)^{\times3},(5/4)^{\times2},(3/2)^{\times3},(24/11)^{\times2}\) |
| central four directions | 18 | 4 | four numerical positive groups; not rationally certified |
| all eight interior links | 24 | 7 | candidates \((3/4)^{\times6},(12/11)^{\times8},(10/7)^{\times3}\) |

Only the one-star row currently has a complete exact certificate.  The
fractions displayed for the pair and eight-link systems are rational
reconstructions of numerical eigenvalues, not proofs.  The correct exact
target is a rational KKT cost matrix and a generalized characteristic
polynomial over \(\mathbb Q\); its roots need not themselves be rational.

The four- and eight-link nullities demonstrate a plausible collective
mechanism.  They do **not** imply a boundary law because:

1. the systems do not form a growing polymer sequence;
2. nullity has not been certified by exact ranks;
3. a null vector may fail to overlap the displacement needed to repair the
   bad event;
4. curvature may simply have been moved into \(U(P)\), where its internal
   action must still be charged;
5. no nonlinear link transformation or Jacobian is present.

## 3. Material orientation risk

The order of operations is theorem-critical:

\[
 \boxed{R_\ell=C_6O_\ell S_\ell d_1}.
\]

Centering raw signed plaquette rows and orienting afterward uses
\(O_\ell C_6S_\ell d_1\), which is not the same operator because
\([C_6,O_\ell]\ne0\).  The superseded Stage 44 convention generated one
spurious zero-spill one-star direction.  The exact Paper 05 audit removed it.

This risk becomes more severe for polymers because one plaquette can belong
to several rooted stars with different induced signs.  A multi-star
certificate must therefore carry, for every row occurrence, the tuple

\[
 (\text{plaquette orientation},\text{root link},\text{incidence sign},
  \text{centering fiber}).
\]

Required orientation tests are:

- invariance under simultaneous reorientation of a link or plaquette basis;
- covariance under oriented cubical automorphisms;
- equality between explicit transport-to-root conventions and the matrix
  incidence convention;
- a hostile comparison against `orient-then-center`, `center-then-orient`,
  and sign-erased implementations;
- reproduction of the exact one-star spectrum as a mandatory regression
  test for every growing-complex implementation.

No result derived from the old zero-mode convention may be imported into H3.
The Stage 45 worst coefficient happens to agree with the corrected maximum,
but that numerical agreement must not be used to validate the old operator.

## 4. The growing-polymer spectral target

### 4.1 Geometry families

Use open and periodic four-dimensional cubical complexes with several
polymer families:

- straight link chains;
- rectangular link boxes and slabs;
- compact approximately cubical polymers with
  \(|\partial P|/|P|\to0\);
- branched and thin adversarial polymers with large boundary-to-volume ratio;
- polymers touching the ambient boundary;
- periodic winding polymers that test harmonic and flux sectors.

Results from compact polymers cannot be generalized to arbitrary connected
sets without a shape or isoperimetric hypothesis.

### 4.2 Exact spectral ledger

For every \(P\), compute or prove:

\[
 r_P=\operatorname{rank}R_P,
 \quad z_P=\dim\ker h_P,
 \quad r_P-z_P,
 \quad \lambda_{\min}^+(P),
 \quad \lambda_{\max}(P),
 \quad \operatorname{tr}h_P,
\]

with all eigenvalues understood relative to the induced metric on
\(\operatorname{im}R_P\).  Also record \(|P|\), \(|U(P)|\), the declared
\(|\partial P|\), topology, and ambient-boundary contact.

The most informative candidate signatures are

\[
 r_P-z_P=O(|\partial P|)
 \quad\text{and}\quad
 h_P=T_{\partial P}^{\mathsf T}K_PT_{\partial P}+E_P,
 \qquad \|E_P\|\to0.
\]

The first says that only boundary-many modes spill; the second identifies the
boundary data that control their cost.  Neither follows from a growing
zero-mode count alone.

### 4.3 Coverage is part of the theorem

Let \(Y_P^{\mathrm{bad}}\subset\operatorname{im}R_P\) be the displacement
cone generated by the declared bad event, and let \(N_P=\ker h_P\).  Compute
the principal-angle or projection constant

\[
 \theta_P=inf_{y\in Y_P^{\mathrm{bad}}\setminus\{0\}}
 \frac{\|\Pi_{N_P}y\|^2}{\|y\|^2}.
\]

If \(\theta_P\to0\), a large nullspace is irrelevant to repair.  A useful
result needs either \(\inf_P\theta_P>0\), a controlled decomposition of every
bad displacement into zero-spill and boundary-charged pieces, or a different
event definition whose energetic gain is preserved under the projection.

## 5. What a boundary-law repair theorem must contain

A publishable linear theorem should provide all of the following.

1. **Typed cochain complex.**  Exact orientations, open/periodic boundary
   conditions, quotient by gauge directions, and the metric on duplicated
   rooted-star data.
2. **Relative-Hodge identification.**  Characterize
   \(\operatorname{im}d_1\cap C^2(U(P))\), harmonic obstructions, and the
   quotient that is seen by \(R_P\).
3. **Controlled right inverse.**  Construct \(J_P\) on the repair subspace
   with \(R_PJ_Py=\delta y\) and a boundary-trace estimate for \(B_PJ_Py\).
4. **Coverage.**  Prove that \(\delta y\) contracts a fixed fraction of the
   actual dispersion defect, not an opportunistically selected null mode.
5. **Complete quadratic energy.**  Charge selected, internal-unselected, and
   external plaquettes, including cross terms with the pre-existing field.
6. **Entropy balance.**  Compute the determinant on the true independent link
   fiber.  Duplicated star coordinates cannot be assigned independent
   Jacobians.
7. **Polymer entropy.**  Establish a net gain
   \(\gamma|P|-C_{\partial}|\partial P|-C_0\) large enough to beat the number
   of connected polymers at the declared graph degree.

A Yang--Mills-facing nonlinear theorem additionally requires:

8. a finite \(SU(2)\) link map, not only its tangent derivative;
9. gauge covariance and compatibility with reflection planes;
10. injectivity or controlled multiplicity and the full Haar/Jacobian ratio;
11. chart, cut-locus, center, orbit, and integer-topology channels;
12. uniformity over every positive-mass retained boundary history;
13. constants uniform in volume and cutoff in physical units;
14. normalized conditional partition-function comparison.

These items are prerequisites for inserting H3 into the retained-state kernel
programme.  They are not consequences of a finite spectral computation.

## 6. Mandatory falsification gates

| Gate | Test | Failure means |
|---|---|---|
| Orientation | Reproduce the exact one-star spectrum after all basis reorientations | The multi-star operator is mistyped; stop |
| Exact zero | Certify nullity using rational ranks and exact KKT substitution | Numerical zero modes are only conjectural |
| Support accounting | Recompute total curvature change on every plaquette, including \(U(P)\) | “Zero spill” may only hide internal action |
| Coverage | Compute principal angles between \(\ker h_P\) and bad displacements | Nullspace cannot repair the declared event |
| Boundary trace | Search for modes with small boundary trace but order-one spill | The proposed boundary factorization is false |
| Scaling | Test compact, thin, branched, boundary-touching, and periodic families | Any theorem must narrow its polymer class |
| Gauge/topology | Separate exact, gauge, harmonic, center-flux, and winding modes | Zero modes may be redundancy or forbidden sector changes |
| External history | Test adverse pre-existing external curvature and cross terms | Vacuum-background energy accounting is insufficient |
| Jacobian | Differentiate the actual link map and audit rank/multiplicity | Coordinate entropy budget is invalid |
| Nonlinearity | Compare tangent predictions with finite \(SU(2)\) updates up to chart edge | Linear repair does not lift uniformly |
| Entropy threshold | Include polymer counting and all logarithmic losses | Boundary scaling alone does not suppress clusters |
| Limit audit | Vary ambient volume, polymer size, heat time, and lattice spacing | A fixed-block result cannot enter a continuum chain |

The stream stops or changes hypothesis at the first failed gate.  In
particular, if the exact nonzero-spill rank is volume-sized for compact
Følner polymers, the strong boundary-factorization form of H3 is falsified.
If nullspaces grow but the coverage constants vanish, H3 may survive only as
a special-channel repair, not as a general dispersion repair.

## 7. Conservative Yang--Mills frontier audit

| Implication | Status | Audit result |
|---|---|---|
| Exact orientation-correct one-star spill form | proved on one finite open block | pass at C2 restricted-model level |
| Conditional spill/free-energy design inequality | algebraically proved for frozen constants | pass at C2 restricted-model level |
| Four/eight-star zero modes | floating finite calculation | C1 only; exact certification missing |
| Growing-polymer boundary law | open | fail |
| Repair coverage of the nonlinear bad event | open | fail |
| Gauge-covariant nonlinear link transformation | open | fail |
| Haar/Jacobian and multiplicity control | open | fail |
| Boundary-history-uniform normalized measure comparison | open | fail |
| Strict state-weighted cluster ceiling | open | fail |
| Repeated RG trajectory and physical-length rate | open | fail |
| Continuum existence, OS reconstruction, dense observable core | open | fail |
| Hamiltonian mass gap | open | fail |

There is no reflection-positivity or Osterwalder--Schrader conclusion in H3 at
this stage.  There is no cutoff-uniform estimate, no construction of
four-dimensional pure Yang--Mills, and no spectral-gap theorem.  The first
unproved implication is:

> finite numerical multi-star cancellation \(\Longrightarrow\) an exact,
> orientation-correct, repair-relevant boundary law on a growing polymer
> family.

The strongest defensible status is:

> **C1 for H3 itself, supported by an exact C2 one-star obstruction and an
> exact C2 conditional budget formula.**

Any summary must use “finite collective-cancellation signal” rather than
“polymer boundary law,” “coordinated repair,” “confinement,” or “mass-gap
mechanism” until the corresponding gates are proved.

## 8. Strategic recommendation

The stream should proceed, because it tests a mechanism genuinely independent
of improving scalar local tails.  The immediate objective is not a nonlinear
repair.  It is an exact spectral atlas for growing oriented polymers and a
relative-cohomological explanation of its kernels.  That work has a sharp
falsification outcome and can yield a standalone finite-complex theorem even
if the Yang--Mills lift fails.

The first go/no-go checkpoint is reached after exact spectra and nullities are
available for at least two compact growing families and two adversarial thin
families.  Continue toward nonlinear repair only if either

\[
 r_P-z_P=O(|\partial P|)
\]

or an explicit boundary-trace factorization holds together with a nonvanishing
bad-event coverage constant.  Otherwise H3 should be downgraded to a finite
cochain-cancellation observation and resources redirected to the normalized
retained-kernel stream.
