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

"""Run deterministic hook contract fixtures."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

from agentic_common import ROOT, fail, load_json_object, rel


def _run_fixtures(trace_directory: str) -> int:
    fixtures = sorted((ROOT / "agentic" / "evals" / "hook_contract").glob("*.json"))
    if not fixtures:
        fail("no hook fixtures found")
    for fixture in fixtures:
        row = load_json_object(fixture)
        script = ROOT / row["script"]
        if not script.exists():
            fail(f"{rel(fixture)} script missing: {row['script']}")
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                # Native hook bytes are pinned by compatibility tests. Keep
                # their real policy/context, redirecting only disposable traces.
                "import runpy,sys; from pathlib import Path; "
                "script=Path(sys.argv[1]); "
                "sys.path.insert(0,str(script.parent)); import hook_utils; "
                "hook_utils.TRACE_DIR=Path(sys.argv[2]); "
                "runpy.run_path(str(script),run_name='__main__')",
                str(script),
                trace_directory,
            ],
            input=json.dumps(row.get("payload", {})),
            capture_output=True,
            text=True,
            cwd=ROOT,
            check=False,
            env={**os.environ, "ABDUCER_DISABLE_HOOK_TRACE": "1"},
        )
        if result.returncode != 0:
            fail(f"{rel(fixture)} hook exited {result.returncode}: {result.stderr}")
        try:
            payload = json.loads(result.stdout.strip().splitlines()[-1])
        except Exception as exc:
            fail(f"{rel(fixture)} hook did not emit JSON: {exc}; stdout={result.stdout}")
        if payload.get("decision") != row.get("expected_decision"):
            fail(f"{rel(fixture)} expected {row.get('expected_decision')} got {payload.get('decision')}")
    print(f"validated {len(fixtures)} hook contract fixtures")
    return 0


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="abducer-hook-contract-") as traces:
        return _run_fixtures(traces)


if __name__ == "__main__":
    raise SystemExit(main())
