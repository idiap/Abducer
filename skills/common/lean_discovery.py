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

"""Lean/Lake bridge for bounded discovery search."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from discovery_calculus import BridgeShape
from discovery_calculus import RouteSignature
from discovery_calculus import assess_symbolic_search_readiness
from discovery_calculus import build_candidates_for_shapes


_TOOLCHAIN_TEXT = "leanprover/lean4:v4.28.0\n"

_LAKEFILE_TEXT = """name = "AbducerFormal"
version = "0.1.0"
defaultTargets = ["AbducerFormal"]

[[lean_lib]]
name = "AbducerFormal"
"""

_ROOT_MODULE_TEXT = """import AbducerFormal.Discovery.Basic
import AbducerFormal.Discovery.Search
"""

_BASIC_MODULE_TEXT = """namespace AbducerFormal.Discovery

inductive BridgeShape where
  | realization
  | transport
  | equivalence
  | factorization
  | obstruction
  deriving Repr, DecidableEq, Inhabited

def BridgeShape.render : BridgeShape -> String
  | .realization => "realization"
  | .transport => "transport"
  | .equivalence => "equivalence"
  | .factorization => "factorization"
  | .obstruction => "obstruction"

structure RouteSig where
  sourceStatementId : String
  targetStatementId : String
  sourceRegime : String
  targetRegime : String
  invariant : String
  candidateObject : String
  branchFamily : String := ""
  sourceExcerpt : String := ""
  targetExcerpt : String := ""
  multipleOperationalizations : Bool := false
  equivalencePressure : Bool := false
  factorizationPressure : Bool := false
  negativePressure : Bool := false
  underTypedCarrier : Bool := false
  barrierScope : String := ""
  deriving Repr, Inhabited

structure SearchReadiness where
  mode : String
  score : Nat
  blockers : List String
  reasons : List String
  deriving Repr, Inhabited

def hasText (text : String) : Bool :=
  !(text.trimAscii.isEmpty)

end AbducerFormal.Discovery
"""

_SEARCH_MODULE_TEXT = """import AbducerFormal.Discovery.Basic

namespace AbducerFormal.Discovery

def readinessScore (route : RouteSig) : Nat :=
  let base :=
    (if hasText route.sourceStatementId then 1 else 0) +
    (if hasText route.targetStatementId then 1 else 0) +
    (if hasText route.sourceRegime then 1 else 0) +
    (if hasText route.targetRegime then 1 else 0) +
    (if hasText route.invariant then 1 else 0) +
    (if hasText route.candidateObject && !route.underTypedCarrier then 1 else 0) +
    (if hasText route.sourceExcerpt then 1 else 0) +
    (if hasText route.targetExcerpt then 1 else 0) +
    (if hasText route.branchFamily then 1 else 0)
  base +
    (if route.multipleOperationalizations || route.equivalencePressure then 1 else 0) +
    (if route.factorizationPressure then 1 else 0) +
    (if route.negativePressure then 1 else 0)

def assessReadiness (route : RouteSig) : SearchReadiness :=
  let blockers :=
    (if hasText route.sourceStatementId then [] else ["missing source statement id"]) ++
    (if hasText route.targetStatementId then [] else ["missing target statement id"]) ++
    (if hasText route.sourceRegime then [] else ["missing source regime"]) ++
    (if hasText route.targetRegime then [] else ["missing target regime"]) ++
    (if hasText route.invariant then [] else ["missing preserved invariant"]) ++
    (if hasText route.candidateObject && !route.underTypedCarrier then [] else ["candidate object is missing or still under-typed"])
  let reasons :=
    (if hasText route.invariant then ["the preserved invariant is named"] else []) ++
    (if hasText route.candidateObject && !route.underTypedCarrier then ["the bridge carrier is named and not marked under-typed"] else []) ++
    (if route.multipleOperationalizations || route.equivalencePressure then ["the route is explicitly equivalence- or coherence-facing"] else []) ++
    (if route.factorizationPressure then ["the route is diagrammatic enough for factorization search"] else []) ++
    (if route.negativePressure then ["negative pressure is explicit, so bounded obstruction search is meaningful"] else [])
  let score := readinessScore route
  if !blockers.isEmpty then
    if score >= 6 then
      {
        mode := "hybrid-llm-plus-symbolic"
        score := score
        blockers := blockers
        reasons := reasons ++ ["the route is partially typed but still needs LLM mediation on missing fields"]
      }
    else
      {
        mode := "llm-first"
        score := score
        blockers := blockers
        reasons := reasons ++ ["the route is still too schematic for bounded symbolic search"]
      }
  else
    {
      mode := "symbolic-search-ready"
      score := score
      blockers := []
      reasons := reasons ++ ["the route is typed enough for bounded search over bridge shapes"]
    }

