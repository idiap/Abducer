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
"""Replay every YM21 stage test in a writable sandbox over read-only source.

This harness intentionally records raw pytest outcomes.  Its sole qualification
route is the declared Stage 70 noncanonical-witness drift, which is accepted
only when a fresh exact recomputation differs at one predeclared hash field and
all substantive certificate fields remain identical.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from agentic_common import ROOT, rel, utc_now, write_json
from integrate_ym_representational_dynamics_20260721 import (
    IMPORT_ROOT,
    NORMALIZED_ROOT,
    REPORT_ROOT,
    SNAPSHOT_ROOT,
    TARGET_ID,
    VERSION,
    tree_digest,
)


EXPECTED_QUALIFICATION = (
    ROOT / "agentic/evals/ym_representational_dynamics_20260721/stage70_expected_qualification.json"
)
STAGE_PATTERN = re.compile(r"^\d{2}_.+")


class ReplayError(RuntimeError):
    """Raised when the replay environment or result violates its contract."""


def semantic_diff(left: Any, right: Any, path: str = "") -> list[dict[str, Any]]:
    """Return deterministic JSON-pointer differences between two values."""

    if type(left) is not type(right):
        return [{"path": path or "/", "left": left, "right": right}]
    if isinstance(left, dict):
        rows: list[dict[str, Any]] = []
        for key in sorted(set(left) | set(right)):
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            child = f"{path}/{escaped}"
            if key not in left:
                rows.append({"path": child, "left": "<missing>", "right": right[key]})
            elif key not in right:
                rows.append({"path": child, "left": left[key], "right": "<missing>"})
            else:
                rows.extend(semantic_diff(left[key], right[key], child))
        return rows
    if isinstance(left, list):
        rows = []
        if len(left) != len(right):
            rows.append({"path": f"{path}/length", "left": len(left), "right": len(right)})
        for index, (one, two) in enumerate(zip(left, right)):
            rows.extend(semantic_diff(one, two, f"{path}/{index}"))
        return rows
    return [] if left == right else [{"path": path or "/", "left": left, "right": right}]


def qualification_from_payloads(
    stored: dict[str, Any], fresh: dict[str, Any], expected: dict[str, Any]
) -> dict[str, Any]:
    """Qualify precisely one nonsemantic witness-hash drift, nothing broader."""

    differences = semantic_diff(stored, fresh)
    paths = [row["path"] for row in differences]
    allowed = expected["allowed_semantic_diff_paths"]
    exact_flags = expected["required_exact_flags"]
    flag_failures: list[str] = []
    for certificate_name, certificate in fresh.get("certificates", {}).items():
        for flag in exact_flags:
            if certificate.get(flag) is not True:
                flag_failures.append(f"{certificate_name}:{flag}")
    accepted = paths == allowed and not flag_failures
    return {
        "schema_version": 1,
        "stage": expected["stage"],
        "qualification": expected["qualification"] if accepted else "rejected",
        "accepted": accepted,
        "raw_failure_preserved": True,
        "xfail_used": False,
        "suppression_used": False,
        "difference_count": len(differences),
        "differences": differences,
        "allowed_paths": allowed,
        "exact_flag_failures": flag_failures,
        "interpretation": (
            "The numerical locator selected a different exact KKT witness in an underdetermined witness space; "
            "the stored witness hash is noncanonical, while all stored substantive matrices, spectra, nullities, "
            "polynomial identities, kernel witnesses, and exact verification flags match fresh recomputation."
            if accepted
            else "The observed failure is broader than the declared noncanonical witness-hash drift."
        ),
        "claim_boundary": "C2 exact finite fixed-complex certificate only; no nonlinear boundary law or mass-gap implication",
    }


def _make_writable(root: Path) -> None:
    for path in root.rglob("*"):
        if path.is_dir():
            path.chmod(path.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
        else:
            path.chmod(path.stat().st_mode | stat.S_IWUSR)
    root.chmod(root.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)


def discover_test_stages(snapshot: Path = SNAPSHOT_ROOT) -> dict[str, list[Path]]:
    """Discover all top-level numbered stages containing pytest files."""

    stages: dict[str, list[Path]] = {}
    for stage in sorted(path for path in snapshot.iterdir() if path.is_dir() and STAGE_PATTERN.fullmatch(path.name)):
        tests = sorted(path.relative_to(stage) for path in stage.rglob("test_*.py"))
        if tests:
            stages[stage.name] = tests
    return stages


def _pytest_counts(output: str) -> dict[str, int]:
    counts = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "xpassed": 0, "errors": 0}
    for key in counts:
        matches = re.findall(rf"(\d+)\s+{key}\b", output)
        if matches:
            counts[key] = int(matches[-1])
    return counts


def _qualify_stage70(temp_stage: Path, expected: dict[str, Any]) -> dict[str, Any]:
    sys.path.insert(0, str(temp_stage))
    try:
        import exact_multistar  # type: ignore[import-not-found]

        stored = json.loads(exact_multistar.RESULTS.read_text(encoding="utf-8"))
        fresh = exact_multistar.build_results()
    finally:
        sys.path.remove(str(temp_stage))
        sys.modules.pop("exact_multistar", None)
    return qualification_from_payloads(stored, fresh, expected)


def run_stage(
    stage_name: str,
    tests: list[Path],
    all_stage_roots: list[Path],
    expected_qualification: dict[str, Any],
    *,
    timeout_seconds: int,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    """Run one stage from a private writable copy and capture the raw result."""

    source_stage = SNAPSHOT_ROOT / stage_name
    with tempfile.TemporaryDirectory(prefix=f"ym21-{stage_name[:3]}-") as raw_temp:
        temp_root = Path(raw_temp)
        temp_stage = temp_root / stage_name
        shutil.copytree(source_stage, temp_stage, copy_function=shutil.copy2)
        _make_writable(temp_stage)
        # Preserve the package's sibling-relative addressing without copying or
        # mutating unrelated stages.  Only the stage under test is writable;
        # every other sibling is a symlink into the read-only source snapshot.
        for sibling in SNAPSHOT_ROOT.iterdir():
            if sibling.name == stage_name:
                continue
            (temp_root / sibling.name).symlink_to(sibling, target_is_directory=sibling.is_dir())
        home = temp_root / "home"
        cache = temp_root / "cache"
        home.mkdir()
        cache.mkdir()
        env = os.environ.copy()
        env.update(
            {
                "HOME": str(home),
                "MPLCONFIGDIR": str(cache / "matplotlib"),
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONPYCACHEPREFIX": str(cache / "pycache"),
                "TMPDIR": str(temp_root),
                "PYTHONPATH": os.pathsep.join(
                    [str(temp_stage), *(str(path) for path in all_stage_roots), env.get("PYTHONPATH", "")]
                ).rstrip(os.pathsep),
            }
        )
        # Run each file in its own pytest process.  Publication supplements use
        # the same Python package name (`supplement`) in five sibling papers;
        # one collection process would conflate those distinct packages.
        commands: list[list[str]] = []
        output_sections: list[str] = []
        counts = {"passed": 0, "failed": 0, "skipped": 0, "xfailed": 0, "xpassed": 0, "errors": 0}
        exit_codes: list[int] = []
        timed_out = False
        for index, test_path in enumerate(tests):
            command = [
                sys.executable,
                "-m",
                "pytest",
                "-q",
                "--disable-warnings",
                f"--basetemp={temp_root / f'pytest-{index}'}",
                str(test_path),
            ]
            commands.append(command)
            try:
                completed = subprocess.run(
                    command,
                    cwd=temp_stage,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=False,
                    timeout=timeout_seconds,
                )
                file_output = completed.stdout
                file_exit = completed.returncode
            except subprocess.TimeoutExpired as exc:
                file_output = (exc.stdout or "") + "\nTIMEOUT"
                file_exit = 124
                timed_out = True
            file_counts = _pytest_counts(file_output)
            for key, value in file_counts.items():
                counts[key] += value
            exit_codes.append(file_exit)
            output_sections.append(f"### {test_path.as_posix()}\n{file_output}")
        output = "\n".join(output_sections)
        exit_code = next((code for code in exit_codes if code != 0), 0)
        qualification = None
        if stage_name == expected_qualification["stage"] and exit_code != 0:
            qualification = _qualify_stage70(temp_stage, expected_qualification)
        raw_status = "passed" if exit_code == 0 else "timed_out" if timed_out else "failed"
        row = {
            "stage": stage_name,
            "source_stage": rel(source_stage),
            "test_files": [path.as_posix() for path in tests],
            "test_file_count": len(tests),
            "commands": [["<root-venv-python>", *command[1:]] for command in commands],
            "exit_code": exit_code,
            "raw_status": raw_status,
            "counts": counts,
            "qualification": qualification["qualification"] if qualification else None,
            "effective_status": (
                "qualified_noncanonical_witness_drift"
                if qualification and qualification["accepted"]
                else raw_status
            ),
            "output_tail": "\n".join(output.splitlines()[-80:]),
            "workspace_policy": "read-only source plus isolated writable temporary copy",
        }
        return row, qualification


def replay(selected_stages: list[str] | None = None, *, timeout_seconds: int = 300) -> dict[str, Any]:
    """Run the dynamic stage portfolio and write a source-integrity-bound report."""

    if Path(sys.prefix).resolve() != (ROOT / ".venv").resolve():
        raise ReplayError(f"replay must use the root virtual environment; sys.prefix={sys.prefix}")
    if not SNAPSHOT_ROOT.exists():
        raise ReplayError("run the YM21 integrator before replay")
    manifest = json.loads((IMPORT_ROOT / "immutable_source_manifest.json").read_text(encoding="utf-8"))
    expected_source_digest = manifest["active_snapshot"]["content_digest"]
    source_digest_before = tree_digest(SNAPSHOT_ROOT)
    stages = discover_test_stages()
    all_discovered = list(stages)
    if selected_stages:
        unknown = sorted(set(selected_stages) - set(stages))
        if unknown:
            raise ReplayError(f"unknown or test-free stages: {unknown}")
        stages = {name: stages[name] for name in selected_stages}
    expected = json.loads(EXPECTED_QUALIFICATION.read_text(encoding="utf-8"))
    all_stage_roots = [path for path in SNAPSHOT_ROOT.iterdir() if path.is_dir() and STAGE_PATTERN.fullmatch(path.name)]
    results: list[dict[str, Any]] = []
    stage70_qualification: dict[str, Any] | None = None
    for stage_name, tests in stages.items():
        print(f"replay {stage_name}: {len(tests)} test file(s)", flush=True)
        row, qualification = run_stage(
            stage_name,
            tests,
            all_stage_roots,
            expected,
            timeout_seconds=timeout_seconds,
        )
        results.append(row)
        if qualification:
            stage70_qualification = qualification
        print(f"  -> {row['effective_status']} {row['counts']}", flush=True)
    source_digest_after = tree_digest(SNAPSHOT_ROOT)
    source_unchanged = source_digest_before == source_digest_after
    no_suppression = all(
        row["counts"]["skipped"] == row["counts"]["xfailed"] == row["counts"]["xpassed"] == 0
        for row in results
    )
    acceptable = {"passed", "qualified_noncanonical_witness_drift"}
    all_effective_pass = all(row["effective_status"] in acceptable for row in results)
    complete = not selected_stages and list(stages) == all_discovered
    status = (
        "passed_with_qualified_stage70_drift"
        if complete and all_effective_pass and source_unchanged and no_suppression and stage70_qualification
        else "passed"
        if complete and all_effective_pass and source_unchanged and no_suppression
        else "partial"
        if not complete and all_effective_pass and source_unchanged and no_suppression
        else "failed"
    )
    aggregate = {key: sum(row["counts"][key] for row in results) for key in results[0]["counts"]} if results else {}
    report = {
        "schema_version": 1,
        "generated_utc": utc_now(),
        "target_id": TARGET_ID,
        "source_version": VERSION,
        "status": status,
        "complete_dynamic_discovery": complete,
        "discovered_stage_count": len(all_discovered),
        "executed_stage_count": len(results),
        "discovered_test_file_count": sum(len(tests) for tests in discover_test_stages().values()),
        "executed_test_file_count": sum(row["test_file_count"] for row in results),
        "aggregate_raw_counts": aggregate,
        "root_venv": rel(Path(sys.prefix)),
        "source_root": rel(SNAPSHOT_ROOT),
        "source_manifest_content_digest": expected_source_digest,
        "source_tree_digest_before": source_digest_before,
        "source_tree_digest_after": source_digest_after,
        "source_unchanged": source_unchanged,
        "source_read_only": all(not (path.stat().st_mode & 0o222) for path in SNAPSHOT_ROOT.rglob("*") if path.is_file()),
        "temporary_workspaces": True,
        "suppression_policy": {"xfail_used": False, "skip_injected": False, "failures_suppressed": False},
        "no_observed_skip_or_xfail": no_suppression,
        "stage70_qualification": stage70_qualification,
        "stages": results,
        "epistemic_boundary": "Executable finite/restricted replay only; no continuum Yang--Mills or mass-gap certification.",
    }
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    write_json(REPORT_ROOT / "replay_report.json", report)
    (REPORT_ROOT / "replay_report.md").write_text(
        "\n".join(
            [
                "# YM 2026-07-21 stage-isolated replay",
                "",
                f"- Status: `{status}`",
                f"- Stages: `{len(results)}/{len(all_discovered)}`",
                f"- Test files: `{report['executed_test_file_count']}/{report['discovered_test_file_count']}`",
                f"- Raw counts: `{aggregate}`",
                f"- Source unchanged: `{source_unchanged}`",
                f"- Skip/xfail observed: `{not no_suppression}`",
                "- Stage 70 raw failure remains visible; only the exact one-field noncanonical witness-hash drift is qualified.",
                "- Boundary: passing finite/restricted tests do not prove continuum Yang--Mills or the mass gap.",
                "",
            ]
            + [
                f"- `{row['stage']}`: `{row['effective_status']}`; raw `{row['raw_status']}`; `{row['counts']}`"
                for row in results
            ]
            + [""]
        ),
        encoding="utf-8",
    )
    if stage70_qualification:
        stage70_qualification = {
            **stage70_qualification,
            "generated_utc": report["generated_utc"],
            "source_stage": rel(SNAPSHOT_ROOT / expected["stage"]),
            "raw_test_result": {
                "passed": next(row for row in results if row["stage"] == expected["stage"])["counts"]["passed"],
                "failed": next(row for row in results if row["stage"] == expected["stage"])["counts"]["failed"],
            },
        }
        write_json(NORMALIZED_ROOT / "stage70_qualification.json", stage70_qualification)
    print(json.dumps({"status": status, "aggregate_raw_counts": aggregate}, indent=2, sort_keys=True))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="append", dest="stages")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        report = replay(args.stages, timeout_seconds=args.timeout_seconds)
    except (ReplayError, OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0 if report["status"] in {"passed", "passed_with_qualified_stage70_drift", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
