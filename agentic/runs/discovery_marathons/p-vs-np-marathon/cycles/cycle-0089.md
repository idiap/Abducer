# cycle-0089

This research cycle converted active route pressure into typed branch lemmas. The main mathematical change is that each branch now names a source object, target object, equation, validity condition, falsifier, and next experiment. Only research-mode cycles with elapsed-time and branch-engine evidence count as genuine long-horizon research progress.

## Selected Branches

- `marathon.branch.bcdeffa51f87`
- `marathon.branch.4b0edf3359d1`
- `marathon.branch.138e68639c07`

## Branch Outputs

# Hardness-Magnification Bridge Realization

## Candidate Lemma

Conditional SR-constrained residual audit: for H_N^SAT and EF+SATeq+SR_h, any accepted lower-bound certificate that parses to an advice-free constrained residual decoder (D_pi,R_pi) is valid only if S_pi+|R_pi|N >= N^{1+epsilon-o(1)}; otherwise equality patching is a falsifier for the source lower bound.

## Definitions

- source object: H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), M_N<=N^{q+o(1)}, L_N=(log N)^d, generator size N^{rho+o(1)}.
- target object: short EF+SATeq+SR_h proof pi of Ckt(H_N^SAT)>N^{1+epsilon-o(1)} in nonuniform Boolean circuit size.
- controlled interface: parse pi to a quotient-label transcript obeying EqSAT links and h-depth SAT self-reduction OR constraints, plus a residual row decoder D_pi.
- target-preserving condition: q,rho<1+epsilon and SR closure size M_N2^h has exponent q_SR<1+epsilon, with no advice beyond the named transcript.

## Assumptions

- Circuit model is nonuniform Boolean circuits on N-bit source inputs; row patching uses equality tests for exceptional source rows.
- EF+SATeq+SR_h means EF plus equisatisfiability links and clauses y_F=OR_b y_{F|x_i=b} for at most h successive restrictions of L_N-bit formulas.
- Parser assumption: every accepted proof in the scoped subsystem yields an advice-free transcript of cost S_pi and a decoder D_pi whose errors are confined to Delta_SR_h(pi) rows.
- Soundness is SAT-semantic over real labels; the lemma audits proof methods and does not assert a lower bound for H_N^SAT or P != NP.

## Equations

- beta_zero_transfer: `C(H_N^{SAT}) \le N^{\rho+o(1)}+M_N L_N^c=N^{\max\{\rho,q\}+o(1)}`. Valid when: Applies when SAT has size L_N^c circuits and the carrier uses only polylogarithmic beta-zero target queries.
- row_patch_bound: `C(H_N^{SAT}) \le C(D_N)+O(|R_N|N)`. Valid when: Valid when D_N agrees with H_N^{SAT} on every source row outside the explicitly listed residual set R_N.
- sr_certificate_threshold: `\mathrm{ValidCert}_{SR_h}(\pi) \Rightarrow S_\pi+\Delta_{SR_h}(\pi)N \ge N^{1+\epsilon-o(1)}`. Valid when: Requires the scoped parser to turn pi into an advice-free SR-constrained residual decoder for the same carrier.

## Attempted Derivation

- Quotient formulas by EqSAT links, then add SR_h constraints for restrictions in the generated polylog formula closure; real SAT labels satisfy all constraints.
- Assume a parser maps any short accepted proof pi to a functional transcript and decoder D_pi over constrained quotient labels, with cost S_pi and residual row set R_pi.
- Apply row patching: hardwire R_pi and correct D_pi by equality gates, giving C(H_N^SAT)<=S_pi+O(|R_pi|N).
- Therefore a proof certificate at threshold N^{1+epsilon-o(1)} must force |R_pi|>=N^{epsilon-o(1)} unless S_pi already exceeds the source threshold.

Blocking gap: The missing proof is semantic-to-residual parsing for full EF+SATeq+SR_h; SR OR clauses couple labels across restrictions, so independent occurrence-label spoofing is not valid.

## Falsifiers

- Low constrained row distance Delta_SR_h(pi)<N^{epsilon-o(1)} with S_pi<N^{1+epsilon-o(1)} is a direct row-patching falsifier.
- SR closure overhead M_N2^h=N^{q_SR+o(1)} with q_SR>=1+epsilon collapses the beta-zero target-preserving window.
- A parser using nonuniform advice to list residual rows or semantic links invalidates the claimed advice-free certificate transfer.
- A genuinely SAT-semantic EF inference outside EqSAT+bounded-SR blocks the constrained parser and quarantines this scoped no-go.

