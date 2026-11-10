#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Export Markdown documents in phyp/ to LaTeX and PDF."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


def _slug_title(path: Path) -> str:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Stable naming and path-derivation helper for artifact routing.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    stem = path.stem.replace("_", " ").replace("-", " ").strip()
    return " ".join(chunk.capitalize() for chunk in stem.split()) or path.stem


def _run(cmd: list[str]) -> None:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: Controlled subprocess execution with logging and error propagation.
    Contribution: Ensures stage execution is traceable and integrated into run-level reasoning logs.
    """

    subprocess.run(cmd, check=True)


def main() -> int:
    """
    Relevance: Operates within the orchestration and observability layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("phyp-doc-exporter")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phyp-dir", default="phyp", help="Directory containing Markdown files.")
    ap.add_argument("--pattern", default="*.md", help="Glob pattern for Markdown files.")
    ap.add_argument(
        "--include-readme",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Include README.md when exporting.",
    )
    ap.add_argument(
        "--pdf-engine",
        default="xelatex",
        help="Pandoc PDF engine (e.g. xelatex, pdflatex).",
    )
    args = ap.parse_args()

    logger.step(
        "Parsed phyp-doc-exporter arguments",
        "\n".join(
            [
                f"phyp_dir={args.phyp_dir}",
                f"pattern={args.pattern}",
                f"include_readme={args.include_readme}",
                f"pdf_engine={args.pdf_engine}",
            ]
        ),
    )

    phyp_dir = Path(args.phyp_dir)
    if not phyp_dir.exists():
        log_path = logger.finalize("error", summary=f"phyp directory not found: {phyp_dir}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] phyp directory not found: {phyp_dir}")

    pandoc = shutil.which("pandoc")
    if not pandoc:
        log_path = logger.finalize("error", summary="pandoc not found in PATH.")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit("[ERROR] pandoc not found in PATH.")
    if not shutil.which(args.pdf_engine):
        log_path = logger.finalize("error", summary=f"PDF engine not found in PATH: {args.pdf_engine}")
        print(f"[LOG] {log_path}", file=sys.stderr)
        raise SystemExit(f"[ERROR] PDF engine not found in PATH: {args.pdf_engine}")

    md_paths = sorted(phyp_dir.glob(args.pattern))
    filtered: list[Path] = []
    for path in md_paths:
        if not path.is_file():
            continue
        if not args.include_readme and path.name.lower() == "readme.md":
            continue
        filtered.append(path)

    if not filtered:
        print(f"[OK] No Markdown files matched in {phyp_dir} (pattern={args.pattern}).")
        log_path = logger.finalize("success", summary="No Markdown files to export.")
        print(f"[LOG] {log_path}")
        return 0

    logger.step("Discovered Markdown files", f"count={len(filtered)}")

    for md in filtered:
        tex = md.with_suffix(".tex")
        pdf = md.with_suffix(".pdf")
        title = _slug_title(md)

        _run(
            [
                pandoc,
                str(md),
                "--from",
                "gfm",
                "--to",
                "latex",
                "--standalone",
                "--metadata",
                f"title={title}",
                "--output",
                str(tex),
            ]
        )
        _run(
            [
                pandoc,
                str(md),
                "--from",
                "gfm",
                "--to",
                "pdf",
                "--standalone",
                "--pdf-engine",
                args.pdf_engine,
                "--metadata",
                f"title={title}",
                "--output",
                str(pdf),
            ]
        )

        logger.add_output("latex_document", tex)
        logger.add_output("pdf_document", pdf)
        print(f"[OK] Exported: {md} -> {tex.name}, {pdf.name}")

    log_path = logger.finalize("success", summary=f"Exported {len(filtered)} Markdown files to TeX/PDF.")
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
