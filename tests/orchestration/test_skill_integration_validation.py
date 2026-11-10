# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from validate_skill_integration import (  # noqa: E402
    LEVELS,
    IntegrationError,
    _attained_level,
    build_report,
)


def test_all_repository_skills_reconcile_across_integration_surfaces() -> None:
    report = build_report(ROOT)

    # Compare exact canonical identities as well as counts, so registry growth
    # cannot conceal missing or duplicate integration rows.
    registry = json.loads((ROOT / "agentic/registries/skill_registry.yaml").read_text())["skills"]
    expected_names = {row["name"] for row in registry}
    assert len(expected_names) == len(registry)
    assert len(report["skills"]) == len(expected_names)
    assert {row["skill_id"] for row in report["skills"]} == expected_names
    assert report["skill_count"] == len(expected_names)
    assert report["dispositions_complete"] is True
    assert report["evidence_ladder"] == list(LEVELS)
    assert report["level_counts"]["catalogued"] == len(expected_names)
    standalone = {"orch", "route"}
    assert {row["skill_id"] for row in report["skills"] if row["disposition"] == "standalone"} == standalone
    assert {row["skill_id"] for row in report["skills"] if row["levels"]["workflow_declared"]} == expected_names - standalone
    assert report["level_counts"]["workflow_declared"] == len(expected_names - standalone)
    assert sum(report["disposition_counts"].values()) == len(expected_names)
    assert report["disposition_counts"].get("standalone", 0) == len(standalone)
    assert all(row["levels"]["catalogued"] for row in report["skills"])


def test_six_previously_missing_skills_are_catalogued() -> None:
    expected = {
        "theory-atlas-defect-compiler",
        "central-formal-conceptual-routes",
        "conceptual-frontier-deepening",
        "pvsnp-negative-tactic-selector",
        "formal-claim-producer",
        "literature-conditioned-invention-forger",
    }
    catalog = (ROOT / "docs/reference/skills.md").read_text(encoding="utf-8")

    for skill in expected:
        assert f"/{skill}/SKILL.md)" in catalog


def test_advisory_and_conditional_declarations_do_not_imply_execution() -> None:
    report = build_report(ROOT)
    rows = {row["skill_id"]: row for row in report["skills"]}
    candidates = [
        row
        for row in rows.values()
        if row["levels"]["workflow_declared"]
        and any(item["mode"] in {"advisory", "conditional"} for item in row["declarations"])
        and not row["levels"]["runtime_routed"]
    ]

    assert candidates
    assert all(not row["levels"]["executable"] for row in candidates)


def test_evidence_ladder_rejects_skipped_levels() -> None:
    flags = {level: False for level in LEVELS}
    flags["catalogued"] = True
    flags["workflow_declared"] = True
    flags["executable"] = True

    with pytest.raises(IntegrationError, match="runtime_routed"):
        _attained_level("broken-skill", flags)
