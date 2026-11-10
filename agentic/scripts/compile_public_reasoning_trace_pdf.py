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
"""Compile a public reasoning-trace TeX file in a bounded scratch directory.

The compiler deliberately accepts only a TeX file and fixed command-line options.
Packet content cannot influence the executable, arguments, environment, working
directory, or promoted paths.  TeX safety validation remains a prerequisite: TeX
is not a security boundary, even when shell escape is disabled.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable


ENGINE_ORDER = ("latexmk", "xelatex", "pdflatex", "lualatex")
DIAGNOSTIC_LIMIT = 12_000
DEFAULT_SOURCE_DATE_EPOCH = 946684800  # 2000-01-01, accepted by PDF toolchains.
MATERIAL_OVERFULL_PT = 12.0


class PdfCompilationError(RuntimeError):
    """A safe compilation or promotion failed."""


@dataclass(frozen=True)
class Engine:
    name: str
    executable: str
    version: str


def _bounded(value: str, limit: int = DIAGNOSTIC_LIMIT) -> str:
    value = value.replace("\x00", "")
    if len(value) <= limit:
        return value
    return f"[... {len(value) - limit} characters omitted ...]\n{value[-limit:]}"


def _safe_environment(scratch: Path, source_date_epoch: int) -> dict[str, str]:
    # PATH is needed to let latexmk locate its selected TeX engine. Everything
    # else is deliberately rebuilt instead of inheriting credentials/config.
    return {
        "PATH": os.environ.get("PATH", os.defpath),
        "HOME": str(scratch),
        "TMPDIR": str(scratch),
        "TZ": "UTC",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "SOURCE_DATE_EPOCH": str(source_date_epoch),
        "FORCE_SOURCE_DATE": "1",
        "openin_any": "p",
        "openout_any": "p",
        "TEXMFOUTPUT": str(scratch),
        "max_print_line": "2000",
    }


def _version(executable: str) -> str:
    try:
        result = subprocess.run(
            [executable, "--version"], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return _bounded((result.stdout or result.stderr).splitlines()[0] if (result.stdout or result.stderr) else "unknown", 500)


def discover_engine(preferred: str = "auto") -> Engine | None:
    if preferred not in {"auto", *ENGINE_ORDER}:
        raise ValueError(f"unsupported TeX engine {preferred!r}; choose auto or {', '.join(ENGINE_ORDER)}")
    names: Iterable[str] = ENGINE_ORDER if preferred == "auto" else (preferred,)
    for name in names:
        executable = shutil.which(name)
        if executable:
            return Engine(name=name, executable=executable, version=_version(executable))
    return None


def _command(engine: Engine, tex_name: str) -> tuple[list[str], int]:
    common = ["-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-no-shell-escape"]
    if engine.name == "latexmk":
        return ([engine.executable, "-pdf", *common, tex_name], 1)
    return ([engine.executable, *common, tex_name], 2)


def _diagnostic_warnings(diagnostics: str) -> list[str]:
    """Return stable release-significant warning codes from TeX output.

    TeX commonly exits successfully with an incomplete or damaged document.
    Keeping this parser next to compilation prevents such a PDF from being
    promoted merely because a later read-only validator was not run.
    """
    warnings: list[str] = []
    lowered = diagnostics.casefold()
    for marker, code in (
        ("undefined reference", "undefined-reference"),
        ("undefined citation", "undefined-citation"),
        ("missing character:", "missing-glyph"),
        ("destination with the same identifier", "duplicate-destination"),
    ):
        if marker in lowered:
            warnings.append(code)
    for match in re.finditer(
        r"Overfull \\[hv]box \(([-+0-9.]+)pt too (?:wide|high)\)", diagnostics, re.I
    ):
        if float(match.group(1)) > MATERIAL_OVERFULL_PT:
            warnings.append("material-overfull-box")
            break
    return warnings


def _validate_paths(tex_path: Path, pdf_path: Path, log_path: Path | None) -> None:
    if tex_path.suffix.lower() != ".tex" or not tex_path.is_file():
        raise PdfCompilationError(f"validated TeX input is missing or not .tex: {tex_path}")
    if pdf_path.suffix.lower() != ".pdf":
        raise PdfCompilationError(f"PDF output must use a .pdf suffix: {pdf_path}")
    resolved = [tex_path.resolve(strict=False), pdf_path.resolve(strict=False)]
    if log_path is not None:
        if Path(log_path).suffix.lower() != ".log":
            raise PdfCompilationError(f"diagnostic output must use a .log suffix: {log_path}")
        resolved.append(Path(log_path).resolve(strict=False))
    if len(set(resolved)) != len(resolved):
        raise PdfCompilationError("TeX, PDF, and diagnostic paths must be distinct")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def compile_pdf(
    tex_path: Path,
    pdf_path: Path,
    *,
    preferred_engine: str = "auto",
    release: bool = False,
    timeout_seconds: int = 120,
    log_path: Path | None = None,
    source_date_epoch: int = DEFAULT_SOURCE_DATE_EPOCH,
) -> dict[str, Any]:
    """Compile and atomically promote a PDF, returning bounded build metadata."""
    tex_path, pdf_path = Path(tex_path), Path(pdf_path)
    log_path = Path(log_path) if log_path is not None else None
    _validate_paths(tex_path, pdf_path, log_path)
    if timeout_seconds < 1 or timeout_seconds > 900:
        raise ValueError("timeout_seconds must be between 1 and 900")
    engine = discover_engine(preferred_engine)
    if engine is None:
        metadata = {
            "disposition": "compiler_unavailable", "engine": None, "engine_version": None,
            "arguments": [], "passes": 0, "duration_seconds": 0.0,
            "diagnostics": "No supported TeX engine found; validated TeX was retained.",
            "warnings": ["compiler_unavailable"], "source_date_epoch": source_date_epoch,
        }
        if release:
            raise PdfCompilationError(metadata["diagnostics"])
        return metadata

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="reasoning-trace-pdf-") as directory:
        scratch = Path(directory)
        local_tex = scratch / "reasoning-trace.tex"
        local_tex.write_bytes(tex_path.read_bytes())
        command, passes = _command(engine, local_tex.name)
        environment = _safe_environment(scratch, source_date_epoch)
        output_parts: list[str] = []
        try:
            for pass_number in range(1, passes + 1):
                result = subprocess.run(
                    command, cwd=scratch, env=environment, capture_output=True,
                    text=True, encoding="utf-8", errors="replace",
                    timeout=timeout_seconds, check=False,
                )
                output_parts.append(f"pass {pass_number} stdout:\n{result.stdout}\npass {pass_number} stderr:\n{result.stderr}")
                if result.returncode:
                    raise PdfCompilationError(
                        f"{engine.name} failed on pass {pass_number} (exit {result.returncode})\n{_bounded(''.join(output_parts))}"
                    )
        except subprocess.TimeoutExpired as exc:
            def decoded(value: str | bytes | None) -> str:
                return value.decode("utf-8", "replace") if isinstance(value, bytes) else (value or "")
            partial = decoded(exc.stdout) + decoded(exc.stderr)
            raise PdfCompilationError(f"{engine.name} exceeded the {timeout_seconds}s timeout\n{_bounded(partial)}") from exc

        built_pdf = local_tex.with_suffix(".pdf")
        if not built_pdf.is_file() or not built_pdf.read_bytes().startswith(b"%PDF-"):
            raise PdfCompilationError(f"{engine.name} returned success without a valid PDF")
        diagnostics = _bounded("\n".join(output_parts))
        warnings = _diagnostic_warnings(diagnostics)
        if release and warnings:
            raise PdfCompilationError(
                "release-significant TeX diagnostics prevented promotion: " + ", ".join(warnings)
            )
        # Promotion happens only after all checks; an earlier valid PDF survives
        # every compiler failure and an interrupted temporary write.
        _atomic_write(pdf_path, built_pdf.read_bytes())
        if log_path is not None:
            _atomic_write(Path(log_path), diagnostics.encode("utf-8"))

    return {
        "disposition": "compiled", "engine": engine.name,
        "engine_version": engine.version,
        # Publish arguments without host-specific executable paths.
        "arguments": [engine.name, *command[1:]], "passes": passes,
        "duration_seconds": round(time.monotonic() - started, 3),
        "diagnostics": diagnostics, "warnings": warnings,
        "source_date_epoch": source_date_epoch,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", required=True, type=Path)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--engine", default="auto", choices=("auto", *ENGINE_ORDER))
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--release", action="store_true")
    args = parser.parse_args()
    try:
        metadata = compile_pdf(args.tex, args.pdf, preferred_engine=args.engine, release=args.release,
                               timeout_seconds=args.timeout, log_path=args.log)
    except PdfCompilationError as exc:
        parser.exit(2, f"PDF compilation failed: {exc}\n")
    if args.metadata:
        _atomic_write(args.metadata, (json.dumps(metadata, indent=2, sort_keys=True) + "\n").encode())
    print(json.dumps(metadata, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
