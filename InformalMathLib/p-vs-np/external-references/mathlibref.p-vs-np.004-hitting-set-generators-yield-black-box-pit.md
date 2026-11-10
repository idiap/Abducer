<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Hitting-Set Generators Yield Black-Box PIT

- Result ID: mathlibref.p-vs-np.004
- Outcome: external_reference
- KB ref: p-vs-np
- Queue ID: proofq.p-vs-np.016,proofq.p-vs-np.017
- Attempt ID: 
- Bridge ID: 
- Source statement: 
- Target statement: 
- Web search used: True
- Entry kind: external-reference

## Statement

If a generator hits a polynomial class, then one can build a deterministic black-box identity test for that class by evaluating over a suitable grid.

## Summary

The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.

## External Reference Metadata

- Reference type: theorem
- Source name: Electronic Colloquium on Computational Complexity
- Source URL: https://eccc.weizmann.ac.il/report/2011/188/
- Search query: Non-Black-Box Hitting Sets From Restriction-Based Lower Bounds Proposition 2.4
- Used for: Clarifies the semantic-to-algorithmic direction on the PIT route by grounding the hitting-set to black-box-PIT implication.

## Imported Reference Notes

Canonical citation: R. J. Anderson, D. van Melkebeek, and I. Volkovich. Non-Black-Box Hitting Sets From Restriction-Based Lower Bounds. ECCC TR11-188, 2011, Proposition 2.4.
Local search failure: The blocked PIT repair lemma needed an exact theorem distinguishing an abstract semantic object from an explicit generator strong enough for algorithmic PIT.
What changed: The PIT route is not blocked by the total absence of a hitting-set-to-PIT connection; it is blocked by the lack of an explicit generator or certificate object for the right class.
Linked queue ids: proofq.p-vs-np.016, proofq.p-vs-np.017
Obstruction classes: pit-upgrade, explicitness-gap
