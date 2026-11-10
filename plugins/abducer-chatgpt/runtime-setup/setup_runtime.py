# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Install the complete locked hosted runtime in an operator-owned environment.

This stdlib-only bootstrap is also exported with the plugin. Installation happens
on the Abducer host, never as a shell command inferred from research content.
Repeated setup audits the same lock and preserves the scientific source tree.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tomllib

_OWNER = "abducer-runtime-setup-v1\n"


def _clean_environment(base=None) -> dict[str, str]:
    """Keep operator credentials, but discard inherited Python/venv targeting."""
    result = dict(os.environ if base is None else base)
    for key in list(result):
        if key.startswith("PYTHON") or key in {
            "VIRTUAL_ENV",
            "CONDA_PREFIX",
            "CONDA_DEFAULT_ENV",
            "UV_PYTHON",
            "UV_PROJECT",
            "UV_PROJECT_ENVIRONMENT",
            "UV_WORKING_DIR",
            "UV_CONFIG_FILE",
            "UV_SYSTEM_PYTHON",
            "UV_BREAK_SYSTEM_PACKAGES",
            "UV_NO_VERIFY_HASHES",
            "UV_NO_GROUP",
            "UV_NO_DEFAULT_GROUPS",
            "UV_FROZEN",
            "UV_CONSTRAINT",
            "UV_BUILD_CONSTRAINT",
            "UV_TARGET",
            "UV_PREFIX",
            "PIP_TARGET",
            "PIP_PREFIX",
            "PIP_USER",
        }:
            result.pop(key, None)
    result.update(
        PYTHONNOUSERSITE="1", PYTHONDONTWRITEBYTECODE="1", PYTHONUNBUFFERED="1"
    )
    return result


def launch_environment(
    environment: Path, source: Path, code: Path, base=None
) -> dict[str, str]:
    """Make direct and PATH-based child Python invocations use the same venv."""
    result = _clean_environment(base)
    scripts = environment / ("Scripts" if sys.platform == "win32" else "bin")
    result.update(
        VIRTUAL_ENV=str(environment),
        PATH=os.pathsep.join([str(scripts), result.get("PATH") or os.defpath]),
        PYTHON=str(scripts / ("python.exe" if sys.platform == "win32" else "python")),
        ABDUCER_REPOSITORY_ROOT=str(source),
        PYTHONPATH=os.pathsep.join(dict.fromkeys([str(code), str(source)])),
    )
    return result


def _destination(environment: Path, roots: tuple[Path, ...]) -> Path:
    """Never install into the source, including through parent-directory aliases."""
    if environment.is_symlink():
        raise ValueError("Use an environment outside the plugin/source directory")
    environment = environment.resolve()
    if any(environment.is_relative_to(root.resolve()) for root in roots):
        raise ValueError("Use an environment outside the plugin/source directory")
    return environment


@contextlib.contextmanager
def _setup_lock(environment: Path):
    """Serialize bridge/worker installers without a stale-directory lock on crashes."""
    environment.parent.mkdir(parents=True, exist_ok=True)
    lock_path = environment.parent / ("." + environment.name + ".abducer-setup.lock")
    flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(lock_path, flags, 0o600)
    with os.fdopen(descriptor, "r+b") as stream:
        if sys.platform == "win32":
            import msvcrt

            stream.write(b"0")
            stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


def _owned_environment(environment: Path) -> None:
    """An ownership marker is insufficient if the target is not a real venv."""
    if not environment.exists():
        return
    marker = environment / ".abducer-environment"
    if marker.is_symlink() or not marker.is_file() or marker.read_text() != _OWNER:
        raise ValueError(
            "Refusing to replace an environment not created by Abducer setup"
        )
    config = environment / "pyvenv.cfg"
    if not config.is_file():
        raise ValueError("Existing Abducer environment is not a virtual environment")
    values = dict(
        line.lower().strip().split("=", 1)
        for line in config.read_text().splitlines()
        if "=" in line
    )
    if any(
        k.strip() == "include-system-site-packages" and v.strip() != "false"
        for k, v in values.items()
    ):
        raise ValueError("Abducer environment must exclude system site packages")


