<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning-trace PDF accessibility

The current target is an expert-readable, searchable PDF with logical source order, selectable text, stable headings, a table of contents or bookmarks, repeated table headings, textual alternatives for topology, and status labels that do not depend on color. Long identifiers wrap without reducing body text below the readability threshold.

Automated checks use `pdftotext -layout` for reading-order sentinels and `pdfinfo` for document metadata and page count. They also inspect compiler diagnostics for missing glyphs, duplicate destinations, undefined references, and material clipping. These checks establish tested usability properties; they do not establish PDF/UA conformance.

Tagged-PDF structure, screen-reader behavior, and formal PDF/UA validation are recorded as **not run** unless dedicated tooling and a human assistive-technology review are performed. An unavailable checker is never reported as a pass. Any missing semantic ID, hidden failure, clipped dossier, color-only state, or unusable Route-A appendix is a blocking finding.

