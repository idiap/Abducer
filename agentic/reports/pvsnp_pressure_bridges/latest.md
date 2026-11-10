<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Pressure Bridge Abstractions

- Target: `p-vs-np-target`
- Purpose: Convert P vs NP conceptual pressures and difficulty hypotheses into target-preserving bridge abstractions.

## Pressure Signals

- `advice_uniformity_leakage`: 8209
- `black_box_substitution_cap`: 2943
- `proof_complexity_transfer_gap`: 2861
- `naturalness_density_pressure`: 2555
- `meta_complexity_carrier_debt`: 1804
- `relativization_algebrization_boundary`: 1482
- `padding_projection_debt`: 1282
- `hardness_magnification_ceiling`: 84

## Recommended Next Move

- Bridge: `pvsnp-bridge-002` Searchable succinct meta-complexity certificate bridge
- Action: Run the symbolic or no-go handoff for this bridge before adding more exploratory cycles; the next cycle should compute an interface parameter, prove an obstruction theorem, or demote the bridge.
- Payoff criterion: Show that accepted certificate pairs exist in every kappa-gap interval, have O(m)-bit descriptions, are searchable in 2^{O(m)}, and soundly imply CC(f_u)>2^{epsilon m}.
- Stop condition: Backtrack if certificate existence is equivalent to the target lower bound or if searchability destroys the target class.
- Skills: pvsnp-qualitative-complexity-reasoner, pvsnp-symbolic-complexity-auditor, paper-contribution-readiness-judge

## Bridge Candidates

### pvsnp-bridge-002 - Searchable succinct meta-complexity certificate bridge

- Priority score: `12568`
- Pressures: `meta_complexity_carrier_debt`, `advice_uniformity_leakage`, `naturalness_density_pressure`
- Difficulty hypothesis: The hard part is not defining MCSP; it is finding compact sound certificates whose existence is frequent enough to build a uniform language without making the accepted set large and constructive.
- Bridge abstraction: Use searchable certificates as the carrier instead of advised hard truth tables, so that uniform search rather than nonuniform choice selects the hard slice.
- Source object: sound O(m)-bit certificates for high MCSP/MKtP truth tables with bounded source-length gaps
- Target object: a uniform E or NP-adjacent language with explicit circuit lower bounds
- Controlled interface: Verifier V, decoder D, certificate length, verifier time, source gap kappa, soundness threshold epsilon, density of accepted codes, and deterministic search schedule.
- Proof obligation: Show that accepted certificate pairs exist in every kappa-gap interval, have O(m)-bit descriptions, are searchable in 2^{O(m)}, and soundly imply CC(f_u)>2^{epsilon m}.
- Symbolic probe: Audit delta<epsilon/kappa transfer and test whether certificate length or verifier time remains single-exponential in target length.
- When to persist: Persist if a named proof or meta-complexity object gives compact sound certificates with explicit gap coverage and no advice.
- When to pivot: Backtrack if certificate existence is equivalent to the target lower bound or if searchability destroys the target class.
- Paper-safe narrative: The proposed abstraction shifts attention from hard truth tables to uniformly searchable certificates of hardness, making advice leakage and naturalness the central tests.
- Falsifiers:
  - Accepted pairs exist only through advice or nonuniform selection.
  - Certificate length or verifier time becomes m^{1+Omega(1)} in the exponent and leaves E.
  - The accepted certificate set is dense, polynomial-time decidable, and useful, triggering natural-proof pressure.

### pvsnp-bridge-004 - Sparse non-natural property bridge

