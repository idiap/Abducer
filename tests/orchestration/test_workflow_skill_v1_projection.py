# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Check projection drift, nominal interfaces and non-executable boundaries.

These checks inspect contracts only. In particular they never import a native
workflow executor, create scientific receipts, or regenerate report artifacts.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

from agentic.scripts import normalize_workflow_skills as exporter

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "integrations/workflow_contracts"


def validator():
    """Load the read-only authoring validator, never a bound operation."""
    spec = importlib.util.spec_from_file_location(
        "workflow_v1_validator", SKILL / "scripts/validate_workflow.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_generated_contracts_are_current():
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "agentic/scripts/normalize_workflow_skills.py"),
            "--check",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_schema_dataflow_and_source_digests():
    helper = validator()
    for path in exporter.projections(ROOT):
        result = helper.validate(ROOT / path, ROOT)
        assert result["valid"], result
        assert not result["runtime_bindings_verified"]
        assert not result["source_semantics_verified"]


def test_drafts_do_not_pass_declared_binding_gate():
    helper = validator()
    for path in exporter.projections(ROOT):
        result = helper.validate(ROOT / path, ROOT, require_declared_bindings=True)
        assert not result["valid"]
        assert all("binding is not declared" in e for e in result["errors"]), result


def test_registry_coverage_and_aliases_are_unambiguous():
    rows = list(exporter.projections(ROOT).values())
    assert len(rows) == 34
    identities = [(d["namespace"], d["id"], d["version"]) for d in rows]
    assert len(set(identities)) == len(identities)
    aliases = [(d["namespace"], alias) for d in rows for alias in d["aliases"]]
    assert len(set(aliases)) == len(aliases)
    for d in rows:
        assert d["id"].endswith("_workflow")
        assert (ROOT / d["extensions"]["abducer.owner"]["path"]).is_file()


def test_named_steps_retain_roles_guards_failure_and_nominal_ports():
    for descriptor in exporter.projections(ROOT).values():
        mapping = descriptor["extensions"].get("abducer.step_interfaces")
        if mapping is None:
            continue
        native = descriptor["extensions"]["abducer.native_contract"]
        assert list(mapping) == [step["id"] for step in native["steps"]]
        for step in native["steps"]:
            operation = descriptor["operations"][mapping[step["id"]]]
            assert list(operation["inputs"]) == step["consumes"]
            assert list(operation["outputs"]) == step["produces"]
            assert all(p["type"] == name for name, p in operation["inputs"].items())
        assert native["exit_gate"]
        assert native["hooks"]
        assert native["handoffs"]


def test_native_rows_are_not_rewritten():
    documents = exporter.projections(ROOT)
    for registry, identities in [
        ("workflow_contracts.yaml", exporter.LEGACY),
        ("named_workflow_contracts.yaml", exporter.NAMED),
    ]:
        source = yaml.safe_load((ROOT / exporter.REG / registry).read_text())
        for row in source["workflows"]:
            projected = documents[
                exporter.DEST / identities[row["id"]] / "workflow.yaml"
            ]
            assert projected["extensions"]["abducer.native_contract"] == row


def test_no_draft_licenses_execution_or_promotion():
    for d in exporter.projections(ROOT).values():
        assert d["lifecycle"] == "draft"
        assert d["provenance"]["coverage"] == "interface_only"
        assert d["provenance"]["gaps"]
        assert d["policy"]["effects"]["filesystem"]["write"] == []
        assert d["policy"]["effects"]["network"] == []
        assert d["policy"]["effects"]["external_write"] == []
        for op in d["operations"].values():
            assert op["execution"]["mode"] == "specification_only"
            assert "binding" not in op["execution"]


def test_source_tamper_is_rejected(tmp_path):
    # A real descriptor copy still points to the real repository sources, so
    # corrupting a digest isolates provenance validation from YAML validity.
    helper = validator()
    path, d = next(iter(exporter.projections(ROOT).items()))
    for source in d["provenance"]["sources"]:
        target = tmp_path / source["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source["path"], target)
    d["provenance"]["sources"][0]["digest"] = "sha256:" + "0" * 64
    copy = tmp_path / "workflow.yaml"
    # This selected legacy descriptor has inline types and no relative refs.
    copy.write_text(yaml.safe_dump(d))
    result = helper.validate(copy, tmp_path)
    assert not result["valid"]
    assert any("source digest mismatch" in error for error in result["errors"])


def test_check_rejects_missing_projections(tmp_path):
    # Reconstruct just the exporter input surface. A missing descriptor must
    # fail the read-only check instead of being silently skipped or recreated.
    sources = {
        s["path"]
        for d in exporter.projections(ROOT).values()
        for s in d["provenance"]["sources"]
    }
    for source in sources:
        target = tmp_path / source
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / source, target)
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "agentic/scripts/normalize_workflow_skills.py"),
            "--repository-root",
            str(tmp_path),
            "--check",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1, result.stderr
    assert "stale_or_missing" in result.stdout
    assert not (tmp_path / exporter.DEST).exists()
