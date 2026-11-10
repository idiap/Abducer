#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""Generate the proof-discovery language specification artifacts."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
_MACRO_DIR = Path(__file__).resolve().parents[3] / "reporting" / "kb-macro-proof-paper-writer" / "scripts"
for _path in (_COMMON_DIR, _MACRO_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from generate_macro_proof_state_report import compile_pdf
from proof_discovery_language import build_language_spec
from proof_discovery_language import render_latex
from proof_discovery_language import render_markdown


def write_outputs(*, docs_dir: Path) -> dict[str, Path]:
    """Write the proof-discovery language artifacts to the docs directory."""

    docs_dir.mkdir(parents=True, exist_ok=True)
    spec = build_language_spec()
    json_path = docs_dir / "proof-discovery-language.json"
    md_path = docs_dir / "proof-discovery-language.md"
    tex_path = docs_dir / "proof-discovery-language.tex"
    pdf_path = docs_dir / "proof-discovery-language.pdf"

    json_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(spec), encoding="utf-8")
    tex_path.write_text(render_latex(spec), encoding="utf-8")
    compile_pdf(tex_path, pdf_path, preferred_engine="auto")
    return {"json": json_path, "markdown": md_path, "tex": tex_path, "pdf": pdf_path}


def main() -> int:
    """Generate the proof-discovery language report."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=Path(__file__).resolve().parents[4] / "docs",
        help="Directory where the proof-discovery language artifacts should be written.",
    )
    args = parser.parse_args()
    write_outputs(docs_dir=args.docs_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
