# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Resolve and bundle the Prism dependency closure for generated projects."""

from __future__ import annotations

import hashlib
import json
import platform as host_platform
import re
import shutil
import subprocess
import sys
import tomllib
import zipfile
from dataclasses import asdict, dataclass
from email.parser import Parser
from pathlib import Path
from typing import Iterable


class DependencyError(RuntimeError):
    """The requested portable dependency closure cannot be produced."""


_REQUIREMENT_NAME = re.compile(r"^\s*([A-Za-z0-9_.-]+)")


@dataclass(frozen=True, slots=True)
class Distribution:
    name: str
    version: str
    source: str
    requirements: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BundledArtifact:
    filename: str
    sha256: str
    size: int
    distribution: str
    version: str
    license: str


@dataclass(frozen=True, slots=True)
class DependencyManifest:
    schema_version: int
    python: str
    platform: str
    roots: tuple[str, ...]
    distributions: tuple[Distribution, ...]
    external_requirements: tuple[str, ...]
    artifacts: tuple[BundledArtifact, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def workspace_distributions(prism_source: Path) -> dict[str, Distribution]:
    """Read public workspace distribution metadata without importing Prism."""
    root = prism_source.resolve()
    found: dict[str, Distribution] = {}
    for pattern in ("packages/*/pyproject.toml", "libs/*/pyproject.toml"):
        for path in sorted(root.glob(pattern)):
            payload = tomllib.loads(path.read_text(encoding="utf-8"))
            project = payload.get("project", {})
            name = str(project.get("name", "")).strip()
            if not name:
                continue
            requirements = tuple(str(item) for item in project.get("dependencies", ()))
            if name in found:
                raise DependencyError(f"duplicate workspace distribution: {name}")
            found[name] = Distribution(
                name=name,
                version=str(project.get("version", "0+unknown")),
                source=path.parent.relative_to(root).as_posix(),
                requirements=requirements,
            )
    if "prism-cli" not in found or "prism-language" not in found:
        raise DependencyError(f"not a Prism workspace: {root}")
    return found


def resolve_workspace_closure(
    distributions: dict[str, Distribution], roots: Iterable[str]
) -> tuple[tuple[Distribution, ...], tuple[str, ...]]:
    """Close over workspace requirements and return external requirements."""
    pending = list(dict.fromkeys(roots))
    selected: dict[str, Distribution] = {}
    external: set[str] = set()
    while pending:
        name = pending.pop(0)
        if name in selected:
            continue
        distribution = distributions.get(name)
        if distribution is None:
            raise DependencyError(f"unknown Prism distribution: {name}")
        selected[name] = distribution
        for requirement in distribution.requirements:
            match = _REQUIREMENT_NAME.match(requirement)
            if match is None:
                raise DependencyError(f"cannot parse requirement: {requirement}")
            dependency = match.group(1)
            if dependency in distributions:
                pending.append(dependency)
            else:
                external.add(requirement)
    return (
        tuple(selected[name] for name in sorted(selected)),
        tuple(sorted(external, key=str.lower)),
    )


def required_roots(
    *,
    handler: str = "fake",
    python_adapter: bool = False,
    standard_library: bool = True,
) -> tuple[str, ...]:
    """Return the feature-selected public Prism distribution roots."""
    roots = ["prism-cli"]
    # prism-cli currently declares all adapters, but keep feature roots explicit
    # so a future CLI split remains correctly represented in the lock.
    if handler == "codex":
        roots.append("prism-adapter-codex")
    elif handler == "litellm":
        roots.append("prism-adapter-litellm")
    elif handler != "fake":
        raise DependencyError(f"unsupported Prism handler: {handler}")
    if python_adapter:
        roots.append("prism-adapter-python")
    if standard_library:
        roots.append("prism-stdlib")
    return tuple(dict.fromkeys(roots))


def build_workspace_wheels(
    prism_source: Path,
    distributions: Iterable[Distribution],
    wheel_directory: Path,
    *,
    uv_executable: str = "uv",
) -> None:
    """Build exact first-party wheels through the workspace's public packaging."""
    wheel_directory.mkdir(parents=True, exist_ok=True)
    for distribution in distributions:
        command = [
            uv_executable,
            "build",
            "--wheel",
            "--package",
            distribution.name,
            "--out-dir",
            str(wheel_directory),
        ]
        completed = subprocess.run(
            command,
            cwd=prism_source,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode:
            raise DependencyError(
                f"failed to build {distribution.name}: "
                f"{completed.stderr.strip() or completed.stdout.strip()}"
            )


def build_generated_adapter_wheel(
    project_root: Path,
    wheel_directory: Path,
    *,
    uv_executable: str = "uv",
) -> None:
    """Build the generated leaf adapter package into the portable wheelhouse."""
    package = project_root / "adapters"
    if not (package / "pyproject.toml").is_file():
        raise DependencyError(
            "Python adapters were requested but no adapter package exists"
        )
    if shutil.which(uv_executable):
        command = [
            uv_executable,
            "build",
            "--wheel",
            str(package),
            "--out-dir",
            str(wheel_directory),
        ]
    else:
        command = [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            "--no-deps",
            "--no-build-isolation",
            "--wheel-dir",
            str(wheel_directory),
            str(package),
        ]
    completed = subprocess.run(
        command,
        cwd=project_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise DependencyError(
            "failed to build generated Python adapters: "
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )


def copy_wheelhouse(source: Path, destination: Path) -> None:
    """Copy an explicit third-party wheelhouse; never consult a package index."""
    if not source.is_dir():
        raise DependencyError(f"wheelhouse does not exist: {source}")
    destination.mkdir(parents=True, exist_ok=True)
    wheels = sorted(source.glob("*.whl"))
    if not wheels:
        raise DependencyError(f"wheelhouse contains no wheels: {source}")
    for wheel in wheels:
        shutil.copy2(wheel, destination / wheel.name)


def download_external_wheels(
    requirements: Iterable[str],
    destination: Path,
    *,
    uv_executable: str = "uv",
) -> None:
    """Resolve the third-party closure into wheels for the current target.

    Network resolution is deliberately a separate, explicitly selected operation.
    Generated projects never consult an index during bootstrap or execution.
    """
    selected = tuple(requirements)
    if not selected:
        return
    destination.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [
            uv_executable,
            "run",
            "--isolated",
            "--python",
            sys.executable,
            "--with",
            "pip",
            "python",
            "-m",
            "pip",
            "download",
            "--only-binary=:all:",
            "--dest",
            str(destination),
            *selected,
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise DependencyError(
            "failed to resolve third-party wheels: "
            f"{completed.stderr.strip() or completed.stdout.strip()}"
        )


def _wheel_identity(filename: str) -> tuple[str, str]:
    """Return normalized distribution and version fields from a wheel filename."""
    if not filename.endswith(".whl"):
        raise DependencyError(f"not a wheel: {filename}")
    fields = filename[:-4].split("-")
    if len(fields) < 5 or not fields[0] or not fields[1]:
        raise DependencyError(f"invalid wheel filename: {filename}")
    return fields[0].replace("_", "-"), fields[1]


def artifact_manifest(
    wheel_directory: Path,
    distributions: Iterable[Distribution],
) -> tuple[BundledArtifact, ...]:
    known = {item.name.replace("-", "_").lower(): item.name for item in distributions}
    artifacts: list[BundledArtifact] = []
    for path in sorted(wheel_directory.glob("*.whl")):
        distribution, version = _wheel_identity(path.name)
        normalized = distribution.replace("-", "_").lower()
        artifacts.append(
            BundledArtifact(
                filename=path.name,
                sha256=_sha256(path),
                size=path.stat().st_size,
                distribution=known.get(normalized, distribution),
                version=version,
                license=_wheel_license(path),
            )
        )
    return tuple(artifacts)


def bundle_dependencies(
    *,
    prism_source: Path,
    project_root: Path,
    handler: str = "fake",
    python_adapter: bool = False,
    wheelhouse: Path | None = None,
    build_wheels: bool = True,
    download_external: bool = False,
) -> DependencyManifest:
    """Bundle a feature-driven dependency closure into a generated project."""
    distributions = workspace_distributions(prism_source)
    roots = required_roots(
        handler=handler,
        python_adapter=python_adapter,
        standard_library=True,
    )
    closure, external = resolve_workspace_closure(distributions, roots)
    vendor = project_root / "vendor"
    wheels = vendor / "wheels"
    wheels.mkdir(parents=True, exist_ok=True)
    if build_wheels:
        build_workspace_wheels(prism_source, closure, wheels)
        if python_adapter:
            build_generated_adapter_wheel(project_root, wheels)
    if wheelhouse is not None:
        copy_wheelhouse(wheelhouse, wheels)
    if download_external:
        download_external_wheels(external, wheels)
    artifacts = artifact_manifest(wheels, closure)
    manifest = DependencyManifest(
        schema_version=1,
        python=f"{sys.version_info.major}.{sys.version_info.minor}",
        platform=f"{sys.platform}-{host_platform.machine()}",
        roots=roots,
        distributions=closure,
        external_requirements=external,
        artifacts=artifacts,
    )
    vendor.mkdir(parents=True, exist_ok=True)
    (vendor / "manifest.json").write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_sbom(vendor / "sbom.json", manifest)
    return manifest


def bundle_prebuilt_dependencies(
    *,
    prebuilt_vendor: Path,
    project_root: Path,
    python_adapter: bool = False,
) -> DependencyManifest:
    """Copy a complete bundled Prism toolchain into a generated project."""
    vendor_source = prebuilt_vendor.resolve()
    manifest_path = vendor_source / "manifest.json"
    wheel_source = vendor_source / "wheels"
    if not manifest_path.is_file() or not wheel_source.is_dir():
        raise DependencyError(
            f"prebuilt toolchain requires vendor/manifest.json and vendor/wheels: {vendor_source}"
        )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_python = f"{sys.version_info.major}.{sys.version_info.minor}"
    expected_platform = f"{sys.platform}-{host_platform.machine()}"
    if payload.get("python") != expected_python:
        raise DependencyError(
            f"prebuilt toolchain targets Python {payload.get('python')}, not {expected_python}"
        )
    if payload.get("platform") != expected_platform:
        raise DependencyError(
            f"prebuilt toolchain targets {payload.get('platform')}, not {expected_platform}"
        )
    distributions = tuple(
        Distribution(
            name=str(item["name"]),
            version=str(item["version"]),
            source=str(item["source"]),
            requirements=tuple(str(value) for value in item.get("requirements", [])),
        )
        for item in payload.get("distributions", [])
        if str(item.get("name", "")).replace("_", "-").lower() != "to-prism"
    )
    destination = project_root / "vendor" / "wheels"
    destination.mkdir(parents=True, exist_ok=True)
    for wheel in sorted(wheel_source.glob("*.whl")):
        distribution, _ = _wheel_identity(wheel.name)
        if distribution.replace("-", "_").lower() == "to_prism":
            continue
        shutil.copy2(wheel, destination / wheel.name)
    if python_adapter:
        build_generated_adapter_wheel(project_root, destination)
    manifest = DependencyManifest(
        schema_version=1,
        python=expected_python,
        platform=expected_platform,
        roots=tuple(
            str(item)
            for item in payload.get("roots", [])
            if str(item).replace("_", "-").lower() != "to-prism"
        ),
        distributions=distributions,
        external_requirements=tuple(
            str(item) for item in payload.get("external_requirements", [])
        ),
        artifacts=artifact_manifest(destination, distributions),
    )
    target_vendor = project_root / "vendor"
    (target_vendor / "manifest.json").write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    _write_sbom(target_vendor / "sbom.json", manifest)
    return manifest


def validate_dependency_bundle(
    project_root: Path, *, require_all_external: bool
) -> list[str]:
    """Validate artifact hashes and report unresolved dependency obligations."""
    vendor = project_root / "vendor"
    payload = json.loads((vendor / "manifest.json").read_text(encoding="utf-8"))
    failures: list[str] = []
    filenames = set()
    for artifact in payload.get("artifacts", []):
        filename = str(artifact["filename"])
        filenames.add(filename)
        path = vendor / "wheels" / filename
        if not path.is_file():
            failures.append(f"missing bundled artifact: {filename}")
        elif _sha256(path) != artifact["sha256"]:
            failures.append(f"artifact hash mismatch: {filename}")
    for distribution in payload.get("distributions", []):
        normalized = str(distribution["name"]).replace("-", "_").lower() + "-"
        if not any(name.lower().startswith(normalized) for name in filenames):
            failures.append(f"missing Prism wheel: {distribution['name']}")
    if require_all_external:
        present = {
            str(item.get("distribution", "")).replace("-", "_").lower()
            for item in payload.get("artifacts", [])
        }
        for requirement in payload.get("external_requirements", []):
            match = _REQUIREMENT_NAME.match(str(requirement))
            if match and match.group(1).replace("-", "_").lower() not in present:
                failures.append(f"missing direct third-party wheel: {match.group(1)}")
    return failures


def write_offline_bootstrap(project_root: Path) -> None:
    """Write relocation-safe launchers that never access a package index."""
    bootstrap = """#!/usr/bin/env sh
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
"$PYTHON_BIN" -m venv "$PROJECT_DIR/.venv"
"$PROJECT_DIR/.venv/bin/python" -m pip install --no-index --require-hashes \\
  --find-links "$PROJECT_DIR/vendor/wheels" -r "$PROJECT_DIR/dependency.lock"
"""
    launcher = """#!/usr/bin/env sh
set -eu
PROJECT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$PROJECT_DIR"
exec "$PROJECT_DIR/.venv/bin/prism" "$@"
"""
    for path, text in (
        (project_root / "bootstrap.sh", bootstrap),
        (project_root / "prism", launcher),
    ):
        path.write_text(text, encoding="utf-8")
        path.chmod(0o755)


def write_dependency_lock(project_root: Path, manifest: DependencyManifest) -> None:
    """Write pip's hash-locked offline input from bundled wheel artifacts."""
    grouped: dict[tuple[str, str], list[str]] = {}
    for artifact in manifest.artifacts:
        grouped.setdefault((artifact.distribution, artifact.version), []).append(
            artifact.sha256
        )
    lines: list[str] = []
    for (distribution, version), hashes in sorted(
        grouped.items(), key=lambda item: (item[0][0].lower(), item[0][1])
    ):
        suffix = " ".join(f"--hash=sha256:{digest}" for digest in sorted(hashes))
        lines.append(f"{distribution}=={version} {suffix}")
    (project_root / "dependency.lock").write_text(
        "\n".join(sorted(set(lines), key=str.lower)) + "\n",
        encoding="utf-8",
    )


def _write_sbom(path: Path, manifest: DependencyManifest) -> None:
    licenses = {
        item.distribution: item.license
        for item in manifest.artifacts
        if item.license != "unknown"
    }
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "components": [
            {
                "type": "library",
                "name": item.name,
                "version": item.version,
                "licenses": (
                    [{"license": {"name": licenses[item.name]}}]
                    if item.name in licenses
                    else []
                ),
                "properties": [{"name": "to_prism:source", "value": item.source}],
            }
            for item in manifest.distributions
        ]
        + [
            {
                "type": "library",
                "name": item.distribution,
                "version": item.version,
                "hashes": [{"alg": "SHA-256", "content": item.sha256}],
                "licenses": (
                    [{"license": {"name": item.license}}]
                    if item.license != "unknown"
                    else []
                ),
                "properties": [{"name": "to_prism:artifact", "value": item.filename}],
            }
            for item in manifest.artifacts
            if item.distribution
            not in {distribution.name for distribution in manifest.distributions}
        ],
    }
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _wheel_license(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            metadata_names = [
                name
                for name in archive.namelist()
                if name.endswith(".dist-info/METADATA")
            ]
            if len(metadata_names) != 1:
                return "unknown"
            metadata = Parser().parsestr(
                archive.read(metadata_names[0]).decode("utf-8", errors="replace")
            )
    except (OSError, zipfile.BadZipFile, KeyError):
        return "unknown"
    expression = metadata.get("License-Expression") or metadata.get("License")
    if expression and expression.strip().upper() not in {"UNKNOWN", "NONE"}:
        return expression.strip()
    license_classifiers = [
        item.rsplit("::", 1)[-1].strip()
        for item in metadata.get_all("Classifier", [])
        if item.startswith("License ::")
    ]
    return "; ".join(license_classifiers) or "unknown"


__all__ = [
    "BundledArtifact",
    "DependencyError",
    "DependencyManifest",
    "Distribution",
    "artifact_manifest",
    "build_generated_adapter_wheel",
    "bundle_dependencies",
    "bundle_prebuilt_dependencies",
    "copy_wheelhouse",
    "download_external_wheels",
    "required_roots",
    "resolve_workspace_closure",
    "validate_dependency_bundle",
    "workspace_distributions",
    "write_dependency_lock",
    "write_offline_bootstrap",
]
