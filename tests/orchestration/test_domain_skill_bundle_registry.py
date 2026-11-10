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

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[2]


def _load():
    schema = yaml.safe_load((ROOT / "agentic/spec/domain_skill_bundle.schema.json").read_text())
    registry = yaml.safe_load((ROOT / "agentic/registries/domain_skill_bundles.yaml").read_text())
    jsonschema.validate(registry, schema)
    return registry["bundles"][0]


def test_ym_bundle_is_explicit_private_and_complete():
    bundle = _load()
    assert bundle["domain_id"] == "ym"
    assert bundle["workflow_id"] == "cohere_fast"
    assert bundle["discovery"] == "bundle-private-explicit-allowlist"
    assert bundle["enabled"] is False
    actual = {p.parent.name for p in (ROOT / bundle["root"]).glob("*/SKILL.md")}
    assert actual == set(bundle["allowed_skills"])
    assert len(actual) == 30


def test_bundle_paths_and_global_skills_do_not_overlap():
    bundle = _load()
    private = ROOT / bundle["root"]
    assert private.is_relative_to(ROOT / "skills/domain_specific")
    for skill in bundle["allowed_skills"]:
        text = (private / skill / "SKILL.md").read_text()
        assert "cohere_fast" in text and "DomainEvidencePacket" in text
        assert "Claim ceiling" in text and "Stop and quarantine" in text
