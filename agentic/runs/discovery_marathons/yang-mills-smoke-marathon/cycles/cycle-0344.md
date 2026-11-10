# cycle-0344

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, declarative conceptual tension, and efficient-representation requirements. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.2943978bc7b2`
- `marathon.branch.74748c38302d`
- `marathon.branch.55f194abd6e5`

## Branch Outputs

# Finite Route A endpoint cumulant screen for reflected Wilson collars

## Candidate Lemma

One-sided endpoint source-screen theorem: for the fixed post-H,K reflected-Wilson hairpin block, if each source-equivalence endpoint class has certified nonpositive connected fourth cumulant, then only positive signed endpoint dominance can lower the corrected OS scalar; the block is promoted, falsified, or quarantined by one valid interval.

## Definitions

- source object: heat-kernel plaquette-sheet endpoint source data C_ep consisting of endpoint classes c, seven regulated source values for log Z_c(s), cumulant intervals [kappa_c^-,kappa_c^+], signed incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and uniform tail budget T_tail.
- target object: the finite Schur-Feshbach corrected null-channel OS scalar I_gate for the locked three-hairpin Wilson block after H,K have been fixed; it is a finite Route A certificate, not a continuum mass-gap statement.
- controlled interface: aggregate endpoint boxes only by equality of regulated source derivatives, form D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}, multiply by same-theory connected cumulant intervals, add C_N and T_tail, then export only the scalar interval for the finite OS gate.
- same-theory condition: the Wilson normalization, heat-kernel regulator, gauge-invariant observable algebra, reflection map, endpoint source insertions, and tail subtraction are identical on the collar and endpoint sides; no boundary counterterm, new boundary state, or algebra enlargement is allowed.
- bridge/carrier: C_ep is incidence-signed and source-equivalent; raw R is representation-limited because it forgets incidence signs, while raw kappa_4 spectra are too strong because they ignore the null-channel contraction.
- conceptual pressure: endpoint collapse must be sign-certified inside the same Wilson theory after H,K without hiding the connected boundary-OPE polarization inside a symbolic parameter.

## Assumptions

- Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action on a reflection-positive collar, restricted to a fixed finite Wilson hairpin block.
- Regime: endpoint boxes are smaller than the collar scale but larger than the lattice cutoff, so the plaquette-sheet endpoint OPE and uniform tail split are meaningful.
- Uniformity: cumulant intervals and T_tail are uniform in the cutoff along the finite block under consideration; no continuum extrapolation is claimed.
- Same-theory: endpoint source derivatives are computed in the same regulated Wilson theory as the collar OS matrix, not in a boundary effective theory.
- Validity: each endpoint source class satisfies kappa_c^+ <= 0, or else the one-sided shielding statement is suspended for that class.
- Local: success changes only the finite post-H,K reflected-Wilson OS transfer gate; Clay existence, gauge-invariant observable density, OS spectral transfer, nontriviality, and mass gap remain untouched.

## Equations

- endpoint dominance: `D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}`. Valid when: Valid when source-equivalent endpoint boxes have first been aggregated by equal regulated heat-kernel source derivatives.
- endpoint scalar decomposition: `I_{\mathrm{gate}}=M_G+C_N\sum_c D_c\,\kappa_c+T_{\mathrm{tail}}`. Valid when: Applies after Wick-square Gram terms and straight f f incidence contacts have been cancelled in the fixed null channel.
- one-sided lower interval: `I_- = M_G-C_N\sum_c [D_c]_+\,K_c^- -\tau_{\mathrm{tail}},\quad K_c^-:=\max(0,-\kappa_c^- )`. Valid when: Requires certified endpoint nonpositivity kappa_c^+ <= 0 and a cutoff-uniform absolute tail bound tau_tail.
- finite promotion test: `I_-\ge 0\Rightarrow \text{finite block passes};\qquad I_+<0\Rightarrow \text{finite same-theory falsifier}`. Valid when: Valid only for this finite Wilson block with the locked H,K data and same-theory endpoint source carrier.

## Attempted Derivation

- Definition/assumption context: this derivation is interpreted inside Reflection-Positivity Closed-Cone Topology; source object: heat-kernel plaquette-sheet endpoint source data C_ep consisting of endpoint classes c, seven regulated source values for log Z_c(s), cumulant intervals [kappa_c^-,kappa_c^+], signed incidences b_{ij,c}, color factor C_N, Gaussian margin M_G, and uniform tail budget T_tail.; target object: the finite Schur-Feshbach corrected null-channel OS scalar I_gate for the locked three-hairpin Wilson block after H,K have been fixed; it is a finite Route A certificate, not a continuum mass-gap statement.; Model: four-dimensional SU(N) lattice Yang-Mills with heat-kernel plaquette action on a reflection-positive collar, restricted to a fixed finite Wilson hairpin block..
- Started from the finite Schur-Feshbach reduced OS scalar after H,K and wrote the remaining connected endpoint contribution as a sum over source-equivalent endpoint classes.
- Used the heat-kernel plaquette-sheet regulator and singlet Wilson flux sources so that Wick-square contractions stay as positive Gram terms and straight nonabelian f f contacts cancel by the fixed null incidence identity.
- Aggregated endpoint boxes before clipping: b_{ij,c}=sum_{v in c} b_{ij,v} and D_c=2b_{12,c}-4b_{13,c}-4b_{23,c}.
- Inserted the certified nonpositivity screen kappa_c^+<=0. Then classes with D_c<=0 cannot lower I_gate, while classes with D_c>0 lower it by at most C_N D_c max(0,-kappa_c^-).
- Added a cutoff-uniform tail budget tau_tail to obtain I_- and the finite promote/falsify/quarantine trichotomy.

Blocking gap: No actual endpoint source intervals or cutoff-uniform M8/tail bounds have been computed for the positive-D source classes of the fixed hairpin geometry.

## Falsifiers

- falsifier: a positive-D endpoint source class has a certified negative connected cumulant witness large enough that I_+<0.
- falsifier: T_tail is not cutoff-uniform, so endpoint locality cannot be transferred to the finite OS scalar.
- falsifier: the source-equivalence aggregation changes when the cutoff is refined, indicating the carrier is not same-theory valid.
- falsifier: a boundary counterterm is required to define the endpoint source derivative, proving that the collar and endpoint observables are not the same Wilson theory.
- Stress case: a D_c<0 class has a positive connected fourth cumulant outside the root-quartic screen, invalidating the one-sided shielding simplification.

## Learning

Conceptual pressure attacked: endpoint collapse must be sign-certified inside the same Wilson theory after H,K. Declarative tension: collar OS positivity, fixed gauge-invariant Wilson observables, and singular connected endpoint OPE must coexist without a boundary theory, but raw R is representation-limited, raw kappa_4 spectra are too strong, and global Schur-preimage positivity is valid but too coarse after H,K. The efficient representation is C_ep: source classes, source stencils or root-quartic caps, cumulant intervals, aggregated signed D_c, C_N, M_G, and T_tail; it preserves Wilson normalization, reflection symmetry, null cancellations, cutoff uniformity, and same-theory observables; primitive operations are source differentiation, interval arithmetic, aggregation before clipping, color multiplication, and tail addition; equivalence is equality of regulated source data; transfer exports only I_gate. Conceptual value signal: sharp finite route change. Negative SU(N) endpoint cumulants are explanatory but not the obstruction; only positive-D leakage times a connected cumulant witness plus uniform tail can lower the finite gate. Clay continuum construction, gauge-invariant observable density, full OS/Wightman reconstruction, nontriviality, OS spectral transfer, and positive mass gap remain non-claimed.

## Gedanken Experiment Design Seed

- Need decision: `use_now_as_falsifier_probe`
- Rationale: The branch is looping unless endpoint-collapse intuition is converted into a finite source interval for the actual post-H,K scalar. A concrete heat-kernel endpoint experiment tests the one-sided screen without claiming continuum Yang-Mills.
- Situation seed: Fixed SU(N) heat-kernel plaquette-sheet three-hairpin endpoint block with one source-equivalent class c_* made increasingly 12-dominant while the other endpoint classes satisfy the half-overlap shield.
- Varied variable: eta=b_{12,c_*}/(b_{13,c_*}+b_{23,c_*}+10^{-12}), the positive-D leakage ratio of the selected endpoint class.
- Held-fixed controls: Same heat-kernel regulator, Wilson normalization, reflection map, and gauge-invariant observable algebra on collar and endpoint sides., Fixed H,K data, fixed Gaussian margin M_G, fixed color factor C_N, and no boundary counterterm., Uniform tail budget convention tau_tail and source-equivalence policy by regulated source derivatives., Endpoint cumulant witness obtained either by the root-quartic cap or by the seven-point same-theory source stencil.
- Expected observation: Below the critical eta the lower interval I_- remains nonnegative; above it a sufficiently negative connected cumulant witness can force I_+<0 and becomes a finite same-theory falsifier.
- Transfer certificate needed: Cutoff-uniform endpoint source intervals, equality of source-equivalent classes across refinements, and a valid tail bound before the thought experiment may promote or demote the finite OS gate.

## Next Experiment

Proof search plus targeted computation: enumerate source-equivalent endpoint classes of the fixed hairpin geometry, compute D_c, run the root-quartic cap and seven-point source stencil for every D_c>0 class, bound T_tail uniformly, and report the connected cumulant witness interval I_gate for promotion, falsifier, or continued quarantine.

# Annular Ward-Hessian constants for the H,K endpoint polarization

## Candidate Lemma

Conditional annular Ward-Hessian certificate for the connected boundary-OPE polarization R_{++}: if the same-theory flowed Wilson C4 sector constants are interval-enclosed and dominated by the positive pair covariance, then the finite H,K endpoint-box Schur-Feshbach plus channel is positive; if not, the R repair is quarantined.

## Definitions

- source object: the centered flowed Wilson hairpin covariance R_{++}^{ren}(t,eta,a,V)=\kappa_2(W_+^H(t)-\langle W_+^H(t)\rangle,W_+^K(t)-\langle W_+^K(t)\rangle) after disconnected-product, perimeter, and cusp subtraction in the Wilson lattice regulator.
- target object: the finite endpoint-box plus-channel quadratic form Q_+^{post}=Q_+^{bare}+\kappa_4 R_{++}^{ren}-L_+ governing the post-H,K Schur-Feshbach positivity test.
- controlled interface: endpoint sheet-current representation J_+ with M_{0,+}=M_{1,+}=0, mixed-Hessian annular constants A_s, and a recovery map from raw hairpin Wilson loops to centered flowed cumulants.
- same-theory condition: pair covariance, connected C4 sectors, counterterms, recovery errors, and L_+ are computed in one cutoff family and one gradient-flow renormalization prescription before any continuum interpretation.
- P_{++}:=2(N^2-1)G_{++} is the positive two-curvature cross-pairing of the two plus-channel endpoint sheet currents.
- C_{4,s}^{WS} denotes a Ward-subtracted connected four-curvature sector with s in {3g,4g,ct,end}.
- A_s^+ is an outward-rounded upper interval for the mixed endpoint Hessian norm of sector s, including near cells and compressed far annuli.
- E_{rec}^+ is the certified upper error of replacing raw Wilson hairpins by endpoint sheet-current flowed cumulants.

## Assumptions

- Model: four-dimensional SU(N) Wilson lattice Yang-Mills on a finite periodic box, with gradient-flow observables at positive flow time t.
- Regime: endpoint cell diameter eta satisfies eta <= c sqrt(t), endpoint separation d satisfies d >= 4 sqrt(t), and H,K geometry is fixed.
- Cutoff: constants are required uniformly for a << eta and V large enough that endpoint boxes and first annuli do not wrap.
- Same-theory: no sector may be imported from a different gauge fixing, action, flow scheme, or normalization.
- Local: only the finite H,K endpoint boxes and their dyadic annuli are used; this does not assert a continuum OS theory.
- Validity: Ward and cusp subtractions must be verified before using Hessian moment cancellation.
- Constraint: zero-pairing quotienting is allowed only after an interval certificate that the pair form changes by zero within outward rounding.

## Equations

- R-sector-decomposition: `R_{++}^{ren}=g_t^4\,2(N^2-1)G_{++}+g_t^6\,N(N^2-1)\sum_{s}\sigma_s C_{4,s}^{WS}+E_{rec}`. Valid when: Valid when the centered flowed Wilson cumulant is expanded through the same Wilson regulator, with disconnected, perimeter, cusp, and Ward counterterms already subtracted.
- annular-Hessian-majorant: `|C_{4,s}^{WS}|\le M_{2,+}^2\left(A_{s,near}^{+}+\sum_{J_0\le J\le J_1}A_{s,J}^{+}+A_{s,J_1}^{+}\frac{q_s}{1-q_s}\right),\quad q_s=2^{4-2\nu_s}<1`. Valid when: Applies after plus-channel monopole and dipole moments vanish and the sector kernel has annular Hessian decay exponent nu_s greater than two.
- certified-lower-bound: `R_{++}^{ren}\ge g_t^4\,2(N^2-1)G_{++}^{-}-g_t^6\,N(N^2-1)M_{2,+}^2\sum_s A_s^{+}-E_{rec}^{+}=:R_{++}^{-}`. Valid when: Requires outward-rounded intervals for the pair baseline, all Ward-subtracted sector Hessians, and the raw-hairpin recovery error in the same cutoff theory.
- endpoint-promotion-margin: `\Delta_R^{-}:=\kappa_4 R_{++}^{-}-L_+>0\ \Longrightarrow\ Q_+^{post}>0`. Valid when: Valid only for the finite H,K Schur-Feshbach endpoint box with the leakage L_+ computed from the same finite matrix decomposition.

## Attempted Derivation

- Conceptual pressure attacked: finite Schur-Feshbach endpoint positivity needs a same-theory Wilson mediator, while positive pair covariance and flowed recovery may both be valid yet connected C4 can erase R_{++}.
- Use the Wilson lattice regulator with positive gradient flow time t; represent each H,K hairpin by endpoint sheet currents plus a certified recovery error from raw centered Wilson loops.
- Expand the centered covariance of the two plus hairpins: disconnected products cancel, one-hairpin perimeter and cusp terms cancel, and the Gaussian two-curvature cross-pairing gives P_{++}=2(N^2-1)G_{++}>0.
- Decompose the remaining connected boundary-OPE polarization into Ward-subtracted sectors 3g, 4g, ct, and end, each with color N(N^2-1) and sector sign sigma_s.
- Apply plus-channel monopole and dipole cancellation to remove constant and gradient Taylor terms of each sector kernel, leaving mixed Hessian bounds weighted by M_{2,+}^2.
- Split endpoint-cell pairs into near cells and dyadic annuli; enclose near cells by direct interval quadrature and compress the far tail by q_s=2^{4-2nu_s}<1.
- Combine intervals into R_{++}^{-} and compare kappa_4 R_{++}^{-} against the finite Schur-Feshbach leakage L_+.

Blocking gap: The proof still lacks outward-rounded numerical or analytic enclosures for A_{3g}, A_{4g}, A_{ct}, A_{end} and a cutoff-uniform recovery error E_rec^+ for the exact H,K geometry.

## Falsifiers

- Ward subtraction fails for one sector, leaving an uncancelled monopole or dipole term in C4.
- The cusp or perimeter subtraction depends on the hairpin partner and is not a one-hairpin counterterm.
- A sector has nu_s<=2 or an observed annular ratio q_s>=1, so the far tail is not summable.
- The positive pair baseline G_{++}^{-} is zero because the H,K plus geometry has zero cross-pairing.
- The recovery error E_rec^+ is of the same size as or larger than the pair baseline.
- The dominance margin Delta_R^- is nonpositive in every stable flow-time plateau.
- The same-theory condition fails because pair and C4 constants are computed with different regulators, gauge fixings, or normalizations.
- A connected cumulant witness survives only at finite cutoff and disappears under the required centered flowed normalization.

## Learning

Cycle 344 turns the endpoint polarization into a sharper finite object: a same-theory flowed Wilson connected cumulant with pair color 2(N^2-1), C4 sector color N(N^2-1), Ward/cusp cancellation, plus-moment Hessian reduction, annular tail compression, recovery errors, and a single dominance margin Delta_R^-. The declarative tension is explicit: endpoint Schur-Feshbach positivity, positive flowed pair covariance, and same-theory recovery must jointly hold, but connected C4 may erase the mediator. Raw Wilson contours are fragmented; endpoint sheet currents are the efficient carrier because they encode H,K sheets, endpoint moments, sector kernels, counterterms, recovery errors, and L_+, preserve gauge/color/reflection/orientation/cutoff/locality/same-theory invariants, use cumulant expansion, Ward subtraction, Taylor Hessians, dyadic intervals, outward rounding, and zero-pairing equivalence, and expose falsifiers. The result is sharp at finite scope and leaves every Clay gate untouched.

## Gedanken Experiment Design Seed

- Need decision: `Design now as a falsifier probe for the finite endpoint-box certificate.`
- Rationale: The branch has already reduced R_{++} to annular sector constants; another abstract restatement would not decide whether C4 erases the positive pair covariance.
- Situation seed: SU(2) Wilson lattice Yang-Mills on periodic boxes with fixed H,K plus-channel hairpin endpoint geometry, gradient-flowed clover curvature, boundary point splitting, centered Wilson hairpin covariance, and Ward/cusp subtraction; compute pair baseline and C4 sector intervals on dyadic annuli.
- Varied variable: flow-time ratio tau=t/d^2 while holding the physical endpoint separation d fixed.
- Held-fixed controls: Same Wilson action, same bare-coupling matching prescription, and same centered flowed cumulant normalization., Same H,K endpoint sheet-current geometry, plus-channel orientation, and zero-pairing quotient certificate., Same annular partition, outward-rounded interval arithmetic, and Schur-Feshbach leakage L_+.
- Expected observation: A valid plateau should show stable G_{++}^{-}, decreasing sector ratios rho_s<1, and a positive Delta_R^- over a nonempty tau interval; persistent negative Delta_R^- is a falsifier for this endpoint repair.
- Transfer certificate needed: Before intuition affects proof obligations, one needs cutoff- and volume-stable interval enclosures for all sector constants, verified Ward/cusp cancellation, certified recovery from raw Wilson hairpins, and same-theory normalization of kappa_4 and L_+.

## Next Experiment

Route to proof search: compute outward-rounded reference-annulus intervals for A_{3g}, A_{4g}, A_{ct}, and A_{end} in the same-theory flowed Wilson cumulant; verify plus-moment Ward cancellation and recovery error; report Delta_R^- as a connected cumulant witness-style finite falsifier for the H,K endpoint gate.

# Raw signed-orbit K4 stress certificate for finite H,K endpoint PSD

## Candidate Lemma

Finite signed-orbit stress lemma: in one heat-kernel cutoff Yang-Mills endpoint box, diagonal upper intervals and one phased off-diagonal lower interval for the raw connected K4 cumulant give a valid falsifier for the post-H,K Schur-corrected endpoint positivity gate whenever D_p^+<0 or L_{pq}(theta)^2>D_p^+D_q^+.

## Definitions

- source object: the finite heat-kernel regulated SU(N) Wilson endpoint data consisting of oriented plaquette sheets, transported color tensors, the Gaussian flux covariance C_sigma, raw connected four-curvature cumulant intervals I_o, OPE error intervals, and the H,K Schur block S_HK at cutoff a and smoothing sigma.
- target object: the finite Hermitian endpoint quadratic form U_sigma on the vacuum-subtracted Wilson endpoint basis after Schur-Feshbach subtraction, whose PSD is the local Route A endpoint-box gate and not a Hamiltonian mass-gap statement.
- controlled interface: a signed-orbit recovery map Rec_sigma sending raw plaquette K4 orbit intervals, Gaussian color contractions, OPE budgets, and Schur data to interval bounds D_i^+ and L_ij(theta) for two-sparse Rayleigh stress tests.
- same-theory condition: all entries of C_sigma, I_o, E_OPE, and S_HK are computed from the same cutoff action, regulator, Wilson endpoint geometry, coupling normalization, and reflection convention; no OS Hilbert observable algebra or gauge-invariant observable density transfer is used.
- bridge/carrier: the connected cumulant witness R_ij=cum_2(:Q_i^2:,:Q_j^2:) with Q_i the transported plaquette-sheet curvature flux associated to endpoint i.
- declarative tension: Wilson/OPE coefficients, non-Gaussian K4 intervals, OPE remainder, and Schur hairpin energy must jointly control one finite endpoint quadratic form, but continuum OS reconstruction, excitation-sector cyclicity, and mass gap transfer remain forbidden conclusions.
- carrier critique: scalar R is too weak, A012 shells lose phases, full Delta_raw is complete but expensive, and signed raw orbits are efficient because they preserve Hermiticity, exact Wilson quotienting, gauge invariance, and same-theory normalization.
- efficient representation requirements: encode oriented plaquettes, sheet weights, heat-kernel transporters, color tensors, cumulant intervals, OPE intervals, endpoint phases, and Schur blocks; preserve gauge invariance, reflection support, Hermiticity, Gaussian/K4 separation, exact quotient identities, and same-theory normalization; support cumulant contraction, phase interval summation, Rayleigh stress search, Loewner bounds, and Schur subtraction; quotient only by exact Wilson identities; keep finite endpoint-box complexity; transfer only through tau, Delta_raw, or x_stress; demote on negative margin, missing intervals, non-invariant quotienting, OPE overflow, or regulator mismatch.

## Assumptions

- Model: finite-volume heat-kernel lattice or cellular SU(N) Yang-Mills regulator with reflection-compatible endpoint boxes and fixed Wilson H,K geometry.
- Cutoff: a>0, sigma/a bounded in the OPE-valid collar regime, and all plaquette sums are finite before any continuum limit is considered.
- Same-theory: Gaussian covariance, raw K4 intervals, OPE errors, Wilson normal ordering, and H,K Schur subtraction use the same action, coupling, regulator, volume, boundary convention, and endpoint basis.
- Validity: raw K4 orbit intervals are rigorous enclosures for the connected four-curvature cumulant after the same vacuum/perimeter/disconnected cumulant cancellation used in the Wilson expansion.
- Local: the claim concerns only the finite post-H,K endpoint-box PSD gate; OS/Wightman reconstruction, nontrivial continuum limit, gauge-invariant observable density, and physical-unit spectral transfer are untouched.
- Uniformity: no volume-uniform or cutoff-uniform RG basin entry is assumed; any promotion beyond this finite gate requires separate large-field, topology, and regulator-independence controls.

## Equations

- Schur-corrected endpoint matrix: `U_{\sigma}=G_{\sigma}+K^{(4)}_{\sigma}+E^{\mathrm{OPE}}_{\sigma}-S_{HK,\sigma}`. Valid when: Valid when the heat-kernel cutoff endpoint box and Schur blocks are finite, same-regulator, and Hermitian.
- Gaussian Wilson contraction: `G_{ij}=\alpha_N g_R^4\,(C_{\sigma}\circ \overline{C_{\sigma}})_{ij},\qquad \alpha_N=(N^2-1)/(8N^2)`. Valid when: Valid when the boundary OPE is truncated after the crossed two-curvature contraction with transported SU(N) traces normalized identically.
- signed raw K4 orbit recovery: `K^{(4)}_{ij}\in {g_R^4\over 16N^2}\sum_{o\in \mathcal O_{ij}} m_o\,\beta_o\,I_o,\qquad I_o=[a_o,b_o]`. Valid when: Valid when exact Wilson trace identities and endpoint symmetries define the orbit quotient without losing orientation phases.
- phased off-diagonal lower bound: `L_{pq}(\theta)=\max\{0,\operatorname{Re}(e^{-i\theta}(G_{pq}-S_{pq}))+{g_R^4\over16N^2}\sum_o m_o\ell_o(\theta)-e^{\mathrm{OPE}}_{pq}\}`. Valid when: Valid when each \ell_o(theta) is the interval lower endpoint of Re(e^{-itheta} beta_o I_o) in the same regulator.
- two-sparse falsifier gate: `D_p^+<0\quad\hbox{or}\quad L_{pq}(\theta)^2>D_p^+D_q^+\;\Longrightarrow\; U_{\sigma}\not\succeq0`. Valid when: Valid when D_i^+ are rigorous diagonal upper bounds and L_pq(theta) is a rigorous lower bound on |U_pq|.

## Attempted Derivation

- Freeze the Clay target boundary: this branch claims neither OS/Wightman reconstruction nor a Hamiltonian mass gap; it tests only the finite post-H,K endpoint PSD gate.
- Use the heat-kernel Wilson OPE for endpoint flux observables Q_i and Q_j; vacuum, perimeter, and disconnected pieces cancel in cum_2(:Q_i^2:,:Q_j^2:).
- Decompose R_ij into the positive Gaussian crossed-curvature color square, the raw connected K4 orbit sum, and an OPE interval in the same cutoff theory.
- Subtract the Schur hairpin block S_HK obtained from the same endpoint basis to form U_sigma.
- For a two-sparse vector x=e_p-z e_q, Hermitian PSD implies U_pp>=0, U_qq>=0, and |U_pq|^2<=U_pp U_qq.
- Replace U_pp and U_qq by rigorous diagonal upper bounds D_p^+,D_q^+ and replace |U_pq| by a phased lower bound L_pq(theta) recovered from signed raw K4 orbits.
- Conclude that D_p^+<0 or L_pq(theta)^2>D_p^+D_q^+ contradicts PSD and supplies a valid finite falsifier for the H,K endpoint route.

Blocking gap: The branch still lacks validator-facing same-regulator raw K4 orbit intervals I_o and tail/OPE enclosures for a concrete H,K endpoint pair.

## Falsifiers

- A same-regulator raw K4 computation gives D_p^+<0 for an endpoint diagonal; this is an immediate finite falsifier of endpoint PSD.
- A phased off-diagonal lower bound satisfies L_pq(theta)^2>D_p^+D_q^+ after OPE and Schur budgets; this gives a two-sparse stress falsifier.
- All signed orbit intervals are too small or phase-cancelled while OPE tails remain large; the negative tactic fails and the branch must move to full Delta_raw proof search or quarantine.
- Any mismatch between heat-kernel regulator, coupling normalization, endpoint geometry, or Schur block data invalidates the same-theory witness.
- A quotient audit finds that A012 or signed-orbit compression merged representatives with opposite phases; the proposed carrier is demoted as representation-limited.

## Learning

Cycle 344 attacks the conceptual pressure that raw non-Gaussian Wilson K4 cumulants need a mediator to a finite Schur-corrected endpoint PSD decision without OS-density circularity. The hard gate is D_i^+<0 or L_pq(theta)^2>D_p^+D_q^+: success gives a valid finite falsifier for the H,K endpoint gate, while failure gives no positivity and routes to full Delta_raw proof search or quarantine. The conceptual value signal is sharp and unifying at finite scope because Gaussian color positivity, connected K4 danger, OPE error, and Schur hairpin energy are combined in one same-theory connected cumulant witness, while continuum Schwinger coherence, OS positivity, gauge-invariant observable density, excitation-sector cyclicity, and physical-unit mass gap remain untouched.

## Gedanken Experiment Design Seed

- Need decision: `Use now as a falsifier probe and data-specification experiment, not as evidence for the Clay theorem.`
- Rationale: The branch has exhausted abstraction; the missing mediator is concrete same-regulator K4 interval data for a connected cumulant witness, so a target-preserving finite stress experiment specifies exactly what must be computed.
- Situation seed: Fix SU(3) heat-kernel lattice Yang-Mills on a finite reflection-symmetric endpoint box with the already chosen H,K collar/hairpin Wilson sheets; select two endpoint sheet-pair nodes p,q and one dominant signed plaquette-quadruple orbit crossing the boundary collar.
- Varied variable: rho_0, the signed interval center or lower endpoint for the dominant raw connected K4 orbit after exact Wilson quotienting.
- Held-fixed controls: Cutoff a, smoothing ratio sigma/a, heat-kernel action, coupling normalization g_R, and volume box., Endpoint H,K geometry, plaquette-sheet weights, Schur block S_HK, Gaussian covariance C_sigma, and OPE error budget., Exact Wilson quotient policy, orientation phases, reflection convention, and color trace normalization.
- Expected observation: As rho_0 is varied through its rigorous interval, the phased lower bound L_pq(theta) either crosses the threshold sqrt(D_p^+D_q^+) and yields a finite falsifier, or it remains below threshold and forces full Delta_raw proof search.
- Transfer certificate needed: A validator-facing certificate containing the raw K4 orbit interval for rho_0, a rigorous bound on all non-dominant orbit tails, exact quotient audit, and same-regulator Schur/OPE/Gaussian data before the thought experiment can affect proof obligations.

## Next Experiment

Proof search: compute the first validator-facing raw signed-orbit K4 interval for a concrete H,K endpoint pair in the heat-kernel regulator, then evaluate D_i^+<0 and L_pq(theta)^2>D_p^+D_q^+; if intervals are still missing, quarantine the branch rather than restating OS Hilbert observable algebra or scalar R.

