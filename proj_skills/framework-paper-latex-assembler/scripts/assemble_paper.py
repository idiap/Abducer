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
"""Assemble approved section packets into deterministic standalone LaTeX."""

from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def digest(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def main()->int:
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--blueprint",required=True,type=Path); ap.add_argument("--sections-dir",required=True,type=Path); ap.add_argument("--output-dir",required=True,type=Path); ap.add_argument("--review",type=Path); ap.add_argument("--figures",type=Path); a=ap.parse_args()
 bp=json.loads(a.blueprint.read_text());
 if a.review and json.loads(a.review.read_text()).get("status")!="pass": raise SystemExit("consistency review has not passed")
 fragments=[]; section_records=[]; bundle_digest=bp.get("input_digest","")
 for item in bp.get("sections",[]):
  sid=item.get("section_id") or item.get("id"); packet=a.sections_dir/f"{sid}.section.json"; tex=a.sections_dir/f"{sid}.tex"
  if not packet.is_file() or not tex.is_file():
   if item.get("required",True): raise SystemExit(f"missing section {sid}")
   continue
  meta=json.loads(packet.read_text());
  if bundle_digest and meta.get("input_digest") not in {None,"",bundle_digest}: raise SystemExit(f"stale section {sid}")
  body=tex.read_text(); fragments.append(body.rstrip())
  if sid=="architecture" and a.figures:
   plan=json.loads(a.figures.read_text()); figure_tex=[]
   for figure in plan.get("figures",[]):
    caption=str(figure.get("caption","Evidence-qualified framework view.")).replace("_",r"\_")
    label=str(figure.get("figure_id","fig:framework")).replace("_","")
    figure_tex.append("\\begin{figure}[ht]\\centering\\fbox{\\parbox{0.82\\linewidth}{\\centering "+str(figure.get("title","Framework view")).replace("_",r"\_")+"}}\\caption{"+caption+"}\\label{"+label+"}\\end{figure}")
   fragments.extend(figure_tex)
  section_records.append({"section_id":sid,"packet_sha256":digest(packet.read_bytes()),"tex_sha256":digest(tex.read_bytes())})
 title=bp.get("title","Evidence-Qualified Framework Description")
 main="\\documentclass[11pt]{article}\n\\usepackage[margin=1in]{geometry}\n\\usepackage{amsmath,amssymb,booktabs,hyperref}\n\\title{"+title.replace("_",r"\_")+"}\n\\author{Anonymous}\n\\date{}\n\\begin{document}\n\\maketitle\n"+"\n\n".join(fragments)+"\n\\end{document}\n"
 a.output_dir.mkdir(parents=True,exist_ok=True); out=a.output_dir/"main.tex"; out.write_text(main)
 manifest={"schema_version":1,"input_digest":bundle_digest,"blueprint_sha256":digest(a.blueprint.read_bytes()),"figures_sha256":digest(a.figures.read_bytes()) if a.figures else None,"sections":section_records,"main_tex_sha256":digest(main.encode()),"promotion_status":"not_promoted"}
 (a.output_dir/"build-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n"); print(out); return 0
if __name__=="__main__": raise SystemExit(main())
