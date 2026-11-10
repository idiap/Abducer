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
"""Materialize one request-bound causal JSON artifact for the dispatcher."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping


CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from agentic.discovery.contracts import (  # noqa: E402
    ContractError,
    canonical_digest,
    canonical_json,
    fsync_directory,
    resolve_workspace_path,
)


OPERATOR_ID = "canonical-causal-artifact-producer"
OPERATOR_VERSION = "1.0.0"
OPERATOR_KIND = "support_probe"


def _read_request() -> dict[str, Any]:
    try:
        value = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ContractError(f"stdin is not a causal producer request: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("causal producer request must be an object")
    return value


def _read_existing(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = -1
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ContractError("causal output collision is not one regular single-link file")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks)
    except OSError as exc:
        raise ContractError("causal output collision cannot be reopened safely") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def _write_create_only(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path, follow_symlinks=False)
        except FileExistsError:
            if _read_existing(path) != data:
                raise ContractError("immutable causal output conflicts with an existing value")
        fsync_directory(path.parent)
    finally:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass


def run(request: Mapping[str, Any], *, workspace: Path) -> dict[str, Any]:
    operator = request.get("operator", {})
    if operator != {
        "operator_id": OPERATOR_ID,
        "version": OPERATOR_VERSION,
        "kind": OPERATOR_KIND,
    }:
        raise ContractError("request does not name the exact causal artifact producer")
    if request.get("input_artifacts") != []:
        raise ContractError("causal artifact producer accepts no ambient input artifacts")
    outputs = request.get("declared_outputs")
    if not isinstance(outputs, list) or len(outputs) != 1:
        raise ContractError("causal artifact producer requires one declared output")
    parameters = request.get("parameters")
    if not isinstance(parameters, Mapping):
        raise ContractError("causal artifact producer parameters must be an object")
    artifact = parameters.get("artifact_value")
    if not isinstance(artifact, Mapping):
        raise ContractError("causal artifact producer requires one JSON-object artifact")
    value = dict(artifact)
    if parameters.get("artifact_digest") != canonical_digest(value):
        raise ContractError("causal artifact value differs from its request digest")
    output_path = resolve_workspace_path(workspace, str(outputs[0]))
    _write_create_only(output_path, canonical_json(value))
    return {"artifacts": [{"path": str(outputs[0])}], "explicit_unknowns": []}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        protocol = run(_read_request(), workspace=arguments.workspace.resolve())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 2
    json.dump(protocol, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
