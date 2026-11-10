<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Reasoning-trace PDF runbook

Build a report only from a validated packet. The operational order is packet validation, print inventory, TeX rendering, isolated compilation, manifest creation, cross-format validation, visibility coverage, and expert review.

For one packet, use the renderer and compiler CLIs with explicit repository-relative input and output paths, then run:

```bash
python3 agentic/scripts/validate_public_reasoning_trace_pdf.py --packet <packet.json> --html <trace.html> --inventory <print-inventory.json> --tex <trace.tex> --pdf <trace.pdf> --manifest <pdf-manifest.json>
```

Validate all committed companions with:

```bash
python3 agentic/scripts/validate_public_reasoning_trace_pdf.py
```

The no-argument command is read-only. It requires the six named workflows and Route-A in release mode. Focused packet, inventory, TeX safety, and semantic tests remain usable without a TeX engine; release validation requires a real PDF and the `pdftotext`/`pdfinfo` inspection tools.

Compilation must use a fixed argument array, an isolated temporary directory, a sanitized environment, deterministic time settings, a bounded timeout, and `-no-shell-escape`. Never enable shell escape, network access, raw `input`/`include`, or packet-controlled packages. On failure, retain the source TeX and bounded diagnostics; do not replace a previously valid PDF.

Treat fatal errors, undefined references, missing glyphs, duplicate destinations, and material overfull boxes as failures. Smaller layout warnings remain visible in the manifest. Use `pdftotext -layout` to check selectable reading order and `pdfinfo` for page and metadata checks. PDF tagging or PDF/UA conformance is reported as not-run unless a dedicated checker actually verifies it.

A stale-output error means a bound byte sequence changed: packet, lens, print inventory, template/renderer, TeX, or PDF. Rebuild the companions in order; do not edit the manifest by hand. Byte-identical PDF is expected only in a pinned toolchain. Across platforms, compare the deterministic inventory and TeX plus normalized metadata and extracted semantics.

Roll out in three gates: one bounded workflow, full Route-A, then all seven reports and their handoffs. Do not enable release enforcement until manifests, visibility reports, tests, and expert-review findings agree.

