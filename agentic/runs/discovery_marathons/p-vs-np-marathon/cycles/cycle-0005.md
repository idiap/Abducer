# cycle-0005

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

For any linear-overhead projection-padding carrier H_N that computes SAT on an embedded formula length m=ell(N), an i.o. lower bound SIZE(H_N)>K N^{1+epsilon} transfers only to SAT exponent c satisfying ell(N)^c=o(N^{1+epsilon}). Thus ell(N)=N^{alpha+o(1)} excludes only c<(1+epsilon)/alpha, while ell(N)=N^{o(1)} can exclude all fixed c but makes the source threshold superpolynomial in the embedded SAT length. This is a valid route-level no-go for projection carriers, not a proof of P != NP.

## Definitions

- source object: H_N is a total N-bit Boolean carrier H_N(y)=V_N(y) AND SAT_m(pi_N(y)) with m=ell(N), shorter formulas padded to length m, and lower bounds measured against fan-in two nonuniform circuits.
- target object: SAT_m against nonuniform polynomial-size circuits; the target consequence SAT notin P/poly is obtained only if every fixed exponent c is excluded.
- controlled interface: a linear-size validity/decoder circuit and one SAT_m circuit compose to compute H_N with no per-instance advice or hidden nonuniform table beyond the target SAT circuit.
- target-preserving condition: lower-bound lengths N form an infinite support, m=ell(N) is unbounded and known, interface overhead is o(N^{1+epsilon}), and the projection is fixed uniformly enough for composition to preserve the target circuit assumption.

## Assumptions

- epsilon>0 and K>0 are fixed constants.
- The source lower-bound model is nonuniform Boolean circuit SIZE on the explicit family H_N.
- The decoder pi_N has output length exactly ell(N) after harmless SAT padding.
- The validity and projection circuitry have size O(N log N), or more generally o(N^{1+epsilon}).
- The claimed source lower bound SIZE(H_N)>K N^{1+epsilon} holds for infinitely many N in the support.

## Equations

- projection_upper_bound: `\mathrm{SIZE}(H_N) \le A N+B\,\mathrm{SIZE}(\mathrm{SAT}_{\ell(N)})+O(N\log N).`. Valid when: Valid when the source carrier is a fixed-output projection of SAT with linear decoding overhead.
- exponent_transfer: `\mathrm{SIZE}(\mathrm{SAT}_m)\le m^c\ \forall m \quad\Rightarrow\quad \mathrm{SIZE}(H_N)\le O(N\log N)+\ell(N)^c.`. Valid when: Applies after the target SAT circuit family is available at every embedded length.
- finite_window: `\ell(N)=N^{\alpha+o(1)}\ \Rightarrow\ \mathrm{SIZE}(H_N)\le N^{\alpha c+o(1)}+O(N\log N).`. Valid when: Valid when the embedding length has a stable polynomial exponent along the lower-bound support.
- contradiction_condition: `K N^{1+\varepsilon}<\mathrm{SIZE}(H_N)\ \mathrm{i.o.}\ \wedge\ \alpha c<1+\varepsilon\ \Rightarrow\ \mathrm{SAT}\notin \mathrm{SIZE}(n^c).`. Valid when: Requires the lower-bound lengths to be infinite and the overhead to be below the threshold.
- all_exponents_cost: `(\forall c\;\ell(N)^c=o(N^{1+\varepsilon}))\ \Longleftrightarrow\ \ell(N)=N^{o(1)},\quad \ell(N)=N^{o(1)}\Rightarrow N^{1+\varepsilon}=\ell(N)^{\omega(1)}.`. Valid when: Valid when ell(N) is unbounded and asymptotics are taken on the same infinite support.

## Attempted Derivation

- Generalize the padded SAT carrier to a projection family H_N with embedded SAT length ell(N) and linear validity/decoder overhead.
- Assume the target negation: SAT has nonuniform circuits of size m^c for a fixed exponent c at every length m.
- Compose the SAT_{ell(N)} circuit with pi_N and V_N, obtaining SIZE(H_N)<=O(N log N)+ell(N)^c.
- Combine with the source lower bound SIZE(H_N)>K N^{1+epsilon} on infinitely many N.
- If ell(N)=N^{alpha+o(1)}, contradiction is forced only for c<(1+epsilon)/alpha.
- To rule out all fixed c, require ell(N)=N^{o(1)} on the lower-bound support.
- But then the source threshold N^{1+epsilon} equals ell(N)^{omega(1)}, so the lower bound is no longer barely nontrivial relative to the embedded SAT instance size.

