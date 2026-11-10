# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from validate_public_reasoning_trace_pdf import EXPECTED_STEMS, MATERIAL_OVERFULL_PT, companion_paths


def test_committed_pdfs_are_real_and_have_clean_compiler_dispositions() -> None:
    for stem in sorted(EXPECTED_STEMS):
        paths = companion_paths(stem)
        assert paths["pdf"].read_bytes().startswith(b"%PDF-")
        manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
        assert manifest["compiler"]["disposition"] == "compiled"
        diagnostics = manifest["compiler"].get("diagnostics", "") + "\n".join(manifest["compiler"].get("warnings", []))
        assert "undefined reference" not in diagnostics.casefold()
        assert "missing character:" not in diagnostics.casefold()
        assert "destination with the same identifier" not in diagnostics.casefold()
        amounts = [float(value) for value in re.findall(r"Overfull \\[hv]box \(([-+0-9.]+)pt too", diagnostics, re.I)]
        assert not amounts or max(amounts) <= MATERIAL_OVERFULL_PT

