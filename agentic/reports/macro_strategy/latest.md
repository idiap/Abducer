<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Macro Strategy Report

- Target: `p-vs-np-target`
- Headline: Current macro strategy: compute the transfer exponents or turn the route into a no-go theorem.
- Status: `active_macro_strategy_synthesis`

## Recommended Next Posture

- `primary`: Compute a, q, and beta for the next proposed carrier before any broader marathon continuation.
- `secondary`: Package padding/projection and black-box substitution failures as bounded no-go theorem candidates.
- `handoff`: Promote only a formal transfer theorem or route-specific impossibility theorem toward paper form.
- `avoid`: Do not spend cycles restating hardness magnification without a carrier, model, quantifier regime, and falsifier.

## Macro Strategies

### 1. Black-box transfer and exponent-window audit

- Route family: `Complexity lower-bound transfer`
- Priority score: `100`
- Thesis: Treat every proposed magnification route as an explicit transfer inequality from SAT in SIZE(n^c) or NP subset P/poly to a source-carrier upper bound.
- Physics picture: For this complexity-theory target, read the physical picture as a proof-dynamics picture: the target circuit is a resource flowing through an interface. Positive query-length exponent beta amplifies the target exponent c and prevents a barely-superlinear source lower bound from ruling out all polynomial-size SAT circuits.
- Why now: The latest cycle isolated max{a,q+beta c} as the active obstruction, so the next work must compute a, q, and beta rather than restate magnification.
- Literature refs: `ref.cook-1971, ref.karp-1972, ref.hardness-magnification-modern`

### 2. Padding and projection demagnification as a no-go route

- Route family: `Projection carrier obstruction`
- Priority score: `100`
- Thesis: Use the padding/projection failures as theorem material: projection carriers either give only bounded exponent windows or move the real proof burden into sparse valid-length lower bounds.
- Physics picture: The conceptual mechanism is proof-debt conservation. Padding changes the coordinate system, but projection back to SAT reveals that the supposedly weak source lower bound already encodes the hard target lower bound.
- Why now: Cycles 1-5 repeatedly converted padding optimism into exact exponent inequalities and sparse-length obligations.
- Literature refs: `ref.hardness-magnification-modern, ref.nonuniform-circuit-lower-bounds, ref.natural-proofs`

### 3. Meta-complexity carrier pressure

- Route family: `MCSP/MKtP/GapMCSP route analysis`
- Priority score: `100`
- Thesis: Use MCSP, MKtP, or GapMCSP only after the carrier's verifier overhead, density, naturalness, advice leakage, and target transfer are stated.
- Physics picture: The meta-complexity carrier is a diagnostic medium: it can reveal whether a weak source lower bound really transfers, or whether constructivity, largeness, and nonuniform advice absorb the intended separation.
- Why now: Cycles 1, 2, 4, 5, and 6 all point to MCSP/MKtP as the next plausible nonprojection test, but cycle 6 already exposed a fixed-threshold ceiling.
- Literature refs: `ref.mcsp, ref.mktp, ref.razborov-rudich-1997, ref.aaronson-wigderson-2009`

### 4. Nonblackbox or subpolynomial-interface escape search

- Route family: `Escape-condition construction`
- Priority score: `100`
- Thesis: The search should now aim at the exact escape left open by the no-go evidence: a target-preserving carrier with subpolynomial queries or a genuinely nonblackbox use of the SAT circuit.
- Physics picture: The route needs a new interaction pattern with the target circuit. If the circuit is only queried as a black box at polynomially growing target length, the beta-ceiling reappears; a real escape must change that interface.
- Why now: Cycle 7 localized the remaining opening as N^{o(1)} target queries, sub-N^{1+epsilon} interface size, and a valid lower-bound carrier.
- Literature refs: `ref.proof-complexity, ref.algebrization, ref.hardness-magnification-modern`
