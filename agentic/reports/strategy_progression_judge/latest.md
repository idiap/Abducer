<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Strategy Progression Judge

- Target: `p-vs-np-target`
- Window: `cycle-0145` to `cycle-0154`
- Decision: `continue_with_targeted_adaptation`
- Payoff potential: `high`
- Paper readiness: `not_ready`
- Alignment: `bridge_aligned`

## Current Strategy

- Route: quantitative transfer obstruction for hardness magnification
- Active object: source exponent a, overhead q, target-query exponent beta, and the target SAT exponent c

## What Progressed

- `cycle-0150` Cycle 150 closes a proof-delivery upgrade rather than rediscovering magnification: Qrep quotient compression is valid exactly as a batched, ranked, proof-carrying same-theory dictionary charged in Gamma_Qrep. The sharp falsifier is the first unranked, cyclic, advice-chosen, or hidden semantic merge. The result is a scoped parser/falsifier theorem and Formula Footprints supporting lemma; it does not prove H_N lower bounds or P != NP.
- `cycle-0151` Cycle 151 upgrades the batched Qrep patch with temporal prefix stability: quotient compression is valid only as append-only, ranked, proof-carrying dictionary use. The first pre-use, rebinding, cyclic, advice-chosen, or hidden semantic merge is an explicit falsifier, while full semantic pruning stays quarantined.
- `cycle-0152` Cycle 152 upgrades Qrep from an append-only convention to a prefix-verifiable rule case: quotient compression preserves the transparent parser only when certificate charge strictly precedes representative use. The exact no-go is temporal, not just acyclicity; delayed same-theory evidence is already a private-row falsifier. This closes a proof-audit loophole while preserving the nonclaim boundary: no H_N lower bound and no P != NP result.
- `cycle-0153` Cycle 153 upgrades Qrep from prefix-verifiable syntax to a theorem-shaped TransparentRowSupport_N rule case: quotient compression is valid exactly as strict-prefix, ranked, proof-carrying, dependency-closed dictionary use. The new falsifier is temporal; delayed same-theory evidence is already hidden support. This is a scoped parser/falsifier contribution, not a lower bound for H_N and not P != NP progress.
- `cycle-0154` Cycle 154 converts strict-prefix Qrep from a syntax convention into a replay theorem with a matching temporal falsifier. The valid contribution is a restricted TransparentRowSupport_N rule case and Formula Footprints supporting lemma: charged, ranked, dependency-closed dictionary compression preserves Gamma line induction; delayed or hidden compression is exactly hidden support. This is route-level certification only, not a lower bound for H_N and not P vs NP progress.

## What Did Not Progress

- `cycle-0154` The derivation does not cover arbitrary semantic SAT branch pruning or FormulaEval rules whose influencing rows are not determined by proof syntax before use; this is exactly RealSATInfluenceRealizer_N^{arb}.

## Novelty And High-Reward Avenues

### pvsnp-bridge-002

- Avenue: Searchable succinct meta-complexity certificate bridge
- Novelty signal: Use searchable certificates as the carrier instead of advised hard truth tables, so that uniform search rather than nonuniform choice selects the hard slice.
- Reward condition: Show that accepted certificate pairs exist in every kappa-gap interval, have O(m)-bit descriptions, are searchable in 2^{O(m)}, and soundly imply CC(f_u)>2^{epsilon m}.
- Step-back/pivot condition: Backtrack if certificate existence is equivalent to the target lower bound or if searchability destroys the target class.
- Why it matters: The proposed abstraction shifts attention from hard truth tables to uniformly searchable certificates of hardness, making advice leakage and naturalness the central tests.

### pvsnp-bridge-004

- Avenue: Sparse non-natural property bridge
- Novelty signal: Constrain the property to be nonlarge, sparse, nonconstructive in the forbidden sense, or proof-system mediated, while preserving enough usefulness to imply the target lower bound.
- Reward condition: Prove either non-largeness, nonconstructivity, or a proof-mediated escape while retaining a formal implication from property membership to target lower bound.
- Step-back/pivot condition: Pivot to barrier exposition or no-go if largeness, constructivity, and usefulness all remain present.
- Why it matters: The bridge must show where naturalness is avoided, not merely assert that the route is non-natural.

