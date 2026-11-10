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
"""Adjudicate claim authorization and cross-section paper consistency."""

from __future__ import annotations
import argparse,json,re
from pathlib import Path

STRONG=re.compile(r"\b(novel|first|state[- ]of[- ]the[- ]art|effective|outperform|proves?|demonstrates?)\b",re.I)
def main()->int:
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--claim-ledger",required=True,type=Path); ap.add_argument("--blueprint",required=True,type=Path); ap.add_argument("--sections-dir",required=True,type=Path); ap.add_argument("--output",required=True,type=Path); a=ap.parse_args()
 ledger=json.loads(a.claim_ledger.read_text()); bp=json.loads(a.blueprint.read_text()); claims={c.get("claim_id") or c.get("id"):c for c in ledger.get("claims",[])}; allocations={x.get("section_id") or x.get("id"):set(x.get("allowed_claim_ids",[])) for x in bp.get("sections",[])}; findings=[]; seen=set(); bodies={}
 for p in sorted(a.sections_dir.glob("*.section.json")):
  s=json.loads(p.read_text()); sid=s.get("section_id",p.stem); seen.add(sid)
  for cid in s.get("consumed_claim_ids",s.get("claim_ids",[])):
   c=claims.get(cid)
   if not c: findings.append({"severity":"error","code":"unknown_claim","section_id":sid,"claim_id":cid})
   elif cid not in allocations.get(sid,set()): findings.append({"severity":"error","code":"claim_not_allocated","section_id":sid,"claim_id":cid})
   elif c.get("allowed_sections") and sid not in c["allowed_sections"]: findings.append({"severity":"error","code":"claim_not_allowed","section_id":sid,"claim_id":cid})
  fragment=a.sections_dir/str(s.get("tex_fragment",f"{sid}.tex"))
  text=fragment.read_text() if fragment.is_file() else str(s.get("latex",s.get("body","")))
  body=re.sub(r"\\(?:section|begin)\{[^}]+\}|\\end\{[^}]+\}","",text).strip(); bodies[sid]=re.sub(r"\s+"," ",body)
  if "This section records the evidence-qualified" in text: findings.append({"severity":"error","code":"placeholder_section_prose","section_id":sid})
  if STRONG.search(text) and not any((claims.get(cid) or {}).get("claim_class") in {"novelty","comparative","evaluative"} for cid in s.get("consumed_claim_ids",[])):
   findings.append({"severity":"error","code":"unlicensed_strong_language","section_id":sid})
 required=[x.get("section_id") or x.get("id") for x in bp.get("sections",[]) if x.get("required",True)]
 for sid in required:
  if sid not in seen: findings.append({"severity":"error","code":"missing_section","section_id":sid})
 duplicates={body for body in bodies.values() if body and list(bodies.values()).count(body)>1}
 for body in sorted(duplicates): findings.append({"severity":"error","code":"duplicate_section_body","section_ids":sorted(sid for sid,value in bodies.items() if value==body)})
 out={"schema_version":1,"status":"fail" if any(f["severity"]=="error" for f in findings) else "pass","findings":findings,"sections_seen":sorted(seen)}
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2)+"\n"); print(a.output); return 0 if out["status"]=="pass" else 1
if __name__=="__main__": raise SystemExit(main())
