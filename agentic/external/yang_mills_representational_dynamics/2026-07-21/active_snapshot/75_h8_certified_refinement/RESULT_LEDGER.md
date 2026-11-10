# H8 certified-refinement result ledger

## Scope

This stage develops H8 at claim level C2: an exact finite theorem for a
declared retained-state kernel. It does not construct the nonlinear
Yang--Mills kernel to which the theorem would have to be applied.

## Main theorem

Let \(Q\) be a nonnegative \(n\times n\) sub-Markov kernel and let
\(\Pi_0\) be a partition with \(b\) cells. Given \(\Pi_r\), assign state
\(i\) the signature

\[
 \sigma_r(i)=\left([i]_{\Pi_r},
    \left(\sum_{j\in C}Q_{ij}\right)_{C\in\Pi_r}\right).
\]

Partition states by equality of signatures. Then:

1. \(\Pi_{r+1}\) refines \(\Pi_r\).
2. Every strict step increases the number of cells, so termination occurs in
   at most \(n-b\) strict rounds.
3. The terminal partition \(\Pi_\star\) is stable: states in one cell have
   equal transition mass into every terminal cell.
4. Every stable refinement of \(\Pi_0\) refines \(\Pi_\star\). Therefore
   \(\Pi_\star\) is the unique coarsest stable refinement, modulo names of
   cells.
5. Each split is certified by an exact rational inequality between two
   transition masses into one old cell.

For item 4, let \(\mathcal S\) be any stable refinement of \(\Pi_0\).
Inductively suppose \(\mathcal S\) refines \(\Pi_r\). Every \(\Pi_r\)-cell
is a union of \(\mathcal S\)-cells. Stability on the latter makes transition
totals equal on each union, so states in one \(\mathcal S\)-cell have the same
\(\Pi_r\)-signature. Thus \(\mathcal S\) refines \(\Pi_{r+1}\). Passing to
the terminal iterate proves the claim.

## Exact Stage 52 reproduction

The original four-state kernel refines as

\[
 (0,0,1,1)\longrightarrow(0,0,1,2)
 \longrightarrow(0,1,2,3).
\]

The first witness distinguishes states 2 and 3 by mass \(1\) versus \(0\)
into \(\{0,1\}\). The second distinguishes states 0 and 1 by mass
\(1/10\) versus \(0\) into the now-visible cell \(\{2\}\). The initial
lumpability defect is exactly \(1\), the final defect is exactly zero, and
the two strict rounds saturate the \(n-b=2\) bound. Exhaustive enumeration of
all 15 four-state partitions finds exactly one stable refinement of the seed.

## Cross-stage regressions

| Regression | Exact outcome | Interpretation |
|---|---:|---|
| Stage 18 moment-only law | \(P(10)=P(01)=1/2\), union \(1>3/4\) | A stable indiscrete seed cannot manufacture the missing history observable. |
| Stage 19 weighted two-state kernel | \(QV=qV\) on both rows | Refinement preserves the exact weighted-transfer calibration but adds no new split to an already discrete seed. |
| Stage 24 equal channels | two cells remain | Channel permutation symmetry is preserved. |
| Stage 24 unequal persistence | five cells result | Four unequal charged channels are separated, with exact witnesses. |

For the Stage 19 row, the displayed decimal is parsed as an exact rational.
The equality \(QV=qV\) is exact for that fixture, not an independently
recovered real-valued parameter.

For the unequal-persistence fixture, \(q=1/400\), persistence is
\((0,1/4000,1/3000,1/2500)\), and the canonical weight has weighted ceiling
at most \(q\). Relabeling the states commutes with refinement.

## Complexity diagnostic

The deterministic delayed-distinction family starts from two cells and
reaches the discrete partition in exactly \(n-2\) rounds. If \(n=2^k\)
retained boundary configurations are represented explicitly, this becomes
\(2^k-2\) strict rounds. The theorem therefore certifies termination but
does not by itself control representation size. Physical use requires a
symmetry quotient or a proof that only a uniformly bounded family of
signatures occurs.

## Mechanization boundary

The executable checker verifies exact finite algebra, rejects floating-point,
negative, super-Markov, nonsquare, and malformed inputs, and fails a tampered
split witness. It does not verify:

- construction or normalization of a nonlinear finite SU(2) boundary kernel;
- measurability of a continuum boundary-state disintegration;
- cutoff- or volume-uniform stable-state counts;
- a uniform root-weight moment or weighted defect ceiling;
- Osterwalder--Schrader reconstruction or a Hamiltonian mass gap.

Accordingly, no C4 or C5 Yang--Mills claim follows from this stage.
