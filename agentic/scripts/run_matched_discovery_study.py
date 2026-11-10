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
"""Execute and persist a publication-disabled matched discovery study.

The CLI is intentionally an internal evaluation surface.  A successful exit
means that the immutable worker receipts and matched-study report replay; it
does not mean that any condition is creatively, conceptually, or physically
superior.  ``--require-complete`` optionally turns a valid partial-failure
report into a nonzero operational exit without discarding the report.
``--validate-existing`` reopens an immutable report and all transitive receipts
against the current checkout without executing workers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from agentic.discovery.matched_studies import (
    MatchedStudyIntegrityError,
    load_matched_discovery_study_report,
    run_matched_discovery_study,
    write_matched_discovery_study_report,
)


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FIXTURE = (
    ROOT / "tests/fixtures/matched_discovery_studies/independent_task_clusters.json"
)


def _fault_plan(rows: list[str]) -> dict[str, str]:
    plan: dict[str, str] = {}
    for row in rows:
        if "=" not in row:
            raise argparse.ArgumentTypeError("--fault must be KEY=MODE")
        key, mode = row.split("=", 1)
        key = key.strip()
        mode = mode.strip()
        if not key or mode not in {"exit_nonzero", "invalid_json", "hang"}:
            raise argparse.ArgumentTypeError(
                "--fault mode must be exit_nonzero, invalid_json, or hang"
            )
        if key in plan:
            raise argparse.ArgumentTypeError("--fault keys must be unique")
        plan[key] = mode
    return plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument(
        "--validate-existing",
        type=Path,
        metavar="REPORT",
        help=(
            "Reopen a content-addressed report and its receipt chain against "
            "the current checkout instead of executing a new study."
        ),
    )
    parser.add_argument("--repetitions", type=int)
    parser.add_argument("--study-id")
    parser.add_argument("--max-workers", type=int, default=4)
    parser.add_argument("--require-kernel-isolation", action="store_true")
    parser.add_argument(
        "--fault",
        action="append",
        default=[],
        metavar="KEY=MODE",
        help="Inject one deterministic worker fault; repeat for multiple stages.",
    )
    parser.add_argument("--require-complete", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.validate_existing is not None:
            execution_options_present = (
                args.run_root is not None
                or args.run_id is not None
                or args.repetitions is not None
                or args.study_id is not None
                or bool(args.fault)
                or args.require_kernel_isolation
                or args.max_workers != 4
                or args.fixture != DEFAULT_FIXTURE
            )
            if execution_options_present:
                raise MatchedStudyIntegrityError(
                    "--validate-existing cannot be combined with execution options"
                )
            report_path = args.validate_existing.resolve(strict=True)
            report = load_matched_discovery_study_report(report_path)
        else:
            if args.run_root is None or not args.run_id:
                raise MatchedStudyIntegrityError(
                    "new study execution requires --run-root and --run-id"
                )
            faults = _fault_plan(args.fault)
            report = run_matched_discovery_study(
                fixture_path=args.fixture,
                run_root=args.run_root,
                run_id=args.run_id,
                repetitions=args.repetitions,
                study_id=args.study_id,
                max_workers=args.max_workers,
                require_kernel_isolation=args.require_kernel_isolation,
                fault_plan=faults,
            )
            report_path = write_matched_discovery_study_report(report)
    except (argparse.ArgumentTypeError, MatchedStudyIntegrityError, OSError, ValueError) as exc:
        json.dump(
            {
                "status": "matched_study_failed",
                "error_type": type(exc).__name__,
                "message": str(exc),
            },
            sys.stderr,
            sort_keys=True,
        )
        sys.stderr.write("\n")
        return 2

    cells = [cell for family in report["families"] for cell in family["cells"]]
    summary = {
        "status": report["status"],
        "study_id": report["study_id"],
        "report_path": str(report_path),
        "family_count": len(report["families"]),
        "condition_count": sum(len(family["conditions"]) for family in report["families"]),
        "scheduled_cell_count": len(cells),
        "complete_cell_count": sum(cell["complete"] for cell in cells),
        "attempted_stage_receipt_count": sum(cell["attempted_stage_count"] for cell in cells),
        "matched_complete_repetitions": {
            family["family_id"]: family["matched_complete_repetitions"]
            for family in report["families"]
        },
        "publication_authorized": False,
        "advantage_inference_authorized": False,
    }
    json.dump(summary, sys.stdout, sort_keys=True)
    sys.stdout.write("\n")
    if args.require_complete and report["status"] != "protocol_complete_internal_calibration_only":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
