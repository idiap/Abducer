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
def test_children_are_acyclic_typed_and_release_is_gated():
    d=json.loads((ROOT/"agentic/registries/cohere_fast_subworkflows.yaml").read_text())
    rows={r["id"]:r for r in d["subworkflows"]}; orders=[r["order"] for r in rows.values()]
    assert orders == sorted(orders) and len(orders)==len(set(orders))
    assert all(r["input_type"] and r["return_type"] for r in rows.values())
    assert rows["manuscript-release"]["when"] == "audit_status == accepted"
    assert all(a in rows and b in rows and rows[a]["order"] < rows[b]["order"] for a,b in d["edges"])
