---
name: framework-paper-taxonomy-plotter
description: Plot a reviewed reasoning taxonomy and workflow input/output types as legible vector appendix figures. Use for paper taxonomy visualizations that preserve reasoning families, explicit type wrappers, multi-input operations, and source uncertainty, with captions and a figure-to-source manifest for the existing appendix owner.
---

# Framework Paper Taxonomy Plotter

Give the reader two complementary views: where reasoning operations belong, and what information each operation consumes and produces. A taxonomy is not an execution graph or a proof of subtype relationships.

## Inputs and ownership

Consume the reviewed `ReasoningTaxonomyModel` from `$framework-reasoning-taxonomy-modeler`, the approved `PaperBlueprint`, its claim ledger, and manuscript context. Read the [model contract](../framework-reasoning-taxonomy-modeler/references/taxonomy-model-contract.md) and [figure handoff](references/figure-handoff.md). Check source identity, digest, scope, and review before rendering. A successful renderer validates structure, not evidence or mathematical truth.

The blueprint names one final appendix section owner, normally `$framework-paper-workflow-appendix-writer` or `$framework-paper-dependent-type-writer`. Supply figure fragments to that owner; do not create a competing `PaperSectionDraft`, new CLI stage, or standalone second appendix. Preserve the existing workflow examples and formal descriptions. This skill builds reusable figures; creating or editing a manuscript follows the actual request's scope.

## Build the views

- Show reasoning families and their operation memberships in one view. Keep many-to-many membership and unclassified operations visible. Layer membership, conceptual grouping, and declared subtyping must have distinct labels and line styles. Inferred or proposed relations remain visibly qualified. Do not infer a tree from names or draw workflow order as taxonomic ancestry.
- Show input → operation → output signatures in another view, grouped by workflow. Preserve every named port, multi-input requirement, wrapper, direction, and full dependent expression. Separate repeated types at distinct ports. These arrows mean consumption/production, not guaranteed successful generation, subtype inclusion, or checked dependent typing.
- Prefer one overview plus paginated detail panels when dense. Never achieve fit by silently omitting operations or shrinking labels beyond readability. Keep stable labels between overview, detail, and examples. Unknown types remain explicit; an empty known port list means none, not unknown.
- Use editable DOT/SVG and vector PDF with readable monochrome distinctions. The bundled renderer uses Python's standard library and Graphviz `dot`; no image generation or network service is needed. Run `python3 proj_skills/framework-paper-taxonomy-plotter/scripts/render_taxonomy.py MODEL.json --output-dir OUTPUT`. It writes provenance mappings, vector figures, and a TeX fragment; it does not insert them into a manuscript.

## Review and handoff

Inspect the generated SVG/PDF and a compiled TeX probe at intended page width. Check long labels, wrapper visibility, arrow direction, every workflow's coverage, grayscale legend, and caption accuracy against the source. Split or reshape dense panels rather than accept illegible scaling. The bundled renderer is a reproducible starting layout; alternate local plotting code is acceptable if it preserves the model and mapping.

Draft a short interpretation that tells the reader what the figures reveal: for example, several reasoning families sharing an evidence type, or generation returning a wrapped candidate rather than a verified result. Derive observations from the actual model; do not invent explanatory findings. Keep hashes and source locators in the sidecar. Captions distinguish declared, inferred, proposed, and unknown elements and explain the two arrow meanings. Pass the reviewed fragment, figures, manifest, interpretation, package requirements, and source trace to the sole owner and then the existing consistency/LaTeX assembly lane. An isolated compile proves buildability only.
