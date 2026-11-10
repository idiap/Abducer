<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Web Search Policy

Default stance: do not browse.

Only use web search if all of the following hold:

1. The missing fact is decisive.
It must materially affect a proof step, a disproof step, an exact theorem statement, or a prior-art determination.

2. The fact is not already available locally.
Check the current KB, discovery artifacts, proof dossier, and local InformalMathLib first.

Generative/IDE search for similar bridge objects or solution patterns may happen before browsing,
but only as conjecture formation.
It does not replace the local KB/InformalMathLib check, and it does not count as prior-art evidence.

3. A local-search failure has been recorded.
Before browsing, record what local theorem lookup, InformalMathLib lookup, or counterexample/barrier search failed and why that failure matters.

4. The query can be stated concretely.
Good web-search targets are named theorems, papers, authors, barrier results, exact thresholds, or model-specific facts.

Search is especially justified when:

1. a prior-art check could invalidate a novelty claim;
2. a negative result or barrier may already be known;
3. the proof depends on an exact theorem statement not present locally.

Do not browse for:

1. generic background;
2. intuitive exposition;
3. extra references that do not change the proof state;
4. decorative citations after the proof decision is already clear.

If web search is used, record:

1. the exact query;
2. the URL/source used;
3. which proof step or novelty decision it informed;
4. what exact statement changed because of the search;
5. whether it changed the outcome.

If the search yields an external theorem, definition, or axiom that the proof attempt relies on, import that reference into `InformalMathLib/<kb-ref>/...` during finalization.
