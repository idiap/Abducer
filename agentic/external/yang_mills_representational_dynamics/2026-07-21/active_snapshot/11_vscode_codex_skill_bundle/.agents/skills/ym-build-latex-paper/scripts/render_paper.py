#!/usr/bin/env python3
"""Compile a LaTeX paper, validate the PDF, and render inspection previews."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from lint_manuscript import inspect_project


UNDEFINED_RE = re.compile(
    r"(?:LaTeX Warning: (?:Reference|Citation).+undefined|There were undefined references)",
    re.IGNORECASE,
)
OVERFULL_RE = re.compile(r"Overfull \\[hv]box")


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def page_count(info: str) -> int:
    match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    return int(match.group(1)) if match else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("main_tex", type=Path)
    parser.add_argument("--outdir", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--no-preview", action="store_true")
    args = parser.parse_args()

    main_tex = args.main_tex.resolve()
    root = main_tex.parent
    outdir = (args.outdir or root / "build").resolve()
    report_path = (args.report or outdir / "build_report.json").resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    report: dict[str, object] = {
        "main": str(main_tex),
        "outdir": str(outdir),
        "strict": args.strict,
        "status": "failed",
    }

    try:
        lint = inspect_project(main_tex)
    except (OSError, UnicodeError) as exc:
        report["error"] = f"lint failed: {exc}"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(report["error"], file=sys.stderr)
        return 2
    report["lint"] = lint
    if lint["errors"] or (args.strict and lint["warnings"]):
        report["error"] = "manuscript lint gate failed"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 3

    required = ["latexmk", "pdfinfo", "pdftotext"]
    if not args.no_preview:
        required.append("pdftoppm")
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        report["error"] = f"missing required executables: {missing}"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(report["error"], file=sys.stderr)
        return 4

    command = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-outdir={outdir}",
        main_tex.name,
    ]
    compiled = run(command, root)
    report["latexmk"] = {
        "command": command,
        "returncode": compiled.returncode,
        "output_tail": compiled.stdout[-12000:],
    }
    pdf = outdir / f"{main_tex.stem}.pdf"
    if compiled.returncode != 0 or not pdf.is_file():
        report["error"] = "LaTeX compilation failed"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 5

    log_path = outdir / f"{main_tex.stem}.log"
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    undefined = UNDEFINED_RE.findall(log)
    overfull = OVERFULL_RE.findall(log)
    report["log_checks"] = {
        "undefined_reference_or_citation_count": len(undefined),
        "overfull_box_count": len(overfull),
    }

    info_run = run(["pdfinfo", str(pdf)], root)
    pages = page_count(info_run.stdout)
    report["pdfinfo"] = {
        "returncode": info_run.returncode,
        "output": info_run.stdout,
        "pages": pages,
    }
    if info_run.returncode != 0 or pages < 1:
        report["error"] = "PDF metadata validation failed"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 6

    text_path = outdir / f"{main_tex.stem}.txt"
    text_run = run(["pdftotext", str(pdf), str(text_path)], root)
    extracted = text_path.read_text(encoding="utf-8", errors="replace") if text_path.exists() else ""
    report["text_validation"] = {
        "returncode": text_run.returncode,
        "characters": len(extracted.strip()),
    }
    if text_run.returncode != 0 or len(extracted.strip()) < 80:
        report["error"] = "PDF text extraction validation failed"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 7

    previews: list[str] = []
    if not args.no_preview:
        preview_dir = outdir / "previews"
        preview_dir.mkdir(exist_ok=True)
        selected = sorted({1, max(1, (pages + 1) // 2), pages})
        for page in selected:
            prefix = preview_dir / f"page-{page:04d}"
            preview_run = run(
                [
                    "pdftoppm",
                    "-png",
                    "-r",
                    "150",
                    "-f",
                    str(page),
                    "-l",
                    str(page),
                    "-singlefile",
                    str(pdf),
                    str(prefix),
                ],
                root,
            )
            image = prefix.with_suffix(".png")
            if preview_run.returncode != 0 or not image.is_file():
                report["error"] = f"preview rendering failed for page {page}"
                report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
                return 8
            previews.append(str(image))

    report["pdf"] = {
        "path": str(pdf),
        "bytes": pdf.stat().st_size,
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
        "previews": previews,
    }
    if args.strict and undefined:
        report["error"] = "undefined references or citations remain"
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        return 9

    report["status"] = "passed"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
