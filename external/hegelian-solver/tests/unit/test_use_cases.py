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

from hegelian_solver.formalizer import formalize_concept
from hegelian_solver.use_cases import load_use_cases, run_use_case_suite, validate_use_cases


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "hegelian_solver/examples/use_cases/spec_use_cases.yaml"


def test_spec_use_cases_validate_formal_material_epistemic_blocks():
    cases = load_use_cases(MANIFEST)

    assert len(cases) == 65
    assert validate_use_cases(MANIFEST) == []
    for raw in cases:
        concept = formalize_concept(raw)
        assert concept.formal_analysis
        assert concept.material_analysis
        assert concept.epistemic_profile
        assert concept.source_refs


def test_use_case_suite_runner_smoke(tmp_path):
    result = run_use_case_suite(path=MANIFEST, output_dir=tmp_path, limit=3)

    assert result.total == 3
    assert result.failed == 0
    assert (tmp_path / "suite_result.json").exists()
    assert all(item.formal_material_epistemic == {"formal": True, "material": True, "epistemic": True} for item in result.items)
    assert all(item.trace_file and Path(item.trace_file).exists() for item in result.items)
