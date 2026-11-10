<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Taxonomy figure handoff

This contract is for the plotter and the existing appendix owner. It adds nested figure material, not a new paper-section schema.

Deliver `taxonomy-figures.tex`, editable `.dot`, `.svg`, vector `.pdf`, and `figure-manifest.json`. The manifest records model packet/source identities, file digest, inherited input digest, scope, every figure's workflow/operation membership and relevant source records, generated filenames, dependency version, and unresolved model unknowns. Keep the reviewed model beside the bundle or identify its immutable location. The helper copies each panel's relevant model records into the manifest so labels and evidence IDs remain traceable.

Generated taxonomy panels show only relevant families/layers on each page, with separate concept inventory panels retaining unused concepts; each operation appears once across the taxonomy pages. Input/output figures paginate separately for each workflow. Artifact inventory panels retain all types, their record fields, wrapper arguments, and alternatives. Explicit relations get their own relation panel so pagination never silently drops them. These are signature views, not temporal workflow diagrams. Workflow edges stay in the model and are not rendered as taxonomy edges.

Use `graphicx` for the TeX fragment. It references figure filenames relative to the compilation directory; the owner should set `\graphicspath`, copy assets to its selected paper-assets directory and adjust paths, or compile the probe in the assets directory. Keep generated filenames unchanged when convenient. No new macro or typography package is assumed. The helper's conservative captions and textual status labels need reviewed, source-specific interpretation before integration.

Check fonts after inclusion, ideally at least 9 pt at final size. A panel with two operations may still be too dense when signatures are long. Lower `--operations-per-page` (default 2), use a landscape page through the owner if justified, or split signatures into separate panels. `--taxonomy-per-page` defaults to 4. Each type expression is wrapped only for display; the exact original expression remains in the manifest. No wrapper or constituent is removed to simplify a label.

Use a new or empty output directory to avoid stale successful manifests. Output hashes cover every generated figure and TeX file; the manifest excludes itself. Run `python3 scripts/test_render_taxonomy.py` from this skill directory for behavioral checks.

The renderer rejects malformed IDs, duplicate IDs, unresolved family/type/operation references, inconsistent workflow membership, absent scope coverage, and unknown relation kinds before writing output. It permits `null` type IDs when a port includes an explicit unknown reason. Evidence review and equality of frozen upstream identities remain the skill's responsibility. Renderer DOT/SVG/TeX/manifest output is deterministic for fixed input bytes, options, and Graphviz version; PDF creation metadata may differ across runs. Cross-version Graphviz layout stability and proof-assistant validation are not claimed.
