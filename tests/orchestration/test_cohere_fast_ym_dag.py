# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
import json
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]


def test_ym_dag_is_acyclic_complete_and_audit_gated():
    wf = yaml.safe_load((ROOT / "agentic/registries/cohere_fast_ym_workflow.yaml").read_text())
    nodes = {n["id"]: n for n in wf["nodes"]}
    assert len(nodes) == 30
    seen = set()
    while len(seen) < len(nodes):
        ready = {i for i, n in nodes.items() if i not in seen and set(n["depends_on"]) <= seen}
        assert ready, "cycle or unbound dependency"
        seen |= ready
    skills = {n["skill"] for n in nodes.values()}
    bundle = yaml.safe_load((ROOT / "agentic/registries/domain_skill_bundles.yaml").read_text())["bundles"][0]
    assert skills == set(bundle["allowed_skills"])
    for release in ("frame_narrative", "proof_appendix"):
        assert "audit_frontier" in nodes[release]["depends_on"]


def test_dependency_projection_agrees_with_workflow():
    graph = json.loads((ROOT / "agentic/state/workflow_dependency_graphs/cohere_fast_ym.json").read_text())
    wf = yaml.safe_load((ROOT / "agentic/registries/cohere_fast_ym_workflow.yaml").read_text())
    assert {(n["id"], n["skill"]) for n in graph["nodes"]} == {(n["id"], n["skill"]) for n in wf["nodes"]}
