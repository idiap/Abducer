# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Rebuild original report sections from a relocated, validated package.

This is a rendering/dependency acceptance check on historical inputs. It never
executes research, requests a model, or treats a rebuilt report as new learning.
The archive reader supplies an isolated temporary workspace for all writes.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def sections(directory):
    """Compare authored section names and interactive tabs, not changing prose."""
    return {
        "markdown": re.findall(r"^## (.+)$", (directory / "latest.md").read_text(), re.M),
        **{name: re.findall(r'<button[^>]+data-tab="([^"]+)"', (directory / name).read_text())
           for name in ("latest.html", "full_timeline.html")},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--lunar-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.lunar_root.resolve() / "app/backend"))
    from domain_packages.archive import ArchiveLimits, validate_archive

    evidence = {"status": "passed", "research_execution_verified": False, "runs": []}
    with tempfile.TemporaryDirectory(prefix="marathon-report-parity-") as raw:
        validated = validate_archive(args.archive.resolve(), Path(raw) / "archive", ArchiveLimits())
        evidence["archive_sha256"] = validated.archive_digest
        source = validated.root / "repository/runtime"
        catalog = json.loads((validated.root / "repository/marathon-binding.json").read_text())
        for run in catalog["runs"]:
            if run.get("initialize") is True:
                continue  # No report exists until this new-run option executes.
            report_dir = source / "agentic/reports/discovery_marathon/targets" / run["target_id"]
            before = sections(report_dir)
            state_path = source / f"agentic/runs/discovery_marathons/{run['run_id']}/run_state.json"
            state_before = state_path.read_bytes()
            for name in ("latest.md", "latest.json", "latest.html", "full_timeline.html"):
                (report_dir / name).unlink()
            command = [sys.executable, "-c",
                "import sys; sys.path.insert(0,'agentic/scripts'); "
                "from run_discovery_marathon import rebuild_reports; rebuild_reports(sys.argv[1],sys.argv[2])",
                run["run_id"], run["target_id"]]
            completed = subprocess.run(command, cwd=source,
                env={**os.environ, "PYTHONPATH": str(source), "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True, text=True, timeout=300)
            if completed.returncode:
                raise RuntimeError(completed.stderr[:3000])
            after = sections(report_dir)
            assert before == after, {"run_id": run["run_id"], "before": before, "after": after}
            assert state_before == state_path.read_bytes(), "Rendering mutated research run state"
            report = json.loads((report_dir / "latest.json").read_text())
            assert all(report[key] == run[key] for key in ("run_id", "target_id", "cycle_count"))
            evidence["runs"].append({"run_id": run["run_id"], "target_id": run["target_id"],
                "cycle_count": run["cycle_count"], "sections": after,
                "files": {name: {"bytes": (report_dir / name).stat().st_size,
                    "sha256": hashlib.sha256((report_dir / name).read_bytes()).hexdigest()}
                    for name in ("latest.md", "latest.json", "latest.html", "full_timeline.html")}})
    args.output.write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
