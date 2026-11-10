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
"""Create deterministic evidence-qualified figure plans from paper models."""

from __future__ import annotations
import argparse, json
from pathlib import Path

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--workflow-model",required=True,type=Path); ap.add_argument("--framework-model",required=True,type=Path); ap.add_argument("--output",required=True,type=Path); args=ap.parse_args()
    workflow=json.loads(args.workflow_model.read_text()); framework=json.loads(args.framework_model.read_text())
    nodes=workflow.get("nodes", workflow.get("stages", [])); edges=workflow.get("edges", [])
    claims=sorted({str(c) for obj in [*nodes,*edges] if isinstance(obj,dict) for c in obj.get("claim_ids",[])})
    figures=[{"figure_id":"fig:framework-workflow","kind":"workflow_topology","title":"Evidence-qualified framework workflow","claim_ids":claims,"node_count":len(nodes),"edge_count":len(edges),"caption":"Declared and evidence-qualified workflow structure; topology alone does not establish runtime execution.","status":"planned"}]
    if framework.get("abstractions") or framework.get("constructs"):
        figures.append({"figure_id":"fig:framework-abstraction","kind":"abstraction_map","title":"Framework abstraction and concrete traceability","claim_ids":[],"caption":"Paper abstractions mapped back to concrete framework evidence.","status":"planned"})
    payload={"schema_version":1,"input_digest":workflow.get("input_digest") or framework.get("input_digest",""),"figures":figures}
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(payload,indent=2)+"\n"); print(args.output); return 0
if __name__=="__main__": raise SystemExit(main())
