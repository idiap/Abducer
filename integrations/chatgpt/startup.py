# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Eager loading and honest readiness for the canonical hosted research library.

Only known library modules are imported. Scientific skill scripts remain cached
source bytes: importing arbitrary workflow code could start research at setup.
Installation belongs to setup_runtime or the container build, not an HTTP call.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import platform
import sys
import tomllib
from collections import deque
from pathlib import Path

from packaging.markers import Marker, default_environment
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.utils import canonicalize_name

MODULES = {
    "jsonschema": "jsonschema",
    "markdown-it-py": "markdown_it",
    "numpy": "numpy",
    "pyyaml": "yaml",
    "rich": "rich",
    "scipy": "scipy",
    "sympy": "sympy",
    "mcp": "mcp",
    "packaging": "packaging",
    "pyjwt": "jwt",
    "pypdf": "pypdf",
    "uvicorn": "uvicorn",
}


def _receipt_path() -> Path:
    return Path(sys.prefix) / "abducer-setup.json"


def _audit_receipt(lock_digest, project_digest, installed, python):
    """Check an installer receipt against this interpreter, never trust its count.

    Developers may run a lock-compatible environment without the bootstrap. A
    present receipt, however, must describe the current lock and complete actual
    distribution inventory; old receipts cannot certify a replaced environment.
    """
    path = _receipt_path()
    if not path.exists():
        return {"status": "absent", "required": False}
    try:
        receipt = json.loads(path.read_text())
        recorded = {
            canonicalize_name(row["name"]): row["version"]
            for row in receipt["installed_distributions"]
        }
        if (
            receipt.get("schema_version") != 2
            or receipt.get("status") != "installed"
            or receipt.get("lock_sha256") != lock_digest
            or receipt.get("pyproject_sha256") != project_digest
            or receipt.get("groups") != ["project", "chatgpt"]
            or receipt.get("python_version") != python["version"]
            or receipt.get("python_implementation") != python["implementation"]
            or receipt.get("python_requires") != python["requires"]
            or receipt.get("isolated") is not True
            or not python["isolated"]
            or recorded != installed
            or len(recorded) != len(receipt["installed_distributions"])
        ):
            raise ValueError("Installation receipt differs from this environment")
    except (OSError, ValueError, KeyError, TypeError):
        return {"status": "stale", "required": False}
    return {"status": "verified", "required": False, "packages": len(recorded)}