- Priority score: `12246`
- Pressures: `naturalness_density_pressure`, `relativization_algebrization_boundary`, `advice_uniformity_leakage`
- Difficulty hypothesis: The route is hard because usefulness against a rich circuit class plus efficient constructivity tends to create a natural property unless largeness or constructivity is explicitly broken.
- Bridge abstraction: Constrain the property to be nonlarge, sparse, nonconstructive in the forbidden sense, or proof-system mediated, while preserving enough usefulness to imply the target lower bound.
- Source object: truth-table or meta-complexity property intended to be useful against polynomial-size circuits
- Target object: non-natural lower-bound evidence compatible with cryptographic pseudorandomness barriers
- Controlled interface: Property density, constructivity time, usefulness class, PRF assumption, and whether the property is defined on all truth tables or a sparse valid slice.
- Proof obligation: Prove either non-largeness, nonconstructivity, or a proof-mediated escape while retaining a formal implication from property membership to target lower bound.
- Symbolic probe: Build a natural-proof ledger with largeness, constructivity, usefulness, and PRF-status fields for the candidate property.
- When to persist: Persist only if the property names exactly which natural-proof premise fails and how usefulness survives.
- When to pivot: Pivot to barrier exposition or no-go if largeness, constructivity, and usefulness all remain present.
- Paper-safe narrative: The bridge must show where naturalness is avoided, not merely assert that the route is non-natural.
- Falsifiers:
  - The property is dense and decidable in polynomial time over truth tables.
  - Usefulness is stated only for a weaker circuit class than the target route needs.
  - The sparse slice has no transfer certificate back to the target theorem.

### pvsnp-bridge-005 - All-exponent quantifier-lift bridge

- Priority score: `9575`
- Pressures: `hardness_magnification_ceiling`, `padding_projection_debt`, `advice_uniformity_leakage`
- Difficulty hypothesis: The route is hard because a single barely-superlinear lower bound generally excludes only a fixed exponent window; all-polynomial separation needs a quantifier-lift mechanism.
- Bridge abstraction: Turn a bounded-window transfer into a cofinal family of source obligations, each indexed so that every target exponent c is eventually covered.
- Source object: a family of source lower bounds indexed by target exponent or padding parameter
- Target object: NP not subset P/poly, requiring exclusion of every fixed polynomial exponent
- Controlled interface: Index set, padding map, source lower-bound strength as a function of c, valid-length coverage, and uniformity of the family.
- Proof obligation: For every fixed c, construct a source instance with margin a_c and overhead q_c,beta_c satisfying a_c>q_c+beta_c c while preserving valid lengths and model identity.
- Symbolic probe: Use exact transfer audits across several symbolic c regimes and prove the parameter family is cofinal rather than finite.
- When to persist: Persist if the next step states a parameterized theorem covering arbitrary c with explicit overhead functions.
- When to pivot: Quarantine if the family only repeats the same bounded window or if each indexed source lower bound carries the original target difficulty.
- Paper-safe narrative: A convincing magnification bridge must carry the all-exponent quantifier, not merely improve a fixed numerical threshold.
- Falsifiers:
  - The source obligation for exponent c is already equivalent to excluding SAT circuits of exponent c.
  - Valid source lengths become sparse without a target-preserving coverage certificate.
  - Uniformity or advice changes with c in a way that weakens the target theorem.

### pvsnp-bridge-003 - Proof-complexity lower-bound certificate bridge

- Priority score: `7220`
- Pressures: `proof_complexity_transfer_gap`, `meta_complexity_carrier_debt`, `naturalness_density_pressure`
- Difficulty hypothesis: The route is hard because a proof certificate must be short enough to search or verify while still soundly certifying a semantic lower bound that is usually as hard as the target.
- Bridge abstraction: Treat proof objects as the medium connecting semantic circuit lower bounds to verifiable mathematical evidence, with the proof system acting as the controlled interface.
- Source object: lower-bound tautologies LB(u,s) in a specified Cook-Reckhow proof system
- Target object: circuit lower bounds or meta-complexity hardness statements connected to P vs NP
- Controlled interface: Tautology family, proof system, proof length bound, verifier complexity, semantic soundness of LB(u,s), and target lower-bound transfer.
- Proof obligation: For a named proof system Psys, formulate LB(u,2^{epsilon m}); prove that short Psys proofs imply searchable hardness witnesses, or prove that any such bridge would yield a route-specific no-go.
- Symbolic probe: Compute witness length, proof length, verifier overhead, and resulting target exponent margin before claiming transfer.
- When to persist: Persist if a concrete proof system and tautology family make the semantic soundness and search overhead explicit.
- When to pivot: Pivot by converting to an impossibility theorem if the bridge requires proof lower bounds as hard as the intended circuit lower bound.
- Paper-safe narrative: A proof-complexity bridge is valuable only if the proof object does more than rename semantic hardness; it must control how hardness evidence is verified and transported.
- Falsifiers:
  - The proof length needed is already exponential beyond the target class.
  - The tautology certifies only proof-system hardness, not circuit lower bounds for f_u.
  - The route collapses into known proof-complexity lower-bound conjectures without a new carrier interface.

