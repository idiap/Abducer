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
"""Run the independent interpretive timeline-paper workflow."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from agentic_common import ROOT, rel


BUILD_VALIDATE_STAGES = [
    ("agentic/scripts/build_timeline_paper_interpretation.py", "agentic/scripts/validate_timeline_paper_interpretation.py"),
    ("agentic/scripts/build_timeline_paper_blueprint.py", "agentic/scripts/validate_timeline_paper_blueprint.py"),
    ("agentic/scripts/build_timeline_formal_derivation.py", "agentic/scripts/validate_timeline_formal_derivation.py"),
    ("agentic/scripts/build_timeline_paper_diagrams.py", "agentic/scripts/validate_timeline_paper_diagrams.py"),
    ("agentic/scripts/build_timeline_paper_sections.py", "agentic/scripts/validate_timeline_paper_sections.py"),
    ("agentic/scripts/build_timeline_latex_sections.py", "agentic/scripts/validate_timeline_latex_sections.py"),
    ("agentic/scripts/build_timeline_paper.py", "agentic/scripts/validate_timeline_paper.py"),
    ("agentic/scripts/archive_timeline_paper_project.py", "agentic/scripts/validate_paper_project_archive.py"),
]


def run(cmd: list[str]) -> None:
    print("==>", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="agentic/reports/discovery_marathon/full_timeline.html", help="Timeline HTML source report.")
    parser.add_argument("--target-id", default="", help="Optional target id; currently recorded by source artifacts.")
    parser.add_argument("--output-dir", default="agentic/reports/timeline_paper", help="Paper output directory; current builder writes the standard latest artifacts.")
    parser.add_argument("--strict", action="store_true", help="Run the forward-eval check after paper validation.")
    args = parser.parse_args()
    source = str(Path(args.source))
    for build, validate in BUILD_VALIDATE_STAGES:
        if build.endswith("build_timeline_paper_interpretation.py"):
            run([sys.executable, build, "--source", source])
        else:
            run([sys.executable, build])
        run([sys.executable, validate])
    if args.strict:
        run([sys.executable, "agentic/scripts/validate_timeline_paper_forward_eval.py"])
    print(f"timeline paper workflow complete from {source}; paper at {rel(ROOT / args.output_dir / 'latest.pdf')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
