<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# P vs NP Negative Tactic Packet

Route-specific selection of contradiction, impossibility, falsifier, and constructive tactics for P vs NP discovery branches.

## Policy

- Use contradiction only when the negated local subclaim has a carrier and an accepted conflict target.
- Use impossibility theorem formation only for scoped method classes with explicit parameters and escape conditions.
- Keep constructive exploration alive when beta=0, subpolynomial queries, nonblackbox use, non-naturalness, or advice-free certificates remain untested.
- Treat scoped no-go results and finite falsifiers as possible paper-level stepping stones.

## Branch Recommendations

### Hardness-Magnification Bridge Realization

- Route family: `black_box_substitution_or_hardness_magnification`
- Tactic mode: `falsifier_search`
- Branch control: `persist_with_falsifier_test`
- Reason: The decisive issue is whether positive target-query exponent beta and overhead q cap the transfer before it reaches all SAT exponents.
- Method class / negation: black-box target-circuit substitution interfaces with source size N, target query length n^beta, and overhead N^q
- Carrier: the transfer inequality SAT in SIZE(n^c) => source carrier in SIZE(N^{q+beta c+o(1)})
- Conflict target: claimed all-exponent exclusion for NP not subset P/poly despite positive beta
- Escape conditions:
  - beta=0 or genuinely subpolynomial target-query length
  - a nonblackbox use of the SAT circuit not summarized by query exponent beta
  - a source lower bound stronger than the transferred upper-bound window
- Proof obligations:
  - Compute beta and q for the named carrier, including all padding and decoding overhead.
  - Derive the exact exponent window q+beta*c+o(1) and identify which SAT exponents survive.
  - Record relativization, algebrization, natural-proofs, and advice status for this interface.
- Handoff: Send this packet to pvsnp-symbolic-complexity-auditor for exact parameters, then to pvsnp-impossibility-theorem-forger and contradiction-route-auditor if the obstruction is theorem-shaped.
- Paper contribution potential: Potential paper-level stepping stone if the result becomes a scoped theorem or finite falsifier with prior-art boundary and explicit escape conditions.

### Barrier-Aware Lower-Bound Route

- Route family: `natural_property_or_combinatorial_lower_bound`
- Tactic mode: `falsifier_search`
- Branch control: `persist_with_falsifier_test`
- Reason: The key question is whether the proposed lower-bound property is simultaneously large, constructive, and useful.
- Method class / negation: large constructive useful properties for the exact circuit class targeted by the branch
- Carrier: the natural-proofs tuple: largeness, constructivity, usefulness, and pseudorandom-function tension
- Conflict target: cryptographic hardness or PRF assumptions for a class that the property claims to separate
- Escape conditions:
  - non-large property
  - nonconstructive or semantic property outside the efficient recognition requirement
  - proof-system-specific object whose usefulness does not induce a large property of truth tables
- Proof obligations:
  - Define the property and the circuit class against which it is useful.
  - Estimate largeness/density and constructivity time.
  - State the PRF or cryptographic assumption needed for the natural-proofs pressure.
- Handoff: Send this packet to pvsnp-symbolic-complexity-auditor for exact parameters, then to pvsnp-impossibility-theorem-forger and contradiction-route-auditor if the obstruction is theorem-shaped.
- Paper contribution potential: Potential paper-level stepping stone if the result becomes a scoped theorem or finite falsifier with prior-art boundary and explicit escape conditions.

### MCSP / Meta-Complexity Carrier Transfer

- Route family: `mcsp_mktp_or_meta_complexity_carrier`
- Tactic mode: `falsifier_search`
- Branch control: `persist_with_falsifier_test`
- Reason: The live risk is that a meta-complexity carrier supplies aggregate or advice-selected hardness rather than a uniform language lower bound.
- Method class / negation: MCSP/MKtP certificate carriers, hard-row selectors, and truth-table ranking mechanisms
- Carrier: row-hardness or certificate selection mechanism and its advice/uniformity ledger
- Conflict target: claim of language hardness from a carrier that may only identify nonuniform hard rows
- Escape conditions:
  - explicit advice-free row-hard certificate
  - searchable certificate within the intended target class
  - density control that avoids natural-property largeness pressure
- Proof obligations:
  - Name the truth-table family, row selector, verifier, and certificate size.
  - Check whether selection uses advice, ranking, or nonuniform hard-string choice.
  - Test easy sparse tables and low-complexity rows as falsifiers.
- Handoff: Send this packet to pvsnp-symbolic-complexity-auditor for exact parameters, then to pvsnp-impossibility-theorem-forger and contradiction-route-auditor if the obstruction is theorem-shaped.
- Paper contribution potential: Potential paper-level stepping stone if the result becomes a scoped theorem or finite falsifier with prior-art boundary and explicit escape conditions.