Blocking gap: Projection carriers cannot simultaneously keep the lower bound weak in the semantic source size and transfer it to exclusion of all polynomial SAT exponents.

## Falsifiers

- falsifier: ell(N)=N^{1/2}, epsilon=0.1, and target exponent c=3 leave the composed H_N upper bound above N^{1.1}, so the bridge cannot refute SAT in SIZE(n^3).
- falsifier: interface overhead N^{1+delta} with delta>=epsilon masks any target-circuit saving and collapses the quantitative transfer.
- falsifier: a decoder using N-bit nonuniform advice can make H_N hard for reasons unrelated to SAT, causing nonuniform leakage and invalid target preservation.
- falsifier: proving H_N>N^{1+epsilon} only at lengths where the projection image is empty or bounded gives no target-class consequence.

## Learning

Cycle 5 converts the padding quarantine into a general projection-carrier dichotomy. The valid bridge says N^{1+epsilon} lower bounds transfer through ell(N) only when ell(N)^c is below the threshold. Positive polynomial embedding length gives only a bounded exponent window; subpolynomial embedding length gives all exponents but turns the source lower bound into ell(N)^{omega(1)}. Thus pure projection magnification fails as a weak-source path, with an explicit falsifier rather than a slogan.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit an MCSP-based route: set source object MCSP_{n,s} on N=2^n-bit truth tables, choose a concrete circuit model for the lower bound, state the exact threshold N^{1+epsilon} or smaller, and test whether the known magnification transfer is non-natural, target-preserving, and strong enough to imply SAT notin P/poly rather than only EXP or subexponential derandomization consequences.

# Barrier-Aware Lower-Bound Route: MCSP-PRF Transfer Audit

## Candidate Lemma

PRF-to-MCSP transfer: let N=2^m and let MCSP_s be the language of N-bit truth tables of m-variate Boolean functions with circuit size at most s=s(m). If a length-N PRG/PRF G_m has every output truth table computable by circuits of size at most s, and fools nonuniform N^k-size distinguishers with error below 1-2^{c s log s-N}, then MCSP_s is not in SIZE(N^k). Since MCSP_s is in NP for s=poly(N), this conditionally gives NP not subset SIZE(n^k), but only from the source PRF assumption.

## Definitions

- source object: a truth-table PRG/PRF family G_m:{0,1}^{r(m)} -> {0,1}^{N}, N=2^m, whose bit-generator B_m(z,i) has size q(m) and q(m)<=s(m).
- target object: the nonuniform lower bound MCSP_s notin SIZE(N^k), where MCSP_s contains exactly the N-bit truth tables of m-input functions with circuit size at most s(m).
- controlled interface: assume a small target circuit C_N for MCSP_s and use D_N=1-C_N as a black-box distinguisher between uniform N-bit strings and outputs of G_m.
- target-preserving condition: the same size threshold s must certify all PRG outputs as yes-instances of MCSP_s, and PRG security must hold against circuits as large as the hypothetical MCSP circuit.
- security scale: adversaries have size polynomial in N, equivalently exponential in m; ordinary poly(m)-security is insufficient.
- barrier status: the argument is a valid natural-proof contraposition, not an escape from naturalization.

## Assumptions

- Fan-in two circuit counting gives at most 2^{c s log s} m-input circuits of size at most s.
- The MCSP threshold s satisfies s log s << N, e.g. s=m^d, so low-complexity truth tables are sparse.
- For every seed z, G_m(z) is the truth table of a function computed by a circuit of size at most s.
- The PRG/PRF security guarantee is nonuniform and covers size N^k+O(1) distinguishers.
- MCSP_s is encoded so that witness circuits of size s can be verified in poly(N) time.

## Equations

