# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Exercise the exported initialization and report path in Lunar's real worker.

HTTP/model callbacks supply explicitly controlled test content. Source operators,
canonical CAS, scheduler, branch validators and report builders remain untouched.
This establishes integration behavior, never a live scientific research result.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from uuid import uuid4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--lunar-root", type=Path, required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--positive", action="store_true")
    args = parser.parse_args()
    repository = Path(__file__).resolve().parents[2]
    sys.path[:0] = [str(repository), str(repository / "agentic/scripts")]
    from tests.discovery.test_bootstrap_pipeline import ControlledModel
    from tests.discovery.test_bootstrap_literature import Channel
    from run_discovery_marathon import build_branch_output, attach_negative_tactic_decision
    sys.path.insert(0, str(args.lunar_root.resolve() / "app/backend"))
    from domain_packages.archive import validate_archive, ArchiveLimits
    from domain_packages.worker.transport import invoke_worker
    from domain_packages.worker.sandbox import WorkerLimits
    args.workspace.mkdir(parents=True, exist_ok=False)
    archive = validate_archive(args.archive.resolve(), args.workspace / "archive", ArchiveLimits())
    output = args.workspace / "output"
    output.mkdir()
    model, channel, branch_calls = ControlledModel(positive=args.positive), Channel(), []
    def model_handler(arguments):
        if len(arguments["messages"]) > 1:
            return model(**arguments)
        prompt = arguments["messages"][0]["content"]
        matches = [json.loads(path.read_text()) for path in (output / "workspace/agentic/runs/discovery_marathons").glob("lunar-marathon-*/branches/*.json")
                   if json.loads(path.read_text())["branch_id"] in prompt]
        if len(matches) != 1:
            raise ValueError("Controlled branch response cannot identify its exact request")
        branch = matches[0]
        branch_calls.append(branch["branch_id"])
        packet = attach_negative_tactic_decision(build_branch_output(branch, 1), branch)
        return {"choices": [{"message": {"content": json.dumps(packet)}}]}
    request = {"contract_version": 1, "request_id": str(uuid4()), "operation": "execute",
        "workflow_id": "discovery_marathon_loop", "hook_id": None,
        "input": {"mode": "live", "inputs": {"target_id": "p-vs-np-target", "run_id": "new"}},
        "authority": {"network": True, "model_access": True}}
    image = subprocess.check_output(["docker", "image", "inspect", args.image, "--format", "{{.Id}}"], text=True).strip()
    result = invoke_worker(image=image, package_root=archive.root, run_root=output,
        manifest=archive.manifest, request=request, model_handler=model_handler,
        fetch_handler=lambda values: channel(**values), model_snapshot={"provider": "controlled", "model_id": "controlled-test-model"},
        on_event=lambda event: print(json.dumps(event), flush=True), limits=WorkerLimits(timeout_seconds=900))
    (args.workspace / "worker-result.json").write_text(json.dumps(result, indent=2))
    assert result["status"] == "succeeded", result["error"]
    structured = result["result"]["structured_value"]
    assert structured["cycle_count"] == int(args.positive)
    assert structured["execution_outcome"] == ("research_cycle_completed" if args.positive else "initialization_requires_revision")
    assert len(model.calls) == 13 and len(channel.urls) == 6
    assert bool(branch_calls) is args.positive
    original = archive.root / "repository/runtime/agentic/reports/discovery_marathon/targets/p-vs-np-target"
    sections = {}
    for name in ("latest.md", "latest.html", "full_timeline.html"):
        pattern = r"^## (.+)$" if name.endswith(".md") else r'<button[^>]+data-tab="([^\"]+)"'
        sections[name] = re.findall(pattern, (output / name).read_text(), re.M)
        assert sections[name] == re.findall(pattern, (original / name).read_text(), re.M)
        if not args.positive:
            assert "no research branch investment is authorized" in (output / name).read_text()
    evidence = {"status": "passed", "controlled_external_capabilities": True, "live_research_verified": False,
        "archive_sha256": archive.archive_digest, "image": image, "initialization_calls": len(model.calls),
        "branch_calls": len(branch_calls), "public_queries": len(channel.urls), "sections": sections,
        "result": structured}
    (args.workspace / "verification.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
