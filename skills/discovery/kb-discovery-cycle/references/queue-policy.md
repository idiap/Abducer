
<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Queue Policy

Queue a discovery output only if all of the following hold:

1. There is a concrete claim under test.
This should usually be a route lemma or conditional proposition, not a generic slogan.

2. The claim is theorem-pair specific.
The queue item must identify the source statement, target statement, bridge object, and invariant.

3. Both positive and negative outcomes would be informative.
The task should admit a meaningful proof or a meaningful refutation/obstruction result.

4. The route is not already closed.
If the queue item is already marked `proved`, `disproved`, or `prior_art_found`, preserve it rather than recreating it.

5. The route is not known to be too thin.
Skip `re-encode-before-retrying` routes unless the user explicitly wants underspecified branches.