def appendUnique (items : List BridgeShape) (shape : BridgeShape) : List BridgeShape :=
  if shape ∈ items then items else items ++ [shape]

def searchShapes (route : RouteSig) : List BridgeShape :=
  let shapes0 := [BridgeShape.realization]
  let shapes1 := if route.sourceRegime != route.targetRegime then appendUnique shapes0 BridgeShape.transport else shapes0
  let shapes2 := if route.multipleOperationalizations || route.equivalencePressure then appendUnique shapes1 BridgeShape.equivalence else shapes1
  let shapes3 := if route.factorizationPressure then appendUnique shapes2 BridgeShape.factorization else shapes2
  let shapes4 := if route.negativePressure || route.underTypedCarrier || hasText route.barrierScope then appendUnique shapes3 BridgeShape.obstruction else shapes3
  shapes4

def renderShapes (shapes : List BridgeShape) : String :=
  String.intercalate "," (shapes.map BridgeShape.render)

end AbducerFormal.Discovery
"""


def _clean_text(value: Any) -> str:
    return " ".join(str(value or "").strip().split())


def _shell_safe_excerpt(text: str, *, limit: int = 800) -> str:
    value = _clean_text(text)
    if len(value) <= limit:
        return value
    return value[: limit - 3].rstrip() + "..."


def _upper_camel(value: Any, *, default: str) -> str:
    tokens = re.findall(r"[A-Za-z0-9]+", _clean_text(value))
    if not tokens:
        return default
    return "".join(token[:1].upper() + token[1:] for token in tokens)


def _escape_lean_string(value: Any) -> str:
    text = str(value or "")
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    return text.replace("\r", " ").replace("\n", " ")


def _bool_literal(value: Any) -> str:
    return "true" if bool(value) else "false"


def _path_candidates(binary: str) -> list[Path]:
    home = Path.home()
    suffix = ".exe" if os.name == "nt" else ""
    candidates = [Path(home / ".elan" / "bin" / f"{binary}{suffix}")]
    if os.name == "nt":
        candidates.append(Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links" / f"{binary}.exe")
    return [path for path in candidates if str(path)]


def _resolve_binary(binary: str) -> str:
    found = shutil.which(binary)
    if found:
        return found
    for path in _path_candidates(binary):
        if path.exists():
            return str(path)
    return ""


def _lean_env() -> dict[str, str]:
    env = dict(os.environ)
    prepend: list[str] = []
    elan_bin = Path.home() / ".elan" / "bin"
    if elan_bin.exists():
        prepend.append(str(elan_bin))
    winget_links = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Links"
    if winget_links.exists():
        prepend.append(str(winget_links))
    if prepend:
        env["PATH"] = os.pathsep.join(prepend + [env.get("PATH", "")])
    return env


def ensure_lake_package(repo_root: Path) -> dict[str, Any]:
    """Bootstrap the minimal Lean/Lake project if the target repo root lacks one."""

    repo_root = repo_root.resolve()
    created: list[str] = []
    wanted = {
        repo_root / "lean-toolchain": _TOOLCHAIN_TEXT,
        repo_root / "lakefile.toml": _LAKEFILE_TEXT,
        repo_root / "AbducerFormal.lean": _ROOT_MODULE_TEXT,
        repo_root / "AbducerFormal" / "Discovery" / "Basic.lean": _BASIC_MODULE_TEXT,
        repo_root / "AbducerFormal" / "Discovery" / "Search.lean": _SEARCH_MODULE_TEXT,
    }
    for path, content in wanted.items():
        if path.exists():
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(str(path))
    return {
        "package_root": str(repo_root),
        "created_files": created,
        "created": bool(created),
    }


def _generated_module_info(*, kb_ref: str, execution_id: str) -> tuple[str, str]:
    namespace = _upper_camel(kb_ref, default="Demo")
    module_leaf = _upper_camel(execution_id, default="DiscoverySearch")
    module_name = f"AbducerFormal.Generated.{namespace}.{module_leaf}"
    relative = Path("AbducerFormal") / "Generated" / namespace / f"{module_leaf}.lean"
    return module_name, str(relative)


def _route_definition(route_name: str, route: RouteSignature) -> str:
    return "\n".join(
        [
            f"def {route_name} : RouteSig :=",
            "  {",
            f'    sourceStatementId := "{_escape_lean_string(route.source_statement_id)}"',
            f'    targetStatementId := "{_escape_lean_string(route.target_statement_id)}"',
            f'    sourceRegime := "{_escape_lean_string(route.source_regime)}"',
            f'    targetRegime := "{_escape_lean_string(route.target_regime)}"',
            f'    invariant := "{_escape_lean_string(route.invariant)}"',
            f'    candidateObject := "{_escape_lean_string(route.candidate_object)}"',
            f'    branchFamily := "{_escape_lean_string(route.branch_family)}"',
            f'    sourceExcerpt := "{_escape_lean_string(route.source_excerpt)}"',
            f'    targetExcerpt := "{_escape_lean_string(route.target_excerpt)}"',
            f"    multipleOperationalizations := {_bool_literal(route.multiple_operationalizations)}",
            f"    equivalencePressure := {_bool_literal(route.equivalence_pressure)}",
            f"    factorizationPressure := {_bool_literal(route.factorization_pressure)}",
            f"    negativePressure := {_bool_literal(route.negative_pressure)}",
            f"    underTypedCarrier := {_bool_literal(route.under_typed_carrier)}",
            f'    barrierScope := "{_escape_lean_string(route.barrier_scope)}"',
            "  }",
        ]
    )


def write_generated_search_module(
    repo_root: Path,
    *,
    kb_ref: str,
    execution_id: str,
    routes: list[dict[str, Any]],
) -> dict[str, Any]:
    """Write the per-branch Lean module that evaluates search shapes for typed routes."""

    ensure_lake_package(repo_root)
    module_name, relative_path = _generated_module_info(kb_ref=kb_ref, execution_id=execution_id)
    module_path = (repo_root / relative_path).resolve()
    namespace = module_name
    body: list[str] = [
        "import AbducerFormal.Discovery.Search",
        "",
        "open AbducerFormal.Discovery",
        "",
        f"namespace {namespace}",
        "",
    ]
    for idx, row in enumerate(routes, start=1):
        route_name = f"route{idx}"
        body.extend(
            [
                _route_definition(route_name, row["route"]),
                "",
                f'#eval s!"READINESS|{row["queue_id"]}|{{readinessScore {route_name}}}"',
                f'#eval s!"SHAPES|{row["queue_id"]}|{{renderShapes (searchShapes {route_name})}}"',
                "",
            ]
        )
    body.extend([f"end {namespace}", ""])
    module_path.parent.mkdir(parents=True, exist_ok=True)
    module_path.write_text("\n".join(body), encoding="utf-8")
    return {
        "module_name": module_name,
        "module_path": str(module_path),
        "relative_path": relative_path,
    }


def _parse_shape_names(text: str) -> list[BridgeShape]:
    mapping = {shape.value: shape for shape in BridgeShape}
    rows: list[BridgeShape] = []
    for token in [part.strip().lower() for part in str(text or "").split(",")]:
        shape = mapping.get(token)
        if shape is not None and shape not in rows:
            rows.append(shape)
    return rows


def run_lean_search(
    repo_root: Path,
    *,
    kb_ref: str,
    execution_id: str,
    routes: list[dict[str, Any]],
    max_candidates_per_route: int = 5,
) -> dict[str, Any]:
    """Run the Lean/Lake bounded search for one branch and return theorem packets plus diagnostics."""

    bootstrap = ensure_lake_package(repo_root)
    lake = _resolve_binary("lake")
    if not lake:
        return {
            "engine": "lean-via-lake",
            "available": False,
            "bootstrap": bootstrap,
            "reason": "lake executable is not available in PATH or the standard elan locations.",
            "routes": [],
            "candidates": [],
        }

    module_info = write_generated_search_module(
        repo_root,
        kb_ref=kb_ref,
        execution_id=execution_id,
        routes=routes,
    )
    build = subprocess.run(
        [lake, "build", "AbducerFormal"],
        cwd=str(repo_root),
        env=_lean_env(),
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )
    completed = subprocess.run(
        [lake, "env", "lean", module_info["relative_path"]],
        cwd=str(repo_root),
        env=_lean_env(),
        capture_output=True,
        text=True,
        timeout=240,
        check=False,
    )

    readiness_by_queue: dict[str, int] = {}
    shapes_by_queue: dict[str, list[BridgeShape]] = {}
    stdout = completed.stdout or ""
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if len(line) >= 2 and line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        if line.startswith("READINESS|"):
            _, queue_id, score = (line.split("|", 2) + ["", ""])[:3]
            try:
                readiness_by_queue[_clean_text(queue_id)] = int(score)
            except ValueError:
                pass
        elif line.startswith("SHAPES|"):
            _, queue_id, payload = (line.split("|", 2) + ["", ""])[:3]
            shapes_by_queue[_clean_text(queue_id)] = _parse_shape_names(payload)

    route_rows: list[dict[str, Any]] = []
    candidate_rows: list[dict[str, Any]] = []
    for row in routes:
        queue_id = _clean_text(row.get("queue_id"))
        route = row["route"]
        readiness = assess_symbolic_search_readiness(route)
        shapes = shapes_by_queue.get(queue_id, [])
        candidates = build_candidates_for_shapes(route, shapes, max_candidates=max_candidates_per_route)
        route_rows.append(
            {
                "queue_id": queue_id,
                "bridge_id": _clean_text(row.get("bridge_id")),
                "readiness": readiness.to_dict(),
                "lean_readiness_score": readiness_by_queue.get(queue_id, readiness.score),
                "search_shapes": [shape.value for shape in shapes],
                "candidate_count": len(candidates),
            }
        )
        for candidate in candidates:
            candidate_rows.append(
                {
                    "queue_id": queue_id,
                    "bridge_id": _clean_text(row.get("bridge_id")),
                    "candidate": candidate.to_dict(),
                }
            )

    return {
        "engine": "lean-via-lake",
        "available": True,
        "bootstrap": bootstrap,
        "module_name": module_info["module_name"],
        "module_path": module_info["module_path"],
        "relative_path": module_info["relative_path"],
        "build_ok": build.returncode == 0 and completed.returncode == 0,
        "package_build_ok": build.returncode == 0,
        "returncode": completed.returncode,
        "stdout_excerpt": _shell_safe_excerpt("\n".join(part for part in [build.stdout or "", stdout] if part.strip())),
        "stderr_excerpt": _shell_safe_excerpt("\n".join(part for part in [build.stderr or "", completed.stderr or ""] if part.strip())),
        "routes": route_rows,
        "candidates": candidate_rows,
    }
