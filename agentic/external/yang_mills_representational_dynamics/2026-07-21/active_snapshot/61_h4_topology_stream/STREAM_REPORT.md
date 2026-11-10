# H4 stream report: topology as compositional data

## Outcome

H4 survives only in a sharpened form.  Topology cannot be retained as a short
list of terminal labels that are evaluated independently on each block.  It
must be retained as data equipped with a composition law, including the
bilinear cross terms and boundary information that appear when regions are
glued.

The strongest new result is exact but deliberately restricted:

> **Contextual-minimality theorem.**  In the embedded integral-flux model on
> an oriented four-torus, any deterministic statistic that predicts the
> Pfaffian charge after addition of every possible integral-flux context must
> distinguish every vector in \(\mathbb Z^6\).  Equivalently, the full
> six-component integral flux, or its complete polarized-pairing covector, is
> the minimal contextually sufficient carrier.

This is a `C2` algebraic theorem for the additive integral-flux calibration.
It is not a construction of nonabelian lattice topology, a bound on its sector
weights, an RG theorem, a continuum construction, or a mass-gap result.

## 1. Evidence inherited from the package

Three earlier stages supply the finite evidence.

1. Stage 39 computes the periodic \(2^4\) cubical cochain complex over
   \(\mathbb F_2\), with
   \[
   (b_0,b_1,b_2,b_3,b_4)=(1,4,6,4,1),
   \]
   six independent two-flux classes, and \(2^6=64\) center sectors.
2. Stage 47 proves that a center sector of Hamming weight \(k\) needs at least
   \(4k\) plaquettes and constructs representatives attaining the bound.  It
   also correctly leaves the full continuous-sector partition ratio open.
3. Stage 48 introduces the integral lift
   \[
   n=(n_{01},n_{02},n_{03},n_{12},n_{13},n_{23})\in\mathbb Z^6
   \]
   and the quadratic Pfaffian charge
   \[
   Q(n)=n_{01}n_{23}-n_{02}n_{13}+n_{03}n_{12}.
   \]
   The family \((2k,0,0,0,0,2k)\) has zero center label and
   \(Q=4k^2\), proving that center flux alone erases unbounded integer data.

The H4 probe in Stage 52 goes further: two states with the same center label
and the same value of \(Q\) acquire different charges after addition of one
common context.  The current stream identifies the general mechanism and
proves its minimality.

All 56 inherited tests relevant to Stages 39, 47, 48, and 52 pass in this
review (14, 15, 15, and 12 tests, respectively).

## 2. Polarization is the missing composition law

Write the flux coordinates in the fixed order
\[
(01,02,03,12,13,23).
\]
The polarization of \(Q\) is
\[
\begin{split}
B(n,m)&=Q(n+m)-Q(n)-Q(m)\\
 &=n_{01}m_{23}+n_{23}m_{01}
   -n_{02}m_{13}-n_{13}m_{02}
   +n_{03}m_{12}+n_{12}m_{03}.
\end{split}
\]
Thus charge does not compose additively:
\[
Q(n+m)=Q(n)+Q(m)+B(n,m).
\]
In matrix form, \(B(n,m)=n^{\mathsf T}Jm\), where
\[
J=
\begin{pmatrix}
0&0&0&0&0&1\\
0&0&0&0&-1&0\\
0&0&0&1&0&0\\
0&0&1&0&0&0\\
0&-1&0&0&0&0\\
1&0&0&0&0&0
\end{pmatrix}.
\]
Direct exact arithmetic gives
\[
J^2=I,\qquad \det J=-1,\qquad \operatorname{signature}(J)=(3,3).
\]
The pairing is therefore nondegenerate and unimodular over \(\mathbb Z\).

