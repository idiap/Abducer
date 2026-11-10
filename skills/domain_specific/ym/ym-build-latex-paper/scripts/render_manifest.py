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
"""Render a bounded TeX fixture and optionally compile it inside one run root."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def inside(root: Path, candidate: Path) -> Path:
    root = root.resolve()
    candidate = candidate.resolve()
    if candidate == root or root not in candidate.parents:
        raise ValueError("output must be a child of the cohere-fast run root")
    return candidate


def atomic_write(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".cohere-fast-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)


def render(run_root: Path, relative_output: str, title: str, compile_pdf: bool) -> dict:
    if any(token in title for token in ("\\input", "\\include", "\\write18")):
        raise ValueError("unsafe TeX control sequence")
    output = inside(run_root, run_root / relative_output)
    if output.suffix != ".tex": raise ValueError("output must end in .tex")
    escaped = title.translate(str.maketrans({"\\": r"\textbackslash{}", "{": r"\{", "}": r"\}", "%": r"\%", "$": r"\$", "#": r"\#", "&": r"\&", "_": r"\_"}))
    body = ("\\documentclass{article}\n\\begin{document}\n"
            f"\\title{{{escaped}}}\\maketitle\n"
            "Candidate research artifact; no workflow status implies proof.\n"
            "\\end{document}\n").encode()
    atomic_write(output, body)
    result = {"schema_version": "1.0", "tex": output.name, "sha256": hashlib.sha256(body).hexdigest(), "compile_status": "not_requested"}
    if compile_pdf:
        exe = shutil.which("pdflatex")
        if not exe:
            result["compile_status"] = "optional_dependency_missing"
        else:
            env = {"PATH": str(Path(exe).parent), "HOME": str(run_root.resolve()), "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "openin_any": "p", "openout_any": "p"}
            completed = subprocess.run([exe, "-interaction=nonstopmode", "-halt-on-error", output.name], cwd=output.parent, env=env, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=30, check=False)
            result["compile_status"] = "compiled" if completed.returncode == 0 else "bounded_compile_failure"
            result["returncode"] = completed.returncode
    manifest = inside(run_root, output.with_suffix(".manifest.json"))
    atomic_write(manifest, (json.dumps(result, sort_keys=True, indent=2) + "\n").encode())
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--output", default="paper/paper.tex")
    parser.add_argument("--title", default="Cohere-fast YM candidate")
    parser.add_argument("--compile", action="store_true")
    args = parser.parse_args()
    print(json.dumps(render(args.run_root, args.output, args.title, args.compile), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
