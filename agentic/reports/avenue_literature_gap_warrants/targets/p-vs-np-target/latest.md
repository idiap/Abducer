<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Avenue Literature-Gap Warrants

Target: `p-vs-np-target`
Status: `implemented`
Warrants: `1`
Investment decisions: `{'reframe_gap_before_investment': 1}`

Target-scoped preinvestment literature-gap warrants. Broad proof-search investment is blocked unless an avenue has a validated warrant with enough novelty, field impact, unification power, and route-decision power.

## Target-preserving P vs NP bridge route

- Avenue: `pvsnp.bridge_route_gap`
- Decision: `reframe_gap_before_investment`
- Allowed next modes: `literature_gap_reframe, artifact_sprint, falsifier_sprint, proof_delivery`
- Relevance score: `3`
- Field-impact score: `4`
- Unification score: `4`
- Route-decision score: `3`

Smallest honest claim: A P vs NP avenue is investable only if it names a target-preserving source object, target class, reduction or proof-system interface, quantifier regime, and barrier status before any global separation rhetoric.

Gap statement: The relevant research gap is a sharply typed bridge that avoids known barrier and quantifier leaks. The current workflow must prove, disprove, or quarantine such a bridge rather than accumulate partial analogies.

Why not already known: Classical NP-completeness and barrier literature frames the target and common obstructions, while modern lower-bound frontiers show restricted progress. The local avenue has not yet demonstrated a bridge that survives model, advice, and exponent transfer.

Closest known results:

- `ref.cook-1971` S. A. Cook (1971), The complexity of theorem-proving procedures: It does not provide lower-bound machinery for separating P from NP.
- `ref.razborov-rudich-1997` A. Razborov and S. Rudich (1997), Natural proofs: It is a barrier criterion, not a complete prohibition on all nonnatural or proof-complexity routes.
- `ref.aaronson-wigderson-2008` S. Aaronson and A. Wigderson (2008), Algebrization: A new barrier in complexity theory: It does not rule out every proof-complexity, meta-complexity, or highly nonblackbox route.
- `ref.murray-williams-2018` C. Murray and R. Williams (2018), Circuit lower bounds for nondeterministic quasi-polytime: It is not a direct P vs NP separation and still leaves target-preserving amplification gaps.

Disqualifiers:

- `barrier_slogan` -> `reframe_gap_before_investment`: The branch cites natural proofs, relativization, or algebrization without checking the exact property or oracle/algebraic interface.
- `advice_or_uniformity_leak` -> `quarantine_low_relevance`: The bridge selects hard objects, rows, formulas, or certificates nonuniformly without paying advice.
- `prior_art_absorbs_bridge` -> `do_not_invest_prior_art_collision`: Known lower-bound, proof-complexity, or meta-complexity literature already proves the bridge under the same assumptions.

## Validation

Run `agentic/scripts/validate_avenue_literature_gap_warrant.py` before starting or promoting broad branch exploration.