def preload_packages(root: Path) -> dict:
    """Audit the active dependency closure and import reviewed direct libraries.

    Installed Requires-Dist metadata supplies transitive constraints and extras;
    PEP 508 markers select only dependencies relevant to this interpreter. The
    source lock also constrains versions and its platform resolution partitions.
    This checks availability without importing arbitrary transitive/skill code.
    """
    project_bytes = (root / "pyproject.toml").read_bytes()
    lock_bytes = (root / "uv.lock").read_bytes()
    project = tomllib.loads(project_bytes.decode())
    lock = tomllib.loads(lock_bytes.decode())
    marker_environment = default_environment()
    python = {
        "version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "requires": project["project"]["requires-python"],
        "isolated": sys.prefix != sys.base_prefix,
    }
    python["supported"] = SpecifierSet(python["requires"]).contains(python["version"])
    versions = {}
    for package in lock["package"]:
        markers = package.get("resolution-markers", [])
        if not markers or any(
            Marker(value).evaluate(marker_environment) for value in markers
        ):
            versions.setdefault(canonicalize_name(package["name"]), set()).add(
                package["version"]
            )
    requirements = (
        project["project"]["dependencies"] + project["dependency-groups"]["chatgpt"]
    )
    direct = [Requirement(raw) for raw in requirements]
    direct = [
        r for r in direct if r.marker is None or r.marker.evaluate(marker_environment)
    ]
    packages, issues = [], []

    def issue(name, reason):
        row = {"dependency": name, "reason": reason}
        if row not in issues:
            issues.append(row)

    if not python["supported"]:
        issue("python", "UnsupportedPythonVersion")
    pending = deque(direct)
    checked, requested_extras, expanded = {}, {}, {}
    while pending:
        requirement = pending.popleft()
        name = canonicalize_name(requirement.name)
        try:
            version = importlib.metadata.version(requirement.name)
            if version not in versions.get(name, set()):
                raise ValueError(
                    "Installed version is absent from this platform's source lock"
                )
            if requirement.url or not requirement.specifier.contains(version):
                raise ValueError(
                    "Installed version does not satisfy the dependency requirement"
                )
            distribution = importlib.metadata.distribution(requirement.name)
            requires_python = distribution.metadata.get("Requires-Python")
            if requires_python and not SpecifierSet(requires_python).contains(
                python["version"]
            ):
                raise ValueError("Dependency does not support this Python version")
            checked[name] = version
            extras = requested_extras.setdefault(name, set())
            extras.update(requirement.extras)
            signature = frozenset(extras)
            if expanded.get(name) == signature:
                continue
            expanded[name] = signature
            for raw in distribution.requires or []:
                child = Requirement(raw)
                if child.marker is None or any(
                    child.marker.evaluate({**marker_environment, "extra": extra})
                    for extra in extras | {""}
                ):
                    pending.append(child)
        except (ImportError, ValueError, OSError) as error:
            issue(requirement.name, type(error).__name__)

    for requirement in direct:
        name = canonicalize_name(requirement.name)
        if name not in checked:
            continue
        try:
            module = MODULES.get(name)
            if not module:
                raise ValueError("No reviewed startup import for this dependency")
            importlib.import_module(module)
            packages.append(
                {"name": requirement.name, "version": checked[name], "module": module}
            )
        except (ImportError, ValueError, OSError) as error:
            issue(requirement.name, type(error).__name__)
    closure_verified = not issues
    installed = {
        canonicalize_name(distribution.metadata["Name"]): distribution.version
        for distribution in importlib.metadata.distributions()
        if distribution.metadata.get("Name")
    }
    lock_digest = hashlib.sha256(lock_bytes).hexdigest()
    receipt = _audit_receipt(
        lock_digest, hashlib.sha256(project_bytes).hexdigest(), installed, python
    )
    if receipt["status"] == "stale":
        issue("installation-receipt", "StaleInstallationReceipt")
    return {
        "status": "ready" if not issues else "blocked",
        "packages": packages,
        "issues": issues,
        "lock_sha256": lock_digest,
        "installation": (
            "locked-runtime-setup"
            if receipt["status"] == "verified"
            else "environment-audit"
        ),
        "loaded": len(packages),
        "complete_closure_verified": closure_verified,
        "verified_count": len(checked),
        "installed_count": len(installed),
        "runtime_packages": [
            {"name": name, "version": checked[name]} for name in sorted(checked)
        ],
        "python": python,
        "receipt": receipt,
    }


def preload(registry) -> dict:
    """Fill all source caches before serving, retaining every unresolved reference."""
    packages = preload_packages(registry.root)
    workflows, issues = [], []
    for row in registry.catalog.native.rows:
        manifest = registry.dependency_manifest(row["id"])
        workflows.append(
            {
                "workflow_id": row["id"],
                "files": len(manifest["entries"]),
                "complete": manifest["declared_sources_complete"],
                "manifest_sha256": manifest["manifest_sha256"],
            }
        )
        issues.extend(
            {"workflow_id": row["id"], **issue} for issue in manifest["issues"]
        )
    return {
        "schema_version": "abducer.startup/v1",
        "release": registry.catalog.release,
        "status": (
            "ready"
            if packages["status"] == "ready" and not issues
            else "needs-attention"
        ),
        "loaded_at": "service-startup",
        "packages": packages,
        "skills": len(registry.catalog.skills),
        "workflows": len(workflows),
        "graphs": len(registry.catalog.viewers),
        "source_files": len(registry._asset_catalog().assets),
        "workflow_dependencies": workflows,
        "issues": issues,
        "scientific_execution_started": False,
        "all_workflows_executable": False,
    }