The mod-two center label
\[
z(n)=n\pmod 2\in(\mathbb Z/2\mathbb Z)^6
\]
does compose additively.  A redundant but audit-friendly state is
\[
\tau(n)=\bigl(z(n),n,Q(n),\ell_n\bigr),
\qquad \ell_n(\,cdot\,)=B(n,\,cdot\,).
\]
Its composition law is
\[
\begin{aligned}
n''&=n+n',&z''&=z+z'\pmod2,\\
\ell''&=\ell+\ell',&
Q''&=Q+Q'+\ell_n(n').
\end{aligned}
\]
Because \(B\) is bilinear, the cross term obeys the two-cocycle identity
\[
B(n,m)+B(n+m,k)=B(m,k)+B(n,m+k),
\]
so this composition is associative.  In this fixed model, \(z,Q,\ell\) are
derived checks: the coordinate-minimal state is simply \(n\).  Retaining the
redundant quantities is useful for detecting orientation, reduction, and
implementation errors.

## 3. Exact contextual-minimality theorem

### Definition

A statistic \(s:\mathbb Z^6\to S\) is *contextually sufficient for charge* if
\[
s(n)=s(m)
\quad\Longrightarrow\quad
Q(n+c)=Q(m+c)\quad\text{for every }c\in\mathbb Z^6.
\]
This is the relevant notion when an unresolved neighboring block can provide
an arbitrary additive context.

### Theorem

Every contextually sufficient statistic for \(Q\) is injective.  It follows
that neither \(Q\), nor \((z,Q)\), nor any proper deterministic quotient of
the full flux can close the charge update against all contexts.

### Proof

Suppose \(s(n)=s(m)\).  Taking \(c=0\) gives \(Q(n)=Q(m)\).  Polarization then
gives, for every \(c\),
\[
0=Q(n+c)-Q(m+c)=B(n-m,c).
\]
Hence \((n-m)^{\mathsf T}J=0\).  Since \(J\) is unimodular, \(n-m=0\), so
\(n=m\).  This proves injectivity. \(\square\)

Only six basis contexts are needed: the vector
\[
\bigl(B(n,e_1),\ldots,B(n,e_6)\bigr)=n^{\mathsf T}J
\]
already reconstructs \(n\), because \(J^{-1}=J\).

### Concrete collision retained as a regression case

Let
\[
n=(-1,-1,-1,-1,-1,-1),\qquad
m=(-1,-1,-1,-1,1,1).
\]
Both have center label \((1,1,1,1,1,1)\) and \(Q=1\).  With the common
context \(c=(1,0,0,0,0,0)\), however,
\[
Q(n+c)=0,\qquad Q(m+c)=2.
\]
This is the smallest existing package witness to the general theorem.

## 4. What “compositionally complete” must mean

There are three distinct levels, and conclusions must not be moved between
them.

### Level A: fixed additive calibration — completed

On \(\Lambda^2\mathbb Z^4\), retain \(n\), derive \(z,Q,\ell\), and compose
with the equations above.  This is exact and associative.

### Level B: finite cubical integral cohomology — specified, not completed

On a finite cell complex \(K\), the coordinate-free carrier should include

\[
\left(H^2(K;\mathbb Z),\ [n],\ I_K,\ r_2[n],\ \text{boundary/relative data}\right),
\]

where \(I_K\) is the appropriate cup/intersection pairing and \(r_2\) is
mod-two reduction.  A block map must be induced by a chain/cochain map, and
gluing must respect relative cohomology and boundary transgression.  A bare
six-vector silently assumes a fixed torus, basis, orientation, and pairing.

For regions with boundary, a bulk integer alone is generally not composable:
the boundary trivialization or Chern--Simons-type transgression data carry the
interface correction.  This is a structural requirement, not a completed
nonabelian construction.

### Level C: nonabelian lattice gauge fields — open

The required carrier must classify the admissible lattice configuration in
the chosen global form of the gauge group and under the declared boundary
conditions.  Center twists, an embedded-abelian flux, and a nonabelian second
Chern class must not be silently identified.  In particular:

