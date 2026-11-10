# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Exercise the installed research environment without starting a research run.

This operator check uses the same child environment as a native job. It checks
real numerical/symbolic operations and canonical PDF extraction, rather than
assuming a package's presence proves that its binaries or scripts can run.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def verify(source: Path) -> dict:
    from .execution_registry import ExecutionRegistry
    from .startup import preload
    from .worker import worker_environment

    import numpy as np
    from scipy.integrate import quad
    import sympy as sp
    from pypdf import PdfWriter
    from pypdf.generic import (
        DecodedStreamObject,
        DictionaryObject,
        NameObject,
    )

    source = source.resolve(strict=True)
    setup = preload(ExecutionRegistry(source))
    if setup["status"] != "ready":
        raise ValueError("Startup dependencies are not ready")
    if sys.prefix == sys.base_prefix:
        raise ValueError("Run this check with Abducer's dedicated virtual environment")
    child_environment = worker_environment()
    child_environment["PYTHONPATH"] += os.pathsep + str(source)
    binary = shutil.which("python", path=child_environment["PATH"])
    if not binary:
        raise ValueError("Managed Python is not discoverable in the child PATH")
    child = json.loads(
        subprocess.check_output(
            [
                binary,
                "-c",
                "import json,sys,site; print(json.dumps([sys.prefix,site.ENABLE_USER_SITE]))",
            ],
            env=child_environment,
            cwd=tempfile.gettempdir(),
            text=True,
        )
    )
    if child != [sys.prefix, False]:
        raise ValueError("Child Python escaped the isolated environment")
    aliases = []
    source_manifest = source / ".abducer-source.json"
    if source_manifest.is_file():
        from .runtime import verify_snapshot

        declared = verify_snapshot(source).get("python_launchers", [])
        expected = {
            f"{folder}/bin/{name}"
            for folder in (".venv", ".venv-pmp")
            for name in ("python", "python3")
        }
        if declared and (set(declared) != expected or len(declared) != len(expected)):
            raise ValueError("Unexpected Python compatibility launcher inventory")
        for relative in declared:
            command = source / relative
            resolved = json.loads(
                subprocess.check_output(
                    [
                        str(command),
                        "-c",
                        "import json,sys; print(json.dumps(sys.prefix))",
                    ],
                    env=child_environment,
                    cwd=tempfile.gettempdir(),
                    text=True,
                )
            )
            if resolved != sys.prefix:
                raise ValueError(
                    "Historical Python command escaped the managed environment"
                )
            aliases.append(relative)
    np.testing.assert_allclose(
        np.linalg.solve([[2.0, 1.0], [1.0, 3.0]], [3.0, 4.0]), [1.0, 1.0]
    )
    if abs(quad(lambda x: x * x, 0, 1)[0] - 1 / 3) > 1e-12:
        raise ValueError("Numerical integration failed")
    x = sp.Symbol("x")
    if sp.simplify(sp.diff(sp.sin(x) ** 2 + sp.cos(x) ** 2, x)) != 0:
        raise ValueError("Symbolic differentiation failed")

    # Produce a tiny text-bearing PDF, then use the actual canonical reader.
    with tempfile.TemporaryDirectory(prefix="abducer-environment-check-") as directory:
        pdf = Path(directory) / "sample.pdf"
        writer = PdfWriter()
        page = writer.add_blank_page(width=300, height=200)
        font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type1"),
                NameObject("/BaseFont"): NameObject("/Helvetica"),
            }
        )
        page[NameObject("/Resources")] = DictionaryObject(
            {
                NameObject("/Font"): DictionaryObject(
                    {NameObject("/F1"): writer._add_object(font)}
                )
            }
        )
        content = DecodedStreamObject()
        content.set_data(
            b"BT /F1 12 Tf 30 100 Td (Abducer PDF environment check) Tj ET"
        )
        page[NameObject("/Contents")] = writer._add_object(content)
        writer.write(pdf)
        spec = importlib.util.spec_from_file_location(
            "abducer_pdf_probe",
            source / "skills/ingest/latex-kb-ingest/scripts/chunk_sources.py",
        )
        if spec is None or spec.loader is None:
            raise ValueError("Canonical PDF reader is absent")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if "Abducer PDF environment check" not in module._read_pdf_text(pdf):
            raise ValueError("Canonical PDF extraction failed")
    return {
        "status": "passed",
        "python": sys.version.split()[0],
        "child_environment_isolated": True,
        "python_aliases_verified": aliases,
        "numerical_and_symbolic_checks": "passed",
        "canonical_pdf_extraction": "passed",
        "dependency_setup": setup,
        "scientific_execution_started": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        default=os.environ.get("ABDUCER_REPOSITORY_ROOT", "."),
    )
    args = parser.parse_args()
    result = verify(args.source_root)
    # Summarize without publishing local paths or complete source inventories.
    result["dependency_setup"] = {
        key: result["dependency_setup"][key]
        for key in ("status", "skills", "workflows", "source_files", "packages")
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