- counting_sparsity: `\Pr_{U\leftarrow\{0,1\}^{N}}[U\in MCSP_s] \le 2^{c s\log s-N}`. Valid when: Valid when N=2^m, circuits have fan-in two, s>=m, and c bounds the standard circuit-counting encoding.
- distinguisher_advantage: `\Delta(D_N)\ge 1-2^{c s\log s-N},\quad D_N=1-C_N`. Valid when: Applies when C_N exactly decides MCSP_s and every PRG output truth table has circuit size at most s.
- security_transfer: `\epsilon_G(N,N^k)<1-2^{c s\log s-N}\Rightarrow MCSP_s\notin SIZE(N^k)`. Valid when: Requires nonuniform PRG security against N^k-size distinguishers and the same threshold s used by MCSP.
- np_transfer: `MCSP_s\in NP\ \wedge\ MCSP_s\notin SIZE(N^k)\Rightarrow NP\not\subseteq SIZE(n^k)`. Valid when: Valid when s is polynomial in N and the lower bound holds on infinitely many input lengths.

## Attempted Derivation

- Fix m, set N=2^m, and define MCSP_s on N-bit truth tables.
- Assume for contradiction that a circuit C_N of size at most N^k decides MCSP_s.
- Let D_N=1-C_N. This adds only O(1) gates, so D_N is within the promised security size.
- By circuit counting, a uniformly random N-bit truth table is in MCSP_s with probability at most 2^{c s log s-N}. Thus D_N accepts uniform strings with probability at least 1-2^{c s log s-N}.
- For every seed z, hardwire z into the bit-generator B_m(z,i). The resulting m-input circuit has size at most s, so G_m(z) is in MCSP_s and D_N rejects it.
- Therefore D_N distinguishes uniform from G_m with advantage at least 1-2^{c s log s-N}, contradicting PRG security if the error bound is smaller.
- Hence no such C_N exists. Since MCSP_s is in NP for s=poly(N), the target consequence is a conditional NP nonuniform lower bound, not an unconditional separation.

Blocking gap: The derivation is a valid conditional lemma, but the missing source object is an unconditional PRG/PRF with output length 2^m, output functions of size s, and security against 2^{Omega(m)}-size distinguishers. Proving that source object is itself a major lower-bound problem.

## Falsifiers

- falsifier: PRF security is stated only for poly(m)-size distinguishers, while the induced MCSP distinguisher has size N^k=2^{km}.
- falsifier: after hardwiring the seed, the PRG output function has circuit size greater than the MCSP threshold s.
- falsifier: s log s is too close to N, so the complement of MCSP_s is not large enough for the claimed advantage.
- falsifier: the MCSP encoding includes advice or parameters not covered by the NP verifier and target SIZE(N^k) model.
- falsifier: the route advertises an unconditional NP lower bound while relying on the source PRG/PRF hardness assumption.

## Learning

Cycle 5 obtains a concrete quantitative transfer: exponentially secure low-complexity PRG/PRF outputs imply MCSP_s notin SIZE(N^k) with advantage threshold 1-2^{O(s log s)-N}. The useful bottleneck is not the slogan that MCSP is tied to natural proofs, but the exact adversary scale N^k and the threshold s log s << N. This is valid route-level progress and not evidence by itself for P != NP.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit a specific hardness-magnification theorem for MCSP or Kt: name the exact barely-superlinear lower bound, the source model, and whether its proof would instantiate L5.1's natural distinguisher or uses a non-natural feature.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

For constants epsilon>0 and kappa<infinity, a uniform constant-gap sequence of MCSP no-instances Y_i of variable lengths m_i with C(Y_i)>2^{epsilon m_i} yields an L in E such that C(L_t)>2^{delta t} for every sufficiently large t and every delta<epsilon/kappa. This is a route-level bridge to E hardness and IW-style derandomization, not a proof of P != NP.

## Definitions

- source object: a uniform sequence (m_i,Y_i) where Y_i is a truth table in {0,1}^{2^{m_i}}, m_i is strictly increasing, bit access to Y_i[x] is computable in 2^{O(m_i)}, and Y_i is on the no-side of MCSP at threshold 2^{epsilon m_i}.
- target object: a language L in E=DTIME(2^{O(n)}) whose length-t slice L_t has Boolean circuit complexity greater than 2^{delta t} for all sufficiently large t.
- controlled interface: on input w of length t choose the unique i with m_i<=t<m_{i+1}, define L(w)=Y_i[prefix_{m_i}(w)], and ignore all padding bits.
- target-preserving condition: the sequence m_i is uniformly computable, has multiplicative gap m_{i+1}<=kappa m_i+O(1), and the table-selection and bit-access procedures use no advice or nonuniform selector.

## Assumptions

