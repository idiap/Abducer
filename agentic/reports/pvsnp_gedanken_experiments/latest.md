<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Gedanken Experiments

- Target: `p-vs-np-target`
- Packets: `5`
- Generation mode: `pvsnp_complexity_gedanken_from_pressure_bridges`

## Essential Conclusions

### Oracle substitution microscope for the beta ceiling

- **Decisive Intuition:** Positive beta is the intuitive source of exponent-window collapse.
- **Formal Lesson:** Formally, black-box substitution yields N^{q+beta c}, so fixed epsilon cannot cover all c if beta>0.
- **Route Control Consequence:** Route control should demand q,beta computation before another magnification cycle.
- **Next Action:** Next action: run exact transfer audit and convert repeated beta>0 outcomes into a no-go theorem.

### Advised hard string versus searchable certificate

- **Decisive Intuition:** The key intuition is the difference between existence of hard strings and uniform access to hard strings.
- **Formal Lesson:** Formally, the bridge needs O(m)-bit sound certificates and kappa-gap coverage to transfer an exponent delta<epsilon/kappa.
- **Route Control Consequence:** Route control should focus on certificate length, verifier time, gap coverage, and naturalness rather than more MCSP slogans.
- **Next Action:** Next action: instantiate V,D for a proof-complexity or meta-complexity object and audit search time plus naturalness.

### Naturalness toggle board for sparse properties

- **Decisive Intuition:** The fundamental intuition is that avoiding natural proofs requires breaking a precise premise, not avoiding the word natural.
- **Formal Lesson:** Formally, the property must fail largeness or constructivity or change proof mediation while retaining usefulness.
- **Route Control Consequence:** Route control should reject property routes that do not publish a naturalness ledger.
- **Next Action:** Next action: build a ledger for the active property and demote it if all three natural-proof premises remain present.

### All-exponent quantifier-lift switch

- **Decisive Intuition:** The intuition is that P/poly separation quantifies over every polynomial exponent.
- **Formal Lesson:** Formally, a bounded exponent window is not NP not subset P/poly unless there is a cofinal lift over c.
- **Route Control Consequence:** Route control should ask whether each new carrier broadens quantifier coverage or repeats the same finite window.
- **Next Action:** Next action: state a parameterized theorem over c or quarantine the route as bounded-window only.

### Proof-system certificate bench for semantic lower bounds

- **Decisive Intuition:** The intuition is that proof objects can organize evidence, but only semantic soundness connects them to circuit lower bounds.
- **Formal Lesson:** Formally, proof length and verifier time must fit the target search bound while LB(u,s) soundly implies CC(f_u)>s.
- **Route Control Consequence:** Route control should reject proof-complexity moves that lose the semantic lower-bound interface.
- **Next Action:** Next action: choose a proof system and LB tautology, then audit proof length, verifier time, and semantic implication.

## Packets

### Oracle substitution microscope for the beta ceiling

- Packet: `gedanken.packet.7ee3d0001137`
- Bridge: `pvsnp-bridge-001`
- Pressure: `black_box_substitution_cap`
- Minimal world: A source language L_N decided by a SAT-oracle circuit with ordinary overhead N^q and SAT queries of length N^beta, against a lower bound SIZE(L_N)>N^{1+epsilon}.
- Controlled contrast: Compare beta>0 with beta=0 while holding q, epsilon, model, and valid lengths fixed.
- Expected observation: When beta>0, the contradiction window is c<(1+epsilon-q)/beta; when beta=0 and q<1+epsilon, the beta*c leakage disappears.
- Transfer certificate: The branch names q, beta, the target class, and whether the beta*c term is structurally unavoidable.
- Follow-up tasks:
  - `compute` Run an exact transfer audit for the active carrier with symbolic q and beta, then classify all-exponent, bounded-window, or no-window outcome.
  - `rank_next_experiment` Use the essential conclusions from `Oracle substitution microscope for the beta ceiling` to rank whether pvsnp-bridge-001 should persist, pivot, or become a no-go theorem.

### Advised hard string versus searchable certificate

