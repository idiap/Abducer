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
ROOT=Path(__file__).resolve().parents[2]
def test_parent_is_domain_bound_and_has_no_second_control_plane():
    w=json.loads((ROOT/"agentic/registries/cohere_fast_workflow_contracts.yaml").read_text())["workflow"]
    assert w["activation"] == "explicit_only" and w["domain_binding_required"]
    assert w["canonical_authority"] == "abducer"
    assert "source runtime authority" in w["prohibitions"]
    assert w["children"][-2:] == ["independent-audit", "manuscript-release"]
