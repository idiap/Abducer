# H6 typed-square result ledger

## Strongest result

For typed rational maps

`B_k : X_k -> X_{k+1}`, `T_k : Y_k -> Y_{k+1}`, and
`R_k : X_k -> Y_k`, define

`Omega_k = T_k R_k - R_{k+1} B_k`.

The implementation verifies exactly, entry by entry,

`T_{n:0} R_0 - R_n B_{n:0}`

`= sum_{j=0}^{n-1} T_{n:j+1} Omega_j B_{j:0}`.

With `S_n : Y_n -> X_n`, it also verifies

`S_n T_{n:0}R_0-B_{n:0}`

`= (S_nR_n-I)B_{n:0}`

`  + sum_j S_n T_{n:j+1} Omega_j B_{j:0}`.

Every matrix entry and every induced-infinity-norm ledger entry is a Python
`Fraction`. Named endpoint types are checked even when incompatible spaces
happen to have the same dimension.

## Exact finite certificates

| ID | Result | Status | Level |
|---|---|---|---|
| H6-TYPE | named domain/codomain checking for every map and composition | proved and hostile-tested | C2 |
| H6-TEL | finite-tower telescoping identity | proved exactly; 20 rational tower tests plus partial towers | C2 |
| H6-REC | recovered transport identity and future-aware norm bound | proved exactly; 10 rational recovery tests | C2 |
| H6-STAR | balanced-star `[C,O]` has rank two and Euclidean norm one | proved by exact Gram-projector identity | C2 |
| H6-SPEC | hostile spectrum `0,(239/630)^2,(33/70)^2,1` | proved by exact characteristic polynomial | C2 |
| H6-SPEC+ | correct spectrum `0,(239/630)^2,(33/70)^3` | proved by exact characteristic polynomial | C2 |
| H6-CE | all four required counterexamples | proved exactly | C2 |

The Euclidean norm certificate is

`[C,O]^T[C,O] = (11^T + ss^T)/6`,

the orthogonal projector onto `span{1,s}` because `1^T s=0` and both vectors
have squared norm six.

The balanced-star matrix is an explicit rational fixture. Its rank, norm, and
spectra are proved exactly for that matrix. This stage does not derive it from
Stage 70 or verify a cross-stage source hash, so its geometric provenance is
metadata rather than a certified implication.

## Counterexample ledger

| Counterexample | Exact witness | Hypothesis it rules out |
|---|---|---|
| small rotations | rational rotation parameter `1/100`; one-step infinity norm `202/10001`, but the 79-step defect exceeds one | uniform one-step smallness without summability/contraction |
| hidden-to-visible swap | `e_1^* Omega=0`, while `e_1^* Swap Omega=(1,0)` | insertion-scale projected control without future invariance |
| ill-conditioned recovery | `R=diag(1,1/1000)`, `S=R^{-1}`; a `1/1000` defect becomes one | existence of an exact recovery without uniform stability |
| support multiplicity | 100 cells each contribute `1/100` to an unnormalized sum | scalar local error without support normalization |

## Frontier audit

| Claim | Status |
|---|---|
| nonlinear gauge-covariant `SU(2)` square | open |
| boundary-history-uniform support seminorm | open |
| positive or reflection-positive recovery | open |
| cutoff/volume-uniform repeated-scale summability | open |
| continuum construction and OS reconstruction | open |
| Yang--Mills mass gap | not reached |

Strongest defensible level: **C2**. The first open implication is a concrete
nonlinear `SU(2)` block satisfying the recovered inequality with uniform
support-indexed constants.