- Packet: `gedanken.packet.9ccde3f6e6b6`
- Bridge: `pvsnp-bridge-002`
- Pressure: `meta_complexity_carrier_debt`
- Minimal world: For each length m, imagine either an advised high-complexity truth table y_m or a searchable pair (u,pi) accepted by verifier V and decoded by D into f_u.
- Controlled contrast: Compare nonuniform advice selection with deterministic exhaustive search over compact certificates.
- Expected observation: Advice selection gives hard objects without a uniform language; compact searchable certificates can generate a uniform E-style language if gap coverage and verifier time hold.
- Transfer certificate: The theorem states exactly when searchable certificates yield a uniform lower-bound language and what naturalness premise is avoided.
- Follow-up tasks:
  - `derive` Formalize the V,D certificate transfer theorem with epsilon, kappa, certificate length, verifier time, and no-advice conditions.
  - `rank_next_experiment` Use the essential conclusions from `Advised hard string versus searchable certificate` to rank whether pvsnp-bridge-002 should persist, pivot, or become a no-go theorem.

### Naturalness toggle board for sparse properties

- Packet: `gedanken.packet.17ec3ca697b6`
- Bridge: `pvsnp-bridge-004`
- Pressure: `naturalness_density_pressure`
- Minimal world: A truth-table property P with toggles for largeness, polynomial-time constructivity over truth tables, usefulness against polynomial-size circuits, and PRF-compatible circuit class.
- Controlled contrast: Compare dense constructive useful property with sparse or proof-mediated useful property.
- Expected observation: If largeness, constructivity, and usefulness all remain present, the route hits natural-proof pressure; if one premise fails, the route must prove usefulness survives.
- Transfer certificate: The property states exactly which natural-proof premise fails and why the target usefulness implication survives.
- Follow-up tasks:
  - `formalize` Build a natural-proof ledger for the active property with density, constructivity, usefulness, PRF-risk, and escape premise.
  - `rank_next_experiment` Use the essential conclusions from `Naturalness toggle board for sparse properties` to rank whether pvsnp-bridge-004 should persist, pivot, or become a no-go theorem.

### All-exponent quantifier-lift switch

- Packet: `gedanken.packet.8bd4b6f7a2cf`
- Bridge: `pvsnp-bridge-005`
- Pressure: `all_exponent_quantifier_gap`
- Minimal world: A family of source carriers indexed by target exponent c, each with overheads q_c,beta_c and source margin a_c.
- Controlled contrast: Compare one fixed source lower bound with a cofinal family covering arbitrary c.
- Expected observation: A fixed carrier covers only a window of c; a genuine quantifier lift must provide a uniform way to cover every fixed c without hiding the target lower bound.
- Transfer certificate: The branch emits a cofinal parameter family or a no-go theorem explaining why no such family exists in the method class.
- Follow-up tasks:
  - `falsify` Test whether the active source family covers arbitrary c or only restates a bounded exponent window.
  - `rank_next_experiment` Use the essential conclusions from `All-exponent quantifier-lift switch` to rank whether pvsnp-bridge-005 should persist, pivot, or become a no-go theorem.

### Proof-system certificate bench for semantic lower bounds

- Packet: `gedanken.packet.6868bfd1a516`
- Bridge: `pvsnp-bridge-003`
- Pressure: `proof_complexity_transfer_gap`
- Minimal world: A lower-bound tautology LB(u,s) in a named Cook-Reckhow proof system, with proof length ell(m), verifier time T_V(m), and semantic soundness CC(f_u)>s.
- Controlled contrast: Compare short verifiable semantic certificates with proof lower-bound obligations as hard as the target.
- Expected observation: Short sound proofs can feed the searchable certificate bridge; missing or huge proofs relocate the target difficulty into proof complexity.
- Transfer certificate: The bridge says whether proof objects can supply searchable high-complexity certificates or only relocate the hard lower bound.
- Follow-up tasks:
  - `formalize` Specify a proof system and LB(u,s) tautology family, then state the semantic soundness and proof-length requirements.
  - `rank_next_experiment` Use the essential conclusions from `Proof-system certificate bench for semantic lower bounds` to rank whether pvsnp-bridge-003 should persist, pivot, or become a no-go theorem.

