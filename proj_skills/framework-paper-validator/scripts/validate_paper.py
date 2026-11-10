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
"""Validate structural and epistemic integrity of a framework-paper bundle."""

from __future__ import annotations
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path

BAD=[re.compile(r"/Users/|/home/"),re.compile(r"TODO|TBD|FIXME"),re.compile(r"\\write18|shell-escape",re.I),re.compile(r"(?:api[_-]?key|secret)\s*[:=]",re.I)]
def main()->int:
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--bundle",required=True,type=Path); ap.add_argument("--output",type=Path); a=ap.parse_args(); errors=[]
 tex=a.bundle/"main.tex"; manifest=a.bundle/"build-manifest.json"
 if not tex.is_file(): errors.append("missing main.tex")
 if not manifest.is_file(): errors.append("missing build-manifest.json")
 text=tex.read_text() if tex.is_file() else ""
 if text.count("\\begin{document}")!=1 or text.count("\\end{document}")!=1: errors.append("document wrapper must occur exactly once")
 for pattern in BAD:
  if pattern.search(text): errors.append(f"forbidden content: {pattern.pattern}")
 if "\\section{Limitations" not in text and "\\section{Limitations and" not in text: errors.append("missing limitations section")
 if "\\section{Evaluation" not in text and "\\section{Current Evidence Status" not in text: errors.append("missing evaluation/evidence-status section")
 if manifest.is_file() and tex.is_file():
  recorded=json.loads(manifest.read_text()).get("main_tex_sha256")
  actual=hashlib.sha256(tex.read_bytes()).hexdigest()
  if recorded != actual: errors.append("main.tex digest does not match build manifest")
 compile_status="not_run_due_to_structural_errors" if errors else "not_available"
 compile_log=""
 latexmk=shutil.which("latexmk")
 if not errors and latexmk:
  result=subprocess.run([latexmk,"-pdf","-interaction=nonstopmode","-halt-on-error","main.tex"],cwd=a.bundle,text=True,capture_output=True,check=False)
  compile_log=(result.stdout+result.stderr)[-4000:]
  compile_status="pass" if result.returncode==0 and (a.bundle/"main.pdf").is_file() else "fail"
  if compile_status=="fail": errors.append("LaTeX compilation failed")
 report={"schema_version":1,"status":"fail" if errors else "pass","errors":errors,"compile_status":compile_status,"compile_log_tail":compile_log}
 target=a.output or a.bundle/"validation.json"; target.write_text(json.dumps(report,indent=2)+"\n"); print(target); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
