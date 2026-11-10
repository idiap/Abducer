<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning-trace PDF architecture

The expert PDF is an additive, offline projection of the validated public reasoning monitor packet. The packet—not the HTML page, TeX layout, or compiler output—is the sole semantic authority. HTML and PDF are sibling views and must bind the same canonical packet digest.

The build is deliberately staged:

1. validate the public trace and construct the monitor packet;
2. construct a deterministic print inventory that gives every semantic item a projection disposition;
3. render inert, deterministic TeX from the packet, inventory, and declarative lens;
4. compile in an isolated temporary directory with shell escape disabled;
5. bind packet, inventory, lens, TeX, PDF, toolchain, and semantic IDs in a manifest;
6. validate cross-format identity and PDF-visible semantics;
7. compute PDF visibility independently of source and HTML coverage.

The expert body explains identity, focus, route, inference dossiers, failures, scope, decisions, obligations, authority, and handoffs. Complete chronology, graph edges, evidence, artifacts, coverage, and projection dispositions remain available in audit appendices. A summary may shorten presentation but may not erase an item from the inventory.

Three axes remain independent throughout: artifact integrity, scientific epistemic status, and workflow disposition. Execution order is never presented as entailment. A receipt is not scientific evidence, a control authorization is not a scientific claim, review authority is not proof authority, and finite evidence cannot silently establish a continuum claim.

Only inspectable public rationale is rendered: premises, the declared operator, a bounded warrant, conclusion, evidence or open obligation, uncertainty, scope, authority, alternatives, and remaining debt. Private model chain-of-thought is neither requested nor stored.

Stable semantic IDs, rather than page numbers or list positions, anchor cross-references. Workflow-specific language comes from declarative print lenses; the renderer has a neutral fallback and contains no workflow-ID branches. The established HTML renderer and main-workflow visualizers are not inputs and are not modified.

