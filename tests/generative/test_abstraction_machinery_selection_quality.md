<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Probe: Abstraction Machinery Selection Quality

These probes check whether Abducer can argue for the best mathematical or conceptual machinery as a stepwise target-controlled abstraction choice, rather than listing prestigious methods.

## Probe 1: Good Route-Role Match

Input: A route says Balaban/RG control is useful for Yang-Mills.

Expected generative interpretation: The route must identify RG as `construction` machinery controlling the interface from regulated gauge fields to continuum Schwinger functions. It must say that RG is not yet a mass-gap witness and must hand off to OS reconstruction plus spectral witness obligations.

Failure signal: The answer says "use RG because renormalisation is powerful" without naming the constructed object, controlled interface, or bridge obligation.

## Probe 2: Premature Endpoint Machinery

Input: A route proposes to prove the Yang-Mills mass gap by writing `Spec(H|P_perp H_YM) subset [Delta,infinity)`.

Expected generative interpretation: The route must classify Hamiltonian spectral language as endpoint `validation` machinery. It must backtrack to reconstruction unless H_YM, Omega, H, and P_perp are outputs of OS/Wightman reconstruction from the same continuum Schwinger functions.

Failure signal: The answer treats the spectral inequality as a derivation rather than as the final obligation.

## Probe 3: Proxy Proof Substitution

Input: A route cites a strong-coupling lattice glueball gap.

Expected generative interpretation: The route must classify this as an `evidence_task` or at most witness-shaped evidence until cutoff-uniform continuum transfer and observable-density obligations are supplied.

Failure signal: The answer promotes fixed-lattice decay or numerical spectroscopy as proof of the continuum Clay target.

## Probe 4: Missing Transfer Bridge

Input: A route has Euclidean correlator decay but no OS reconstruction or density statement.

Expected generative interpretation: The route must classify correlator decay as `witness` machinery and require transfer obligations: OS reconstruction, same-theory observable family, spectral representation, cutoff-uniform constants, and density in the excitation sector.

Failure signal: The answer says "decay implies gap" without stating the conditions under which the implication is valid.

## Probe 5: Method-Name-Only Explanation

Input: "Use spectral theory, RG, and category theory to solve the problem."

Expected generative interpretation: The route must be rejected or quarantined until each method is assigned a universal role, target-object link, controlled interface, assumptions, output obligation, invalid-use modes, and validation handoff.

Failure signal: The answer praises breadth or novelty without typing proof roles.

## Probe 6: Non-Yang-Mills Universality Case

Input: A P vs NP route proposes communication-complexity lower bounds.

Expected generative interpretation: The route must not import Yang-Mills vocabulary. It should classify communication complexity as either `representation`, `transfer`, or `witness` machinery depending on the exact lower-bound bridge. It must state the target object as P vs NP, forbid unrelated lower-bound folklore, and require a transfer bridge into proof-object adequacy for the final separation target.

Failure signal: The answer hard-codes gauge theory examples or accepts a lower-bound analogy without a transfer certificate.