- the meaning and availability of center-flux sectors depend on whether the
  theory uses strict periodic fields, twisted boundary conditions, or a
  quotient global form;
- Stage 48's Pfaffian is an embedded-abelian calibration, not yet the complete
  nonabelian lattice charge;
- the blocking map must preserve admissibility or give a quantitative bound
  on the configurations where the topological chart fails;
- exceptional configurations and changes of topological sector must remain
  in the normalized measure rather than being deleted by definition.

These points impose the current `C2` ceiling.

## 5. Sector weights are boundary-resolved kernels

For a region \(R\), boundary state \(b\), and topology state \(\tau\), the
unnormalized sector weight has the schematic form
\[
Z_R(\tau;b)=
\int_{\Omega_R(\tau;b)} e^{-S_R(A)}\,d\mu_R(A).
\]
The physical object needed for iteration is a normalized conditional kernel,
not a minimum action and not an isolated scalar:
\[
K_R\bigl((b,\tau),d(b',\tau')\bigr)
=\frac{Z_R\bigl((b,\tau),d(b',\tau')\bigr)}
       {Z_R^{\mathrm{all}}(b,\tau)}.
\]
Gluing two regions contracts their common boundary variable and sums over
compatible topology states.  Therefore boundary-resolved sector kernels
compose by convolution or matrix multiplication.

### Scalar-weight counterexample

Scalar sums cannot determine gluing.  Consider two boundary channels and
region vectors
\[
a=(1,3),\qquad a'=(2,2),\qquad b=(3,1).
\]
Both \(a\) and \(a'\) have the same scalar sector weight, namely four, but
gluing to the same neighbor gives
\[
a\cdot b=6,\qquad a'\cdot b=8.
\]
Consequently, even exact scalar sector partition functions are not a
compositionally sufficient retained state.  Boundary response must be kept.

Stage 47's exact minimum-action expression
\[
R_{\min}(\alpha)=\bigl(1+e^{-4\alpha}\bigr)^6-1
\]
is valuable calibration, but it contains neither continuous fluctuation
entropy nor boundary response.  It cannot be substituted for the normalized
kernel above.

## 6. Finite algorithms

### Algorithm A: construct and audit the topological carrier

**Input:** oriented finite cell complex, integral coboundary matrices, block
chain map, cup-product rule, and a finite flux catalog.

1. Verify \(d_{k+1}d_k=0\) exactly.
2. Use Smith normal form over \(\mathbb Z\) to compute the free and torsion
   parts of \(H^2\); separately row-reduce mod two for center data.
3. Compute the cup/intersection matrix \(J_K\) in a declared basis and record
   every orientation convention.
4. Canonicalize cocycles modulo coboundaries and retain relative/boundary
   classes when the region has an interface.
5. Propagate the class through the block chain map and verify naturality of
   reduction and pairing.
6. Form context signatures
   \[
   \sigma_C(n)=\bigl(z(n),Q(n),B(n,c_1),\ldots,B(n,c_r)\bigr)
   \]
   and refine any colliding states that evolve differently.
7. Return either a closed finite carrier or an explicit collision witness.

For the current \(\mathbb Z^6\) calibration, the six basis contexts give an
injective signature immediately.

### Algorithm B: compute boundary-resolved sector kernels

**Input:** a finite lattice block, finite/discretized boundary state set,
topology classifier, positive action weight, and certified integration or
quadrature enclosures.

1. Partition configurations by input boundary, output boundary, and topology.
2. Accumulate nonnegative interval enclosures for every kernel entry.
3. Normalize row by row; reject zero denominators and track enclosure error.
4. Check gauge invariance, positivity, sector exhaustiveness, and the declared
   reflection operation.
5. Glue two copies by tensor contraction and compare with a direct two-block
   computation.
6. Run partition refinement whenever two retained states have distinguishable
   rows.
7. Evaluate a topology-channel Lyapunov moment rather than an unnormalized
   action barrier.

This algorithm is finite and falsifiable.  It does not by itself supply
cutoff-, volume-, or history-uniform bounds.

## 7. Obstruction ledger

| Candidate retained object | Exact verdict | Reason |
|---|---|---|
| six center bits \(z\) | insufficient | fixed \(z\) hides unbounded \(Q\) |
| integer charge \(Q\) | insufficient | charge has unresolved polarized cross terms |
| \((z,Q)\) | insufficient | explicit common-context collision |
| full integral flux \(n\) on fixed \(T^4\) | compositionally complete for the additive calibration | \(n+n'\) and \(B(n,n')\) are computable |
| pairing covector \(\ell_n=B(n,\cdot)\) | equivalent to \(n\) in this calibration | \(J\) is unimodular |
| scalar sector weight \(Z_R(\tau)\) | insufficient for gluing | loses interface correlations |
| boundary-resolved positive sector kernel | correct finite compositional type | exact physical construction and uniform bounds remain open |
| embedded-abelian flux/Pfaffian | not a complete nonabelian carrier | bundle, admissibility, and interface theorems absent |

