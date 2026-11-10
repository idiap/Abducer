# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "skills/domain_specific/ym/ym-build-latex-paper/scripts/render_manifest.py"
spec = importlib.util.spec_from_file_location("ym_renderer", SCRIPT)
renderer = importlib.util.module_from_spec(spec); spec.loader.exec_module(renderer)


def test_renderer_is_deterministic_bounded_and_non_overwriting(tmp_path):
    run = tmp_path / "run"; run.mkdir()
    result = renderer.render(run, "paper/main.tex", "YM candidate", False)
    assert result["compile_status"] == "not_requested"
    assert (run / "paper/main.manifest.json").is_file()
    with pytest.raises(FileExistsError): renderer.render(run, "paper/main.tex", "YM candidate", False)


@pytest.mark.parametrize("path", ["../escape.tex", "/tmp/escape.tex", "paper/not-tex.txt"])
def test_renderer_rejects_unsafe_output_paths(tmp_path, path):
    with pytest.raises(ValueError): renderer.render(tmp_path, path, "safe", False)


def test_renderer_rejects_tex_file_inclusion(tmp_path):
    with pytest.raises(ValueError): renderer.render(tmp_path, "paper/main.tex", r"\\input{/etc/passwd}", False)


def test_compile_has_bounded_optional_dependency_outcome(tmp_path):
    result = renderer.render(tmp_path, "paper/main.tex", "YM candidate", True)
    assert result["compile_status"] in {"compiled", "bounded_compile_failure", "optional_dependency_missing"}