def _python_matches(version: tuple[int, ...], requirement: str) -> bool:
    """Check numeric release specifiers without installing a bootstrap dependency.

    Abducer declares stable Python releases. Unsupported prerelease/arbitrary
    equality syntax fails explicitly instead of silently ignoring a new bound.
    """
    compatible = True
    for clause in requirement.split(","):
        match = re.fullmatch(
            r"\s*(~=|>=|<=|==|!=|>|<)\s*(\d+(?:\.\d+)*)(\.\*)?\s*", clause
        )
        if not match:
            raise ValueError("Unsupported requires-python constraint: " + requirement)
        operator, numeric, wildcard = match.groups()
        target = tuple(map(int, numeric.split(".")))
        length = max(len(version), len(target))
        actual, wanted = version + (0,) * (length - len(version)), target + (0,) * (
            length - len(target)
        )
        if wildcard:
            if operator not in {"==", "!="}:
                raise ValueError("Unsupported requires-python wildcard")
            equal = version[: len(target)] == target
            accepted = equal if operator == "==" else not equal
        elif operator == "~=":
            if len(target) < 2:
                raise ValueError(
                    "Compatible Python bound needs a major and minor version"
                )
            upper = target[:-2] + (target[-2] + 1,)
            accepted = actual >= wanted and version < upper
        else:
            accepted = {
                ">=": actual >= wanted,
                "<=": actual <= wanted,
                ">": actual > wanted,
                "<": actual < wanted,
                "==": actual == wanted,
                "!=": actual != wanted,
            }[operator]
        compatible = compatible and accepted
    return compatible


def _inspect_python(
    python: Path, environment: Path, requirement: str, env: dict
) -> dict:
    """Probe the target interpreter in isolation before mutating its packages."""
    script = (
        "import importlib.metadata as m,json,platform,sys; "
        "print(json.dumps({'prefix':sys.prefix,'base_prefix':sys.base_prefix,"
        "'version':list(sys.version_info[:3]),'implementation':platform.python_implementation(),"
        "'distributions':sorted([{'name':d.metadata['Name'],'version':d.version} "
        "for d in m.distributions()],key=lambda d:d['name'].lower())}))"
    )
    info = json.loads(
        subprocess.check_output(
            [str(python), "-I", "-c", script],
            text=True,
            env=env,
        )
    )
    if (
        Path(info["prefix"]).resolve() != environment
        or info["prefix"] == info["base_prefix"]
    ):
        raise ValueError(
            "Target Python does not belong to the dedicated virtual environment"
        )
    if not _python_matches(tuple(info["version"]), requirement):
        raise ValueError(
            "Target Python does not satisfy requires-python " + requirement
        )
    return info