## 8. The next theorem

### Proposed one-block nonabelian topology-kernel theorem

Freeze a compact gauge group and its global form, a finite four-dimensional
lattice block, boundary conditions, a gauge-invariant admissibility rule, and
a reflection-positive regulated measure.  Construct a retained topology state
\(\tau\) and boundary state \(b\) such that:

1. admissible configurations are partitioned measurably and exhaustively by
   \((b,\tau)\), up to an explicitly bounded exceptional set;
2. \(\tau\) contains the appropriate center/twist class, integral nonabelian
   topological class, and the interface data needed for gluing;
3. the one-block map induces an associative topology update, and direct
   two-block classification agrees with composition of two one-block maps;
4. the normalized boundary-resolved sector kernel is positive, gauge
   invariant, and has no omitted sectors;
5. for a declared topology size \(T(\tau)\) and positive retained-state weight
   \(V\), a certified finite bound of the form
   \[
   \sup_{(b,\tau)}\frac{1}{V(b,\tau)}
   \sum_{\tau'}\int
   e^{\lambda T(\tau')}V(b',\tau')
   K_R\bigl((b,\tau),d(b',\tau')\bigr)<\infty
   \]
   holds on the one-block domain.

The first version may be finite-volume and regulator-specific.  A later
theorem must make the constants uniform in volume, cutoff, block scale, and
positive-mass retained history and must fit within the strict multichannel
budget.  No iteration claim is admissible before the two-block composition
check succeeds.

## 9. Strategic conclusion

The simple substrate delivered by H4 is a **cohomological state object plus a
positive boundary kernel**:
\[
\mathsf T_R=
\bigl(\text{relative cocycle/class},\text{pairing},
\text{boundary transgression},\text{center reduction}\bigr),
\qquad K_R\ge 0.
\]
Gauge-field coordinates realize this object; the topology carrier records
what survives gluing; and the kernel records how much normalized measure each
transition carries.  The exact additive theorem shows why total-charge labels
are too compressed.  The physical Yang--Mills task is now localized: build
this object nonabelianly on one block, prove its two-block coherence, and only
then seek a uniform topology-channel bound.

## 10. Claim guardrails

- **Proved (`C2`):** center cohomology and barriers in the finite periodic
  models; integral-flux/Pfaffian algebra; contextual minimality of full
  \(\mathbb Z^6\) flux; insufficiency of scalar weights for generic gluing.
- **Specified but open:** integral finite-cell implementation with relative
  data; boundary-resolved Yang--Mills sector kernel; nonabelian topology under
  blocking; exceptional-set estimates; uniform sector tails.
- **Not claimed:** complete nonlinear `SU(2)` or other simple-group topology;
  basin entry; repeated RG; continuum existence; Osterwalder--Schrader
  reconstruction; Hamiltonian mass gap; Clay-level result.