## Learning

The cycle upgrades the SR semantic escape into a quantitative constrained-distance invariant. Occurrence spoofing is invalid after SR constraints, but any bounded-SR parser still faces the same row-patching threshold. Progress is route-level certification, not a P vs NP proof.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: Cycle 88 found self-reduction as a concrete semantic escape; the route now needs a quantitative audit, not another barrier restatement.
- Situation seed: Use the beta-zero XOR carrier and close each generated formula under h levels of SAT self-reduction; test the best SR-constrained residual decoder for row parity.
- Varied variable: SR depth h, equivalently closure exponent eta with 2^h=N^{eta+o(1)}.
- Held-fixed controls: M_N=N^{q+o(1)} with q<1+epsilon and generator size N^{rho+o(1)} with rho<1+epsilon., Formula length L_N=(log N)^d, d>1, and all target SAT calls remain polylogarithmic., No advice leakage: transcripts must be uniformly parsed from pi and charged in S_pi.
- Expected observation: Either Delta_SR_h stays above N^{epsilon-o(1)}, supporting row-forcing, or a low-distance constrained decoder gives a reproducible falsifier for the certificate route.
- Transfer certificate needed: An advice-free parser pi -> (D_h,R_h) for EF+SATeq+SR_h and a proof that SR closure overhead remains below the source threshold.

## Next Experiment

Fix h with 2^h=N^{eta}; formalize Delta_SR_h for the generated formula closure and try to prove the parser for EF+SATeq+SR_h restricted to extension variables naming only quotient labels and SR clauses.

# Barrier-Aware Lower-Bound Route

## Candidate Lemma

For Psys=EF+SAT_U^subst proofs of LB(H_N^SAT,N^{1+epsilon}), promotion needs ExtensionRowRealizer: every accepted short proof has |K_pi|>=N^{epsilon-o(1)} or yields an advice-free residual D_pi agreeing with H off K_pi; small K_pi is then a falsifier by patching.

## Definitions

- source object: a poly(N)-length EF+SAT_U^subst proof pi of the propositional lower-bound sentence LB_{N,s}(H_N^SAT) with s=N^{1+epsilon-o(1)}.
- target object: the beta-zero SAT parity function H_N^SAT on N bits, with M_N=N^{q+o(1)} polylog-length SAT rows generated by uniform G_N.
- controlled interface: ExtensionRowRealizer(pi) outputs semantic row support K_pi and residual circuit D_pi, closed under formula equality and extension substitution inside SAT atoms.
- target-preserving condition: K_pi is uniformly enumerable from pi,N and D_pi is advice-free, so patching K_pi gives a genuine circuit for H_N^SAT below the claimed source threshold.

## Assumptions

- Psys is EF plus uniform SAT_U axioms, formula-equality reasoning, and extension substitution into SAT atoms; no hidden row advice is allowed.
- G_N has size N^{rho+o(1)}, M_N=N^{q+o(1)}, row length (log N)^d, and the source claim is C(H_N^SAT)>N^{1+epsilon-o(1)}.
- Semantic support counts generator rows whose SAT truth value can affect an atom after all substitutions, not syntactic occurrences before substitution.
- The residual D_pi must compute the XOR of all rows outside K_pi, not merely pass ordinary proof soundness or local consistency.

## Equations