def _write_receipt(environment: Path, value: dict) -> None:
    """Readers see a complete receipt or a non-ready state during synchronization."""
    path = environment / "abducer-setup.json"
    with tempfile.NamedTemporaryFile(
        mode="w", dir=environment, prefix=".abducer-receipt-", delete=False
    ) as stream:
        temporary = Path(stream.name)
        try:
            stream.write(json.dumps(value, indent=2) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        except BaseException:
            temporary.unlink(missing_ok=True)
            raise
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def install(requirements_root: Path, environment: Path) -> dict:
    """Sync the source lock in an isolated, serialized, operator-owned venv."""
    root = requirements_root.resolve(strict=True)
    environment = _destination(environment, (root,))
    uv = shutil.which("uv")
    if not uv:
        raise ValueError("Install uv on the Abducer host before running runtime setup")
    inputs = {
        name: (root / name).read_bytes() for name in ("pyproject.toml", "uv.lock")
    }
    requirement = tomllib.loads(inputs["pyproject.toml"].decode())["project"][
        "requires-python"
    ]
    # Parse all clauses before any environment mutation, including future bounds.
    _python_matches(tuple(sys.version_info[:3]), requirement)
    lock_digest = hashlib.sha256(inputs["uv.lock"]).hexdigest()
    python = environment / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    marker = environment / ".abducer-environment"
    env = _clean_environment()
    with _setup_lock(environment):
        _owned_environment(environment)
        with tempfile.TemporaryDirectory(prefix="abducer-dependencies-") as name:
            staged = Path(name)
            for filename, content in inputs.items():
                (staged / filename).write_bytes(content)
            requirements = staged / "requirements.txt"
            subprocess.run(
                [
                    uv,
                    "export",
                    "--project",
                    str(staged),
                    "--locked",
                    "--no-dev",
                    "--group",
                    "chatgpt",
                    "--no-emit-project",
                    "--output-file",
                    str(requirements),
                    "--no-config",
                ],
                check=True,
                stdout=subprocess.DEVNULL,
                env=env,
            )
            if not environment.exists():
                selected_python = (
                    sys.executable
                    if _python_matches(tuple(sys.version_info[:3]), requirement)
                    else requirement
                )
                subprocess.run(
                    [
                        uv,
                        "venv",
                        "--python",
                        selected_python,
                        "--no-project",
                        "--no-config",
                        str(environment),
                    ],
                    check=True,
                    env=env,
                )
                marker.write_text(_OWNER)
            _owned_environment(environment)
            _inspect_python(python, environment, requirement, env)
            receipt = {
                "schema_version": 2,
                "status": "installing",
                "lock_sha256": lock_digest,
                "pyproject_sha256": hashlib.sha256(
                    inputs["pyproject.toml"]
                ).hexdigest(),
                "groups": ["project", "chatgpt"],
                "environment": str(environment),
                "python": str(python),
                "scientific_execution_started": False,
            }
            _write_receipt(environment, receipt)
            try:
                subprocess.run(
                    [
                        uv,
                        "pip",
                        "sync",
                        "--python",
                        str(python),
                        "--require-hashes",
                        str(requirements),
                        "--no-config",
                    ],
                    check=True,
                    env=env,
                )
                subprocess.run(
                    [uv, "pip", "check", "--python", str(python), "--no-config"],
                    check=True,
                    env=env,
                )
                info = _inspect_python(python, environment, requirement, env)
                receipt.update(
                    status="installed",
                    python_requires=requirement,
                    isolated=True,
                    python_version=".".join(map(str, info["version"])),
                    python_implementation=info["implementation"],
                    installed_packages=[d["name"] for d in info["distributions"]],
                    installed_distributions=info["distributions"],
                )
                _write_receipt(environment, receipt)
            except BaseException as error:
                _write_receipt(
                    environment,
                    {**receipt, "status": "failed", "error_type": type(error).__name__},
                )
                raise
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    adjacent = Path(__file__).resolve().parent
    default_root = adjacent if (adjacent / "uv.lock").is_file() else adjacent.parents[1]
    parser.add_argument("--requirements-root", type=Path, default=default_root)
    parser.add_argument(
        "--environment",
        type=Path,
        required=True,
        help="Dedicated writable environment outside the source/plugin directory",
    )
    parser.add_argument("--launch", choices=["server", "bridge", "worker"])
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Canonical Abducer source snapshot for execution",
    )
    parser.add_argument(
        "--code-root", type=Path, help="Optional separately released integration code"
    )
    parser.add_argument(
        "arguments",
        nargs=argparse.REMAINDER,
        help="Arguments after -- are passed to the selected service",
    )
    args = parser.parse_args()
    if args.arguments and not args.launch:
        parser.error("Service arguments require --launch")
    source = (args.source_root or args.requirements_root).resolve(strict=True)
    code = (args.code_root or source).resolve(strict=True)
    if (
        args.launch
        and not (code / "integrations/chatgpt" / (args.launch + ".py")).is_file()
    ):
        parser.error("--launch requires an installed Abducer source/code release")
    if args.launch:
        for name in ("pyproject.toml", "uv.lock"):
            if (source / name).read_bytes() != (
                args.requirements_root / name
            ).read_bytes():
                parser.error("Source and setup requirements differ: " + name)
        _destination(args.environment, (args.requirements_root, source, code))
    receipt = install(args.requirements_root, args.environment)
    print(json.dumps(receipt), flush=True)
    if args.launch:
        arguments = (
            args.arguments[1:] if args.arguments[:1] == ["--"] else args.arguments
        )
        command = [receipt["python"], "-m", "integrations.chatgpt." + args.launch]
        if args.launch == "server":
            command.append("serve")
        command.extend(arguments)
        environment = launch_environment(Path(receipt["environment"]), source, code)
        os.chdir(code)
        os.execve(receipt["python"], command, environment)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