- Boolean circuit size C(.) is fan-in-2 nonuniform circuit size over the usual basis, and fixing input variables never increases size.
- epsilon>0 and kappa are constants independent of i; delta is any fixed constant with delta<epsilon/kappa.
- For all sufficiently large i, Y_i is a valid MCSP no-instance: C(Y_i)>2^{epsilon m_i}.
- The interval index i(t) and the bit Y_i[x] are computable uniformly within 2^{O(t)} time.

## Equations

- mcsp-threshold: `N_i=2^{m_i},\quad Y_i\notin \mathrm{MCSP}[N_i^{\epsilon}]\Rightarrow C(Y_i)>N_i^{\epsilon}=2^{\epsilon m_i}`. Valid when: Valid when the source lower-bound model is standard Boolean circuit size and the MCSP promise threshold is N_i^epsilon.
- padding-lower-bound: `m_i\le t<m_{i+1}\le \kappa m_i+O(1)\quad\Rightarrow\quad C(L_t)\ge C(Y_i)>2^{\epsilon m_i}\ge 2^{(\epsilon/\kappa-o(1))t}`. Valid when: Applies after the padding map chooses the unique carrier interval and fixing padded inputs preserves circuit-size lower bounds.
- target-exponent: `\forall\delta<\epsilon/\kappa\;\exists t_0\;\forall t\ge t_0:\ C(L_t)>2^{\delta t}`. Valid when: Requires constant multiplicative carrier gaps so the o(1) loss is eventually below epsilon over kappa minus delta.
- uniform-running-time: `T_L(t)\le 2^{a m_i}\mathrm{poly}(t)\le 2^{O(t)}`. Valid when: Valid when bit access to Y_i and computation of the interval index are uniform without advice.

## Attempted Derivation

- Let f_i:{0,1}^{m_i}-> {0,1} be the function with truth table Y_i.
- For each target length t choose i with m_i<=t<m_{i+1} and define L_t(u,v)=f_i(u), where |u|=m_i and v contains the padding bits.
- Uniformity: compute i by enumerating the computable m_j up to t, then compute the requested bit of Y_i in time 2^{O(m_i)}<=2^{O(t)}; therefore L is in E.
- Lower bound: if a circuit D of size S computes L_t, fixing all padding inputs to 0 gives a circuit of size S for f_i. Thus S>=C(Y_i)>2^{epsilon m_i}.
- Since t<m_{i+1}<=kappa m_i+O(1), for every delta<epsilon/kappa and all large t one has 2^{epsilon m_i}>2^{delta t}.
- Therefore the bridge lemma is valid: a dense uniform no-side MCSP carrier transfers to all-length E hardness with exponent delta<epsilon/kappa.

Blocking gap: The remaining gap is source construction: no known MCSP reduction or meta-complexity argument produces a uniform constant-gap sequence of explicit no-side tables at threshold 2^{epsilon m}.

## Falsifiers

- falsifier: m_i=2^i with constant epsilon gives only delta_i about epsilon/2^i at upper endpoints, so all-length IW hardness collapses.
- falsifier: a reduction proving MCSP hardness but outputting no-side tables only on an unknown sparse set gives no uniform interval map i(t).
- falsifier: existential high-MCSP tables chosen by advice yield at best an E/poly object and are not valid for the E target.
- falsifier: MCSP threshold 2^{epsilon_i m_i} with epsilon_i->0 transfers no fixed positive exponential lower-bound exponent.
- falsifier: a polynomial-time natural property that is large and useful against all small circuits would trigger the Razborov-Rudich obstruction; the route must use non-natural certification or assumptions outside that formal pattern.

## Learning

Cycle 5 turns the vague density requirement into a proved quantitative bridge: MCSP no-side threshold 2^{epsilon m} plus carrier gap kappa gives all-length E hardness exponent any delta<epsilon/kappa. The exact obstruction is now constructive, not folklore: build a uniform constant-gap no-side carrier or the route fails by threshold collapse or nonuniform leakage.

## Gedanken Experiment Design Seed

- Need decision: ``
- Rationale:
- Situation seed:
- Varied variable:
- Held-fixed controls:
- Expected observation:
- Transfer certificate needed:

## Next Experiment

Audit known MCSP gap reductions and meta-complexity candidates for whether their no-side outputs can be normalized into a uniform constant-gap sequence; record the exact m_i growth, epsilon threshold, and selector uniformity.
