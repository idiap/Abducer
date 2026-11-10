# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
from pathlib import Path
from types import SimpleNamespace

import pytest

from agentic.scripts import compile_public_reasoning_trace_pdf as compiler


def test_missing_engine_is_explicit_in_development_and_fatal_in_release(tmp_path, monkeypatch):
    tex = tmp_path / "trace.tex"
    tex.write_text("validated", encoding="utf-8")
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: None)
    metadata = compiler.compile_pdf(tex, tmp_path / "trace.pdf")
    assert metadata["disposition"] == "compiler_unavailable"
    assert not (tmp_path / "trace.pdf").exists()
    with pytest.raises(compiler.PdfCompilationError, match="No supported"):
        compiler.compile_pdf(tex, tmp_path / "trace.pdf", release=True)


def test_compiler_uses_fixed_no_shell_escape_arguments_and_atomic_outputs(tmp_path, monkeypatch):
    tex = tmp_path / "unsafe name.tex"
    tex.write_text(r"\documentclass{article}\begin{document}safe\end{document}", encoding="utf-8")
    pdf = tmp_path / "published.pdf"
    log = tmp_path / "published.log"
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: compiler.Engine("pdflatex", "/tool/pdflatex", "pdfTeX test"))
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        (Path(kwargs["cwd"]) / "reasoning-trace.pdf").write_bytes(b"%PDF-1.4\nfixture")
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr(compiler.subprocess, "run", fake_run)
    metadata = compiler.compile_pdf(tex, pdf, log_path=log)
    assert metadata["disposition"] == "compiled"
    assert metadata["passes"] == 2
    assert pdf.read_bytes().startswith(b"%PDF-")
    assert log.read_text().count("stdout") == 2
    for command, kwargs in calls:
        assert command == ["/tool/pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "-no-shell-escape", "reasoning-trace.tex"]
        assert kwargs["env"]["openin_any"] == "p"
        assert kwargs["env"]["openout_any"] == "p"
        assert kwargs["env"]["TZ"] == "UTC"
        assert kwargs.get("shell") is None
    assert all(not Path(arg).is_absolute() for arg in metadata["arguments"])


def test_failed_compile_preserves_existing_pdf_and_cleans_scratch(tmp_path, monkeypatch):
    tex, pdf = tmp_path / "trace.tex", tmp_path / "trace.pdf"
    tex.write_text("validated", encoding="utf-8")
    pdf.write_bytes(b"%PDF-old")
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: compiler.Engine("xelatex", "/tool/xelatex", "test"))
    monkeypatch.setattr(compiler.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1, stdout="bad", stderr="missing.sty"))
    with pytest.raises(compiler.PdfCompilationError, match="missing.sty"):
        compiler.compile_pdf(tex, pdf)
    assert pdf.read_bytes() == b"%PDF-old"


def test_engine_selection_is_validated(monkeypatch):
    with pytest.raises(ValueError, match="unsupported"):
        compiler.discover_engine("packet-controlled-command")


@pytest.mark.parametrize("alias", ["pdf", "log"])
def test_output_aliases_and_wrong_suffixes_are_rejected_before_execution(tmp_path, monkeypatch, alias):
    tex = tmp_path / "trace.tex"
    tex.write_text("validated", encoding="utf-8")
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: pytest.fail("engine must not be discovered"))
    if alias == "pdf":
        with pytest.raises(compiler.PdfCompilationError, match=".pdf suffix"):
            compiler.compile_pdf(tex, tex)
    else:
        with pytest.raises(compiler.PdfCompilationError, match=".log suffix"):
            compiler.compile_pdf(tex, tmp_path / "trace.pdf", log_path=tmp_path / "diagnostics.txt")


def test_release_warning_gate_preserves_previous_pdf(tmp_path, monkeypatch):
    tex, pdf = tmp_path / "trace.tex", tmp_path / "trace.pdf"
    tex.write_text("validated", encoding="utf-8")
    pdf.write_bytes(b"%PDF-previous")
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: compiler.Engine("pdflatex", "/tool/pdflatex", "test"))

    def fake_run(command, **kwargs):
        (Path(kwargs["cwd"]) / "reasoning-trace.pdf").write_bytes(b"%PDF-new")
        return SimpleNamespace(returncode=0, stdout="LaTeX Warning: There were undefined references.", stderr="")

    monkeypatch.setattr(compiler.subprocess, "run", fake_run)
    with pytest.raises(compiler.PdfCompilationError, match="undefined-reference"):
        compiler.compile_pdf(tex, pdf, release=True)
    assert pdf.read_bytes() == b"%PDF-previous"


def test_development_compile_reports_material_warnings(tmp_path, monkeypatch):
    tex, pdf = tmp_path / "trace.tex", tmp_path / "trace.pdf"
    tex.write_text("validated", encoding="utf-8")
    monkeypatch.setattr(compiler, "discover_engine", lambda preferred: compiler.Engine("pdflatex", "/tool/pdflatex", "test"))

    def fake_run(command, **kwargs):
        (Path(kwargs["cwd"]) / "reasoning-trace.pdf").write_bytes(b"%PDF-new")
        return SimpleNamespace(returncode=0, stdout="Overfull \\hbox (13.5pt too wide)", stderr="")

    monkeypatch.setattr(compiler.subprocess, "run", fake_run)
    metadata = compiler.compile_pdf(tex, pdf)
    assert metadata["warnings"] == ["material-overfull-box"]
