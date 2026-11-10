<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Dynamic reasoning selection

Choose from epistemic need, then bind a skill:

| Current deficit | Prefer |
|---|---|
| No adequate candidate explanation or bridge | abductive hypothesis formation |
| Consequences under explicit premises are unknown | deductive entailment |
| A pattern across scoped cases is needed | inductive generalization |
| A source structure may transfer to the target | structural analogy and transfer |
| Alternatives need a controlled discriminating comparison | contrastive counterfactual reasoning |
| A finite, symbolic, toy, or numerical probe is needed | model-based reasoning |
| A candidate lacks adversarial pressure | critical refutational testing |
| Findings exist but authority or obligations are unclear | evidential status calibration |

After every output, compare the old and new criterion dispositions. Continue
only when there is a real state delta or an explicit recovery hypothesis.
Acceptance and workflow switching require calibration. A capability gap is a
routing blocker, not evidence against the scientific claim.

## Capability selection after type selection

Once the epistemic need fixes a reasoning type, query the registered
materializers for that type. Reject candidates whose prerequisites, domain,
input contract, output contract, or authority ceiling do not fit the current
state. Prefer a primary mapping over a secondary mapping when both are equally
fit; mapping confidence is curatorial evidence about the mapping, not evidence
for the scientific claim. Give the selected alias-to-skill binding to `$route`
and execute only if the resulting route receipt is executable.
