"""Command-line interface for individual skills and complete runs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from tdr.export import export_candidate
from tdr.orchestration import DiscoveryEngine
from tdr.skills import CATALOG, execute_skill, list_skills
from tdr.validation import adapter_report


def _read_json(path: str | None) -> dict[str, Any]:
    if path in (None, "-"):
        raw = sys.stdin.read()
    else:
        raw = Path(path).read_text(encoding="utf-8")
    value = json.loads(raw or "{}")
    if not isinstance(value, dict):
        raise ValueError("input must be a JSON object")
    return value


def _emit(value: Any, pretty: bool = True) -> None:
    json.dump(value, sys.stdout, indent=2 if pretty else None, sort_keys=pretty, ensure_ascii=False)
    sys.stdout.write("\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tdr", description="Higher abductive theory-discovery reasoner")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("skills", help="List the executable skill catalogue")
    run_skill = sub.add_parser("run-skill", help="Run one skill against a JSON object")
    run_skill.add_argument("name", choices=tuple(CATALOG))
    run_skill.add_argument("--input", "-i", default="-")
    run_skill.add_argument("--pretty", action="store_true")
    run_skill.add_argument("--project")
    run_skill.add_argument("--run")

    init = sub.add_parser("init", help="Initialize a local project")
    init.add_argument("project")
    init.add_argument("--context-id", default="pending-context")

    demo = sub.add_parser("demo", help="Run the built-in tensor-product reconstruction")
    demo.add_argument("--project", required=True)

    ingest = sub.add_parser("ingest", help="Ingest a source as a staged fragment")
    ingest.add_argument("source_path")
    ingest.add_argument("--project", required=True)
    ingest.add_argument("--run", required=True)
    ingest.add_argument("--name")

    for command, skill in (("map", "map-theory-fragment"), ("reflect", "run-philosophical-reflection"), ("generate", "generate-theory-candidates")):
        child = sub.add_parser(command, help=f"Run {skill}")
        child.set_defaults(skill_name=skill)
        child.add_argument("--input", "-i", required=True)
        child.add_argument("--project", required=True)
        child.add_argument("--run", required=True)

    validate = sub.add_parser("validate", help="Run formal, concrete, and adversarial validation")
    validate.add_argument("--input", "-i", required=True)
    validate.add_argument("--project", required=True)
    validate.add_argument("--run", required=True)

    inspect = sub.add_parser("inspect", help="Inspect run state and event trace")
    inspect.add_argument("--project", required=True)
    inspect.add_argument("--run")

    replay = sub.add_parser("replay", help="Deterministically replay and compare a run")
    replay.add_argument("--project", required=True)
    replay.add_argument("--run", required=True)

    export = sub.add_parser("export", help="Export a stored candidate")
    export.add_argument("--project", required=True)
    export.add_argument("--candidate", required=True)
    export.add_argument("--format", choices=("json", "latex", "mmt", "lean"), required=True)
    export.add_argument("--output")

    adapters = sub.add_parser("adapters", help="Report optional formal-tool availability")
    adapters.add_argument("--pretty", action="store_true")

    serve = sub.add_parser("serve", help="Start the local JSON HTTP API")
    serve.add_argument("--project", required=True)
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "skills":
            _emit(list_skills())
        elif args.command == "run-skill":
            payload = _read_json(args.input)
            if args.project and args.run:
                output = DiscoveryEngine(args.project).execute(args.run, args.name, payload)
            else:
                output = execute_skill(args.name, payload)
            _emit(output, args.pretty)
        elif args.command == "init":
            engine = DiscoveryEngine(args.project)
            state = engine.create_run(args.context_id)
            _emit({"project": str(Path(args.project).resolve()), "run_id": state.run_id, "phase": state.phase})
        elif args.command == "demo":
            _emit(DiscoveryEngine(args.project).run_demo())
        elif args.command == "ingest":
            path = Path(args.source_path)
            payload = {"name": args.name or path.stem, "sources": [{"artifact_id": path.name, "locator": str(path), "content": path.read_text(encoding="utf-8")} ]}
            _emit(DiscoveryEngine(args.project).execute(args.run, "map-theory-fragment", payload))
        elif args.command in {"map", "reflect", "generate"}:
            _emit(DiscoveryEngine(args.project).execute(args.run, args.skill_name, _read_json(args.input)))
        elif args.command == "validate":
            engine = DiscoveryEngine(args.project)
            payload = _read_json(args.input)
            outputs = {
                name: engine.execute(args.run, name, payload)
                for name in ("formalize-candidate", "instantiate-concretely", "falsify-candidate")
            }
            _emit(outputs)
        elif args.command == "inspect":
            engine = DiscoveryEngine(args.project)
            if args.run:
                _emit(engine.inspect(args.run))
            else:
                with engine.repository.connection() as db:
                    runs = [dict(row) for row in db.execute("SELECT * FROM runs ORDER BY updated_at DESC").fetchall()]
                _emit({"runs": runs, "records": engine.repository.list_records()})
        elif args.command == "replay":
            _emit(DiscoveryEngine(args.project).replay(args.run))
        elif args.command == "export":
            candidate = DiscoveryEngine(args.project).repository.get_record(args.candidate)
            content = export_candidate(candidate, args.format)
            if args.output:
                Path(args.output).write_text(content, encoding="utf-8")
                _emit({"output": str(Path(args.output).resolve()), "format": args.format})
            else:
                sys.stdout.write(content + ("\n" if not content.endswith("\n") else ""))
        elif args.command == "adapters":
            _emit(adapter_report(), args.pretty)
        elif args.command == "serve":
            from .http import serve
            serve(args.project, args.host, args.port)
        return 0
    except (ValueError, KeyError, OSError, json.JSONDecodeError) as error:
        _emit({"error": type(error).__name__, "message": str(error)})
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

