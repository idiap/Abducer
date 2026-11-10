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
"""Integrate validated second-wave Route A result blocks into a TeX manuscript."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any


FORBIDDEN = (
    "pipeline",
    "workflow",
    "TODO",
    "todo",
    "result-elaboration",
    "implementation packet",
    "agent",
    "skill",
    "queue",
)


def scan_forbidden(text: str) -> list[str]:
    lowered = text.lower()
    return [term for term in FORBIDDEN if term.lower() in lowered]


def insert_after_label(text: str, label: str, block: str) -> str:
    pattern = re.compile(rf"(\\label\{{{re.escape(label)}\}})")
    match = pattern.search(text)
    if not match:
        raise ValueError(f"label not found: {label}")
    insert_at = text.find("\n", match.end())
    if insert_at == -1:
        insert_at = match.end()
    return text[: insert_at + 1] + "\n" + block.strip() + "\n" + text[insert_at + 1 :]


def integrate(paper: Path, result: dict[str, Any], output: Path, compile_pdf: bool) -> dict[str, Any]:
    text = paper.read_text(encoding="utf-8")
    block = result.get("tex_block", "").strip()
    if not block:
        shutil.copyfile(paper, output)
        changed = False
    else:
        forbidden_block = scan_forbidden(block)
        if forbidden_block:
            raise ValueError(f"forbidden paper language in result block: {forbidden_block}")
        label = result.get("insert_after_label", "sec:open-modules")
        text = insert_after_label(text, label, block)
        output.write_text(text, encoding="utf-8")
        changed = True
    forbidden_paper = scan_forbidden(output.read_text(encoding="utf-8"))
    compile_status: dict[str, Any] = {"attempted": False}
    pdf_path = None
    if compile_pdf:
        build_dir = output.parent / f"{output.stem}_compile"
        build_dir.mkdir(parents=True, exist_ok=True)
        cmd = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", str(build_dir), str(output)]
        first = subprocess.run(cmd, cwd=Path.cwd(), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        second = subprocess.run(cmd, cwd=Path.cwd(), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) if first.returncode == 0 else first
        pdf_path = build_dir / f"{output.stem}.pdf"
        compile_status = {
            "attempted": True,
            "returncode": second.returncode,
            "pdf": str(pdf_path) if pdf_path.exists() else None,
        }
    return {
        "schema": "abducer.routea_second_wave_revision_manifest.v1",
        "source_paper": str(paper),
        "output_tex": str(output),
        "changed": changed,
        "source_artifact": result.get("source_artifact"),
        "result_type": result.get("result_type", "no-change"),
        "changed_claims": result.get("changed_claims", []),
        "nonclaims": result.get("nonclaims", []),
        "forbidden_language_hits": forbidden_paper,
        "compile_status": compile_status,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", type=Path)
    parser.add_argument("result", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compile", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    result = json.loads(args.result.read_text(encoding="utf-8")) if args.result else {"result_type": "no-change"}
    output = args.output or args.paper.with_name(args.paper.stem + "_second_wave.tex")
    manifest = integrate(args.paper, result, output, args.compile)
    manifest_path = args.manifest or output.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    if manifest["forbidden_language_hits"]:
        return 1
    if manifest["compile_status"].get("attempted") and manifest["compile_status"].get("returncode") != 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