### pvsnp-bridge-006 - Route-specific impossibility bridge

- Priority score: `5707`
- Pressures: `black_box_substitution_cap`, `padding_projection_debt`, `relativization_algebrization_boundary`
- Difficulty hypothesis: Some branches are hard because their method class structurally loses the target quantifier; in that case the bridge is a negative theorem, not another positive search loop.
- Bridge abstraction: Treat persistent failure as a candidate obstruction theorem with precise hypotheses, excluded method class, escape conditions, and proof skeleton.
- Source object: a method class such as black-box SAT substitution, projection magnification, or relativizing counting diagonalization
- Target object: a theorem explaining why that method class cannot imply P != NP or NP not subset P/poly under stated assumptions
- Controlled interface: Method-class axioms, exact target, transfer formula, barrier signature, and escape conditions not ruled out.
- Proof obligation: State and prove that every method satisfying the method-class axioms yields only a bounded exponent window, a sparse-length proxy, or a relativizing/algebrizing result.
- Symbolic probe: Derive the contradiction or cap using exact transfer formulas and check nonvacuity by listing a covered example and an escape example.
- When to persist: Persist if the theorem statement has nonvacuous examples, exact assumptions, and a new route-specific consequence.
- When to pivot: Reject if it only paraphrases natural proofs, relativization, or algebrization without a new controlled interface.
- Paper-safe narrative: A negative result can be a scientific contribution when it identifies the exact bridge condition under which a family of approaches loses the target.
- Falsifiers:
  - The theorem rules out methods broader than its hypotheses justify.
  - The obstruction is already a known barrier with no route-specific refinement.
  - An escape condition covers the active branch, so the no-go does not apply.

### pvsnp-bridge-001 - Subpolynomial nonblackbox interface bridge

- Priority score: `4309`
- Pressures: `black_box_substitution_cap`, `hardness_magnification_ceiling`, `padding_projection_debt`
- Difficulty hypothesis: The route is hard because positive query-length exponent beta converts any fixed epsilon source margin into only a finite SAT exponent window, so the bridge must remove or structurally transform the beta*c term.
- Bridge abstraction: Replace plain black-box SAT-oracle substitution by an interface whose target-circuit dependence is beta=0 or N^{o(1)}, or by a genuinely nonblackbox use of the target circuit that cannot be counted as N^{q+beta c} gate substitution.
- Source object: a barely-superlinear source carrier L_N with lower bound SIZE(L_N)>N^{1+epsilon}
- Target object: SAT lower bounds strong enough to imply NP not subset P/poly
- Controlled interface: State ordinary overhead q, target-query length exponent beta, adaptivity model, advice accounting, and whether the target circuit is used as a replaceable oracle gate or as a nonblackbox object.
- Proof obligation: Prove a transfer theorem in which SAT in SIZE(n^c) induces source circuits below N^{1+epsilon} for every fixed c, or prove a no-go theorem that every black-box interface with beta>0 gives only c<(1+epsilon-q)/beta.
- Symbolic probe: Run audit_transfer.py with exact a=1+epsilon, q, beta; promote only if beta=0 with positive margin or a certified nonblackbox escape is supplied.
- When to persist: Persist only if the next step computes q and beta for a named carrier and identifies the nonblackbox operation that blocks gate-by-gate substitution.
- When to pivot: Pivot to a no-go theorem if two named carriers still produce beta>0 or q>=1+epsilon under exact audit.
- Paper-safe narrative: The bridge problem is not the existence of a hard carrier alone, but the construction of an interface whose dependence on hypothetical SAT circuits does not reintroduce the target exponent.
- Falsifiers:
  - beta>0 and q<1+epsilon yields only a bounded exponent window.
  - q>=1+epsilon lets the interface consume the source lower-bound margin.
  - nonblackbox use is merely oracle substitution in disguise.

