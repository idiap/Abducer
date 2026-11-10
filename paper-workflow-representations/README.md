<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Workflow representations in the paper

The root `reasoning-as-typed-epistemic-composition.tex` includes these editable assets.
Its current title is **Conceptual Tensions and the Reorganization of Scientific
Reasoning**. `conceptual-inquiry.tex` organizes the main text around reconstructing
commitments, locating tensions, diagnosing bottlenecks, changing representations,
reflecting on alternatives, and developing revisable programmes. Its running
pair-state example distinguishes observable identity from the separate obligation
that dynamics respect that identity. The first figure shows revisitation and the
nonconceptual and no-preference branches.

`supporting-calculus.tex` preserves the inference taxonomy and workflow abstractions
as Appendix A. `procedure-supplement.tex` retains prior source-procedure accounts and
the diffusion walkthrough. Detailed native, dependent-type, taxonomy and workflow
appendices follow. Former claims about higher-order completeness, status-only
evaluation and decreasing obligation counts are explicitly scoped to their limited
models. They do not define the main account of conceptual inquiry.

`granular-workflows.tex` introduces the notation and includes discovery, boundary, and Cohere fragments. Every workflow has a concrete constructed example and a description of each declared occurrence, typed dependency, relation license and control boundary. Companion provenance files map aliases and conceptual descriptions to exact source names. Nine unresolved projection occurrences are described as gaps; source coverage is not a claim that their mechanisms are implemented. The dependent family remains a proposal, not native proof enforcement.

Regenerate figures with `dot -Tpdf NAME.dot -o NAME.pdf` in this directory. Build the root TeX twice from the repository root with `pdflatex -interaction=nonstopmode -halt-on-error reasoning-as-typed-epistemic-composition.tex`. Keep this directory alongside the root TeX. `provenance.json` records source and artifact hashes; the request's `check_coverage.py` reproduces bounded declared-source accounting. This is manually reviewed integration, not automatic full-pipeline acceptance.

The workflow subsections also draw on selected underlying skills and contracts, recorded under `internal_mechanism_sources` in their provenance files. Native projection gaps are distinguished from the richer prescribed procedures. The latter are not claimed as verified native implementations or measured scientific results.

## Step-level regeneration

The prior step revision is preserved: `step-walkthrough.tex` supplies the diffusion
chain now included in the procedure supplement, and `steps/` contains 65 occurrence
explanations covering all 19 workflows.
`step-explanations.json` is the reviewed authoring packet. Each step has purpose,
input, procedure, criterion, output, failure/continuation and a concrete example
transition. Exact bindings connect the prose to native declarations; numbering is
a reading order, not an assertion that parallel branches execute sequentially.
Each workflow carries one continuous case and a changed-input contrast.

The reusable skill contract is
`proj_skills/framework-paper-workflow-appendix-writer/references/step-explanation-contract.md`.
From the repository root, regenerate and check actual inclusion with:

```bash
python3 proj_skills/framework-paper-validator/scripts/step_explanations.py \
  --packet paper-workflow-representations/step-explanations.json \
  --render-dir paper-workflow-representations/steps \
  --manuscript reasoning-as-typed-epistemic-composition.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error reasoning-as-typed-epistemic-composition.tex
```

Edits to explanation content or frozen scientific sources invalidate the recorded
review. Use `--draft` only for intermediate rendering, then renew the manual
seven-criterion review before delivery. The checker validates integrity, not
scientific truth or explanatory adequacy by itself. The author drafts, assembly
helper, plan, source review and test evidence are retained in
`.prism/paper-step-explanations/`. This manual lane remains separate from the
fixed nine-section paper runner.

## Conceptual argument and review

The reusable conceptual contract is
`proj_skills/framework-core-mechanism-curator/references/conceptual-inquiry-contract.md`.
The model is now manual authoring version 2.0.0: conceptual roles organize the
argument, with optional many-to-many inference annotations. The plan, frozen source
selection, curated model, claim ledger, blueprint and reviews are in
`.prism/paper-conceptual-inquiry/`. Its initial migration script is historical;
the reviewed TeX files here are the canonical final sources.

Regenerate the new vector diagram before compiling after a diagram edit:

```bash
dot -Tpdf paper-workflow-representations/conceptual-inquiry.dot \
  -o paper-workflow-representations/conceptual-inquiry.pdf
```

Review whether the main argument still explains the tension and transformation
after removing inference labels. This manual content check complements the
occurrence integrity gate; neither compilation nor complete metadata establishes
conceptual merit or scientific execution.


## Recursive goals and workflow relationships

The current extension is in `recursive-goals.tex`: it explains goal identity,
required obligations and alternative routes, shared dependencies, bounded
attempts, stopping and parent enablement. The pair-state example follows two
recursive levels through a proof or counterexample and a revised parent question.
`recursive-goals.dot` and `workflow-ecosystem.dot` supply the two new vector
figures. `workflow-relations-table.tex` covers all 19 workflows in Appendix C,
with exact source-policy handles and scoped return/stop dispositions.

This is an explanatory management model. Source-policy switches, registered
Cohere composition, native local data dependencies and editorial connections
have separate meanings; the paper does not establish a universal scheduler.
Renewing resources resumes unresolved work without rehabilitating unchanged
refuted claims. The shared authoring reference is
`proj_skills/framework-core-mechanism-curator/references/recursive-goals-and-workflow-relations.md`.
The manual goal/workflow supplement, source index, plan and reviews are in
`.prism/paper-recursive-goals/`; they do not silently extend closed runner schemas.

Rebuild the added figures before compiling after changes:

```bash
dot -Tpdf paper-workflow-representations/recursive-goals.dot -o paper-workflow-representations/recursive-goals.pdf
dot -Tpdf paper-workflow-representations/workflow-ecosystem.dot -o paper-workflow-representations/workflow-ecosystem.pdf
```


## Concise structured interfaces

Current step rendering separates **Purpose, Input, Method, Check, Output, Next
and Example**. Inputs and outputs name carried scientific content; routing
remains in Next. The overview table similarly separates Purpose/Input and
Output/Next; goal and child-handoff records use named fields.

The current wording and source-bound semantic review are recorded in
`.prism/paper-structured-io/`. Purpose/input/output text is 37.9% shorter across
65 steps; procedures, criteria, examples and source bindings are preserved.
The renderer uses aligned standard description labels. There is no word minimum:
empty fields fail integrity validation, while source-bound review judges substance.
Use the existing step regeneration command above after renewing review for content
edits. Build the canonical root TeX after regeneration. Separate fields increase
vertical space, so page count is not the measure of this wording reduction.
