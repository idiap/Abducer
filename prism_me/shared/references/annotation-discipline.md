<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Annotation Discipline

Use this policy whenever the request creates or edits `.py` or `.md` files.

The goal is not decorative commenting. The goal is to make the files legible to a newly onboarded agent or engineer who needs to understand:

- the core concept
- the intent of the file
- how the file fits the wider system
- why the main sections or code paths exist

## Python Files

When you touch a Python file, prefer explanation at three levels.

### 1. Module level

Add or improve the module docstring so it explains:

- the core concept modeled by the file
- the file's responsibility in the system
- the main abstractions or workflow stages it defines
- any important boundary conditions, invariants, or extension points

### 2. Class and function level

Add or improve docstrings so they explain:

- the intent of the class or function
- why it exists, not only what it returns
- the meaning of important inputs and outputs
- the conditions under which it should or should not be used

### 3. Local logic level

Add inline comments before non-obvious blocks to explain:

- the reasoning behind a branch, transformation, or ordering constraint
- the contract being preserved
- why a simpler-looking alternative was not used

Do not waste comments on line-by-line narration. Explain decisions, structure, and meaning.

## Markdown Files

When you touch a Markdown file, make it readable as onboarding material.

Add or improve:

- an opening explanation of the document's purpose
- clear framing for the audience or user of the document
- section introductions that explain why the section exists
- explicit descriptions of artifacts, stages, or outputs
- interpretation guidance where a reader might not know how to use the file

Markdown should not just list steps. It should help a future agent understand the concept behind the steps.

## Required Explanatory Themes

For both Python and Markdown, make sure the touched file answers most of these questions:

1. What concept does this file embody?
2. What job is it trying to do?
3. Where does it sit in the broader workflow or architecture?
4. What are the important inputs, outputs, and boundaries?
5. What should a future agent notice before changing it?

## Workflow Impact

- `prism-quality-criteria-elicitor` should include explanatory quality as part of the content bar.
- `prism-repo-cartographer` should identify annotation gaps in relevant `.py` and `.md` files.
- `prism-slice-planner` should include annotation work in slices when understanding would otherwise stay thin.
- `prism-implementation-driver` should add or improve explanatory annotations whenever it touches `.py` or `.md`.
- `prism-reflective-refinement-loop` should test whether explanatory improvements actually made the files more usable.
- `prism-spec-verification-critic` should audit whether the touched files became meaningfully more legible.
- `prism-integration-handoff` should record which files were annotation-enriched.