- beta0_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j))`. Valid when: Valid when G_N is the fixed uniform beta-zero generator with M_N=N^{q+o(1)} polylog-length SAT rows.
- semantic_support: `K_\pi=\{j\le M_N:\exists A\in SATAtoms(\pi)\ \Delta_j SAT(A)\ne 0\}`. Valid when: Applies after SAT atoms are interpreted semantically over generator rows and extension substitutions are closed in the same proof system.
- residual_patch: `C(H_N^{SAT})\le S(D_\pi)+O(|K_\pi|N)`. Valid when: Requires D_pi compute the outside-row XOR and each omitted polylog SAT row be patched by uniform brute force.

## Attempted Derivation

- Fix Psys=EF+SAT_U^subst and parse every SAT atom after extension expansion into semantic dependence on the generator rows G_N(x,j).
- Assume ExtensionRowRealizer with |K_pi|<=N^{epsilon-eta} and S(D_pi)<=N^{1+epsilon-eta}; patching gives C(H_N^SAT)<=N^{1+epsilon-O(eta)}.
- Thus a valid short proof of the source lower bound must either pay semantic row support N^{epsilon-o(1)} or become a sparse-residual falsifier to the claimed source lower bound.
- Substitution into a single SAT atom can hide many generator rows, so occurrence transcripts are invalid unless semantic support or a row-syntax realizer is proved.

Blocking gap: ExtensionRowRealizer for arbitrary EF SAT atoms: convert semantic support after substitution into an advice-free residual D_pi without assuming occurrence locality or generator-local closure.

## Falsifiers

- SAT-composition axiom: one atom SAT(Compose(G_N,x)) can mention all rows semantically while the occurrence parser sees only one formula occurrence.
- Shared extension variable E(x) abbreviating the whole row tuple makes private-label row forcing invalid unless support is semantic, not syntactic.
- Sparse K_pi without uniform enumeration is a falsifier to patching; hidden nonuniform row advice can fake an accepted certificate.
- If S(D_pi)>=N^{1+epsilon-o(1)}, the residual inequality is valid but gives no contradiction, so the sparse-support attack loses force.

## Learning

Cycle 89 fixes the strong system and moves the fork from occurrence parsing to semantic support. The exact contribution target is ExtensionRowRealizer: large semantic row charge or sparse-residual falsifier. Substitution is the named obstruction, not generic barrier folklore.

## Gedanken Experiment Design Seed

- Need decision: `design_now`
- Rationale: The top proof gap is concrete: extension substitution may compress rows. Varying semantic fan-in tests whether the row-support invariant, not occurrence count, controls transfer.
- Situation seed: Define an EF+SAT_U^subst proof skeleton with one extension atom A_t(x)=SAT(CL verifier for XOR of the first t generator rows), used inside LB(H_N^SAT).
- Varied variable: semantic fan-in t, from polylog(N) to N^{epsilon} and then to M_N.
- Held-fixed controls: G_N remains the same uniform beta-zero generator and row length is (log N)^d., The claimed source threshold stays C(H_N^SAT)>N^{1+epsilon-o(1)}., No nonuniform row advice is permitted in the residual circuit., The proof system rules are fixed to EF+SAT_U^subst with formula equality and substitution.
- Expected observation: Occurrence width stays one while semantic support grows as t. For t<N^{epsilon-o(1)}, a real residual should patch below threshold; for t>=N^{epsilon-o(1)}, the proof pays row charge.
- Transfer certificate needed: A formal ExtensionRowRealizer proving that A_t either exposes K_pi={1,...,t} uniformly or supplies D_pi for the outside-row XOR; otherwise the intuition cannot enter proof obligations.

## Next Experiment

Instantiate A_t with a Cook-Levin XOR verifier, compute K_pi exactly for t=polylog,N^{epsilon/2},N^{epsilon}, and test whether uniform D_pi for outside-row XOR follows or is blocked by SAT-composition.

# MCSP / Meta-Complexity Carrier Transfer

## Candidate Lemma

Cook-Reckhow witnessed-extensionality guard: any beta-zero SAT-parity proof whose formula identities have advice-free adaptive-cover witnesses either yields the low-cover circuit upper bound for H_N^SAT or uses an unwitnessed SAT-extensionality rule outside the valid carrier interface.

## Definitions

- source object: a short CR_wExt proof pi of a lower-bound sentence for H_N^SAT(x)=xor_{j<=M_N} SAT(G_N(x,j)), with M_N=N^{q+o(1)} and L_N=(log N)^d.
- target object: an unrestricted Boolean circuit for H_N^SAT, or a certified semantic-escape obstruction for the parser-to-query theorem.
- controlled interface: parse pi into occurrence SAT queries, witnessed formula-equality quotients, forced-row set F_N, residual set R_N, and adaptive-cover exponent alpha_ext.
- target-preserving condition: every formula identity or extension-variable congruence used by pi is witnessed inside the same advice-free proof with cover alpha_ext; no unwitnessed SAT-extensionality oracle is allowed.

## Assumptions

- Model is nonuniform circuit size for the target upper bound, but extraction of the transcript and quotient is uniform and advice-free from pi.
- Generator G_N has circuit size N^{rho+o(1)} and produces polylog-length SAT instances; row patch circuits may hardwire residual row data.
- ForcedRows means row parity is constant over all completions respecting the parsed local SAT facts and witnessed equality quotient.
- The lemma is route-level: it falsifies low-cover carriers; it is not a lower bound and not a proof of P != NP.

## Equations

- beta0_carrier: `H_N^{SAT}(x)=\bigoplus_{j\le M_N} SAT(G_N(x,j)),\quad M_N=N^{q+o(1)},\ L_N=(\log N)^d`. Valid when: Valid when the beta-zero source family and generator overhead are fixed before parsing proofs.
- guard_cap: `\alpha_{guard}=\max\{\rho,\ q+\alpha_{ext},\ \max(f,r)+1\}`. Valid when: Applies after forced rows, residual rows, and witnessed equality covers have named exponents.
- patch_upper_bound: `C(H_N^{SAT})\le N^{\alpha_{guard}+o(1)}`. Valid when: Requires the target-preserving extraction to be advice-free and all semantic identities witnessed.

## Attempted Derivation

- Parse pi into occurrence queries and build the quotient graph whose edges are witnessed formula identities, extension definitions, or congruence certificates.
- Contract the quotient; each representative has at most N^{alpha_ext+o(1)} adaptive-cover cost, so evaluating all M_N rows costs N^{q+alpha_ext+o(1)} plus generator overhead.
- For forced rows use the parsed parity value; for unforced or residual rows hardwire a row patch of size O((|F_N|+|R_N|)N), giving exponent max(f,r)+1.
- Conclude the stated upper bound; if a proof step uses unwitnessed SAT-extensionality, the parser has no same-theory witness and the derivation stops at a named semantic escape.

Blocking gap: Need a referee-checkable formal syntax for CR_wExt witnesses and a polynomial-time extractor from pi to the adaptive quotient graph.

## Falsifiers

- falsifier: alpha_ext+q < claimed lower-bound exponent minus o(1), because the witnessed quotient already gives a smaller circuit for H_N^SAT.
- falsifier: |R_N| or |F_N| below N^{epsilon-o(1)}, because row patching costs only N^{max(f,r)+1+o(1)}.
- falsifier: an MCSP/MKtP selector chooses a hard row using advice; this identifies nonuniform hardness but not an advice-free target language.
- falsifier: unwitnessed SAT-extensionality appears; the route has changed to a semantic-oracle proof system rather than a valid controlled carrier.

## Learning

Cycle 89 sharpens the fork: witnessed formula identity is not a new proof-system escape; it is charged by alpha_ext and yields the same low-cover upper-bound falsifier. The only remaining escape is unwitnessed SAT-extensionality, which must be treated as a semantic-oracle rule unless replaced by an advice-free quotient witness.

## Gedanken Experiment Design Seed

- Need decision: `design-now`
- Rationale: The live fork is concrete: does formula identity enter through extractable witnesses with a measurable cover, or through an unwitnessed SAT-semantic rule that defeats occurrence parsing?
- Situation seed: A CR proof family for the beta-zero parity H_N^SAT where G_N emits pairs of polylog CNFs linked by extension-variable definitions; compare witnessed quotient proofs with one added unwitnessed SAT-extensionality axiom.
- Varied variable: alpha_ext, the adaptive-cover exponent of the formula-identity witness quotient.
- Held-fixed controls: M_N=N^{q+o(1)} and generator overhead N^{rho+o(1)} remain fixed., No advice is allowed in choosing rows, witnesses, or quotient representatives., Residual and forced-row exponents r and f are measured after the same parser., SAT instances stay polylogarithmic so row patching costs O(N) per row.
- Expected observation: For alpha_ext below the threshold, witnessed proofs collapse to the patch upper bound; replacing witnesses by unwitnessed extensionality removes the quotient and exposes the exact semantic escape.
- Transfer certificate needed: A uniform extractor that maps each CR_wExt proof to occurrence queries, equality quotient, forced rows, residual rows, and alpha_ext without using SAT truth advice.

## Next Experiment

Write the CR_wExt inference list and prove preservation of the extracted quotient, ForcedRows, and residual sets for extension introduction, substitution, congruence, and witnessed SAT-equivalence rules.
