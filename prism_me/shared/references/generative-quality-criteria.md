<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Generative Quality Criteria

Use this guide when defining quality bars for skill behavior that is not purely deterministic.

The point is to evaluate the actual content the skill generates, not only whether the interface looks tidy.

## Deterministic And Interface Dimensions

These still matter:

- inputs and outputs are explicit
- artifact paths are stable
- stage order is coherent
- contracts are typed
- runtime boundaries are visible

But these are not enough.

## Generative And Content Dimensions

A good skill should usually be judged on most of these dimensions:

1. Conceptual clarity
   Does the output clearly express the core concept instead of hiding behind generic wording?

2. Intent fidelity
   Does the content stay aligned with the real job of the skill?

3. Epistemic discipline
   Does it separate facts, assumptions, unknowns, risks, and open questions cleanly?

4. Coverage
   Does it cover the important dimensions of the task instead of cherry-picking the easy parts?

5. Specificity
   Does it use concrete, decision-making language instead of vague advice?

6. Actionability
   Can another agent use the output to decide what to do next?

7. Differentiation
   Is the skill output recognizably distinct from neighboring skills, or is it blandly interchangeable?

8. Failure-mode awareness
   Does it surface plausible weak points, edge cases, or likely misuses?

9. Explanatory richness
   Does it actually teach the reader how to interpret the content?

10. Revision usefulness
    When criticized, does it become sharper in a targeted way rather than simply longer?

## Good Quality Criteria Packet

A strong quality-criteria artifact should include:

- explicit evaluation dimensions
- success signals
- failure signals
- sample probes or test prompts
- pass or conditional thresholds
- common failure patterns to watch

## Refinement Expectations

Once criteria exist, run reflective refinement loops against them.

At minimum:

1. evaluate a current draft against the criteria
2. localize concrete weak spots
3. revise the skill or artifact
4. re-evaluate
5. run at least one more cycle if the result still has meaningful gaps