### pvsnp-bridge-005

- Avenue: All-exponent quantifier-lift bridge
- Novelty signal: Turn a bounded-window transfer into a cofinal family of source obligations, each indexed so that every target exponent c is eventually covered.
- Reward condition: For every fixed c, construct a source instance with margin a_c and overhead q_c,beta_c satisfying a_c>q_c+beta_c c while preserving valid lengths and model identity.
- Step-back/pivot condition: Quarantine if the family only repeats the same bounded window or if each indexed source lower bound carries the original target difficulty.
- Why it matters: A convincing magnification bridge must carry the all-exponent quantifier, not merely improve a fixed numerical threshold.

### pvsnp-bridge-003

- Avenue: Proof-complexity lower-bound certificate bridge
- Novelty signal: Treat proof objects as the medium connecting semantic circuit lower bounds to verifiable mathematical evidence, with the proof system acting as the controlled interface.
- Reward condition: For a named proof system Psys, formulate LB(u,2^{epsilon m}); prove that short Psys proofs imply searchable hardness witnesses, or prove that any such bridge would yield a route-specific no-go.
- Step-back/pivot condition: Pivot by converting to an impossibility theorem if the bridge requires proof lower bounds as hard as the intended circuit lower bound.
- Why it matters: A proof-complexity bridge is valuable only if the proof object does more than rename semantic hardness; it must control how hardness evidence is verified and transported.

### pvsnp-bridge-006

- Avenue: Route-specific impossibility bridge
- Novelty signal: Treat persistent failure as a candidate obstruction theorem with precise hypotheses, excluded method class, escape conditions, and proof skeleton.
- Reward condition: State and prove that every method satisfying the method-class axioms yields only a bounded exponent window, a sparse-length proxy, or a relativizing/algebrizing result.
- Step-back/pivot condition: Reject if it only paraphrases natural proofs, relativization, or algebrization without a new controlled interface.
- Why it matters: A negative result can be a scientific contribution when it identifies the exact bridge condition under which a family of approaches loses the target.


## Paper Contribution Readiness

- Smallest honest claim: A contribution-shaped claim has not yet been stabilized; the next bounded step must name the source object, target object, validation burden, and overclaim boundary.
- Novelty argument: Novelty must be established against the target literature before paper claims are made.
- Main problem implication: The candidate must state how it changes the main target's route priority, validation burden, or obstruction map.

## Alignment

- Handoff: Source: latest cycle window and bridge candidates. Target: P != NP or an explicitly scoped lower-bound/nonuniform separation consequence.
- Transfer risk: The branch remains aligned only if its carrier, barrier escape, or transfer formula preserves uniformity, valid lengths, and the all-exponent target rather than proving a proxy statement.

## Next Decisive Test

Run the prefix-scan verifier on one minimal proof with a valid two-row strict-prefix Qrep merge and on one identical proof with the certificate delayed by one line; compute Gamma_Qrep in both cases and export the rejected line as the private-row falsifier pivot.

## Contribution Pivot Invariant

If the next work only restates hardness magnification, MCSP promise, or barrier folklore, the branch is looping. If it computes a concrete transfer parameter, proves a route-specific no-go, or certifies a searchable certificate carrier with no advice leakage, it is moving toward a real scientific contribution.

## When To Stop

Stop, backtrack, or quarantine when two sharpened attempts still yield only a bounded exponent window, advised hard strings, a natural/relativizing/algebrizing proof object, or a certificate-existence condition equivalent to the target lower bound.

## Do Not Stop Prematurely If

Do not stop while a named carrier still has an untested exact audit: beta=0 or N^{o(1)} query dependence, compact searchable certificates, sparse non-natural property escape, proof-system overhead, or cofinal all-exponent lift.

## Validation Handoff

- Run validate_strategy_progression_judge.py after the builder.
- Render the Strategy Judge report tab in generate_discovery_marathon_html.py.
- Re-run this judge whenever the valid research-cycle count reaches another 10-cycle boundary.
