# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Real isolated setup and failure gates, without network or research work."""

import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import sys

import pytest

from integrations.chatgpt import setup_runtime as setup

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def requirements(tmp_path):
    """A valid empty runtime lock exercises uv without installing test fixtures."""
    uv = shutil.which("uv")
    if not uv:
        pytest.skip("The operator bootstrap requires uv")
    root = tmp_path / "source"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        '[project]\nname="abducer-setup-fixture"\nversion="0.0.0"\n'
        'requires-python=">=3.11"\ndependencies=[]\n'
        "[dependency-groups]\nchatgpt=[]\n"
    )
    subprocess.run(
        [uv, "lock", "--project", str(root), "--offline", "--no-config"],
        check=True,
        capture_output=True,
        env=setup._clean_environment(),
    )
    return root


def test_real_setup_and_path_children_ignore_ambient_python(
    requirements, tmp_path, monkeypatch
):
    destination = tmp_path / "runtime"
    before = (requirements / "uv.lock").read_bytes()
    monkeypatch.setenv("PYTHONHOME", "/nonexistent/foreign-python")
    monkeypatch.setenv("PYTHONPATH", "/untrusted/imports")
    monkeypatch.setenv("VIRTUAL_ENV", "/foreign/environment")
    monkeypatch.setenv("UV_NO_VERIFY_HASHES", "true")
    monkeypatch.setenv("UV_NO_GROUP", "chatgpt")
    first = setup.install(requirements, destination)
    again = setup.install(requirements, destination)
    assert first == again
    assert first["status"] == "installed" and first["schema_version"] == 2
    assert first["isolated"] and first["python_requires"] == ">=3.11"
    assert first["installed_packages"] == []
    assert first["installed_distributions"] == []
    assert (requirements / "uv.lock").read_bytes() == before
    assert json.loads((destination / "abducer-setup.json").read_text()) == first
    environment = setup.launch_environment(destination, requirements, ROOT)
    assert environment["VIRTUAL_ENV"] == str(destination)
    assert environment["PYTHON"] == first["python"]
    assert "PYTHONHOME" not in environment
    assert "UV_NO_VERIFY_HASHES" not in environment
    assert "UV_NO_GROUP" not in environment
    assert environment["PYTHONPATH"] == os.pathsep.join([str(ROOT), str(requirements)])
    # PATH-based launch is what native tools and shell hooks frequently use.
    actual = json.loads(
        subprocess.check_output(
            [
                "python",
                "-c",
                "import sys,site,json; print(json.dumps([sys.prefix,site.ENABLE_USER_SITE]))",
            ],
            env=environment,
            text=True,
            cwd=tmp_path,
        )
    )
    assert actual == [str(destination), False]


def test_failed_sync_replaces_prior_success_receipt(
    requirements, tmp_path, monkeypatch
):
    destination = tmp_path / "runtime"
    setup.install(requirements, destination)
    run = subprocess.run

    def fail_sync(command, **kwargs):
        if command[1:3] == ["pip", "sync"]:
            current = json.loads((destination / "abducer-setup.json").read_text())
            assert current["status"] == "installing"
            raise subprocess.CalledProcessError(1, command)
        return run(command, **kwargs)

    monkeypatch.setattr(setup.subprocess, "run", fail_sync)
    with pytest.raises(subprocess.CalledProcessError):
        setup.install(requirements, destination)
    receipt = json.loads((destination / "abducer-setup.json").read_text())
    assert receipt["status"] == "failed"
    assert receipt["error_type"] == "CalledProcessError"
    assert "installed_distributions" not in receipt
    assert not list(destination.glob(".abducer-receipt-*"))


def test_existing_environment_rejects_borrowed_interpreter_and_system_packages(
    requirements, tmp_path
):
    destination = tmp_path / "runtime"
    destination.mkdir()
    (destination / ".abducer-environment").write_text(setup._OWNER)
    (destination / "pyvenv.cfg").write_text("include-system-site-packages = true\n")
    with pytest.raises(ValueError, match="system site"):
        setup.install(requirements, destination)
    (destination / "pyvenv.cfg").write_text("include-system-site-packages = false\n")
    # The presence of a marker cannot turn a system interpreter into a venv.
    python = destination / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    python.parent.mkdir()
    python.symlink_to(sys.executable)
    with pytest.raises(ValueError, match="dedicated virtual environment"):
        setup._inspect_python(
            Path(sys.executable), destination, ">=3.11", setup._clean_environment()
        )


@pytest.mark.parametrize(
    "version,requirement,accepted",
    [
        ((3, 10, 12), ">=3.11", False),
        ((3, 13, 1), ">=3.11,<3.14", True),
        ((3, 14, 0), ">=3.11,<3.14", False),
        ((3, 13, 1), "~=3.12", True),
        ((3, 13, 1), "~=3.12.0", False),
        ((3, 13, 1), "==3.13.*", True),
        ((3, 13, 1), "!=3.13.*", False),
    ],
)
def test_python_requires_bounds(version, requirement, accepted):
    assert setup._python_matches(version, requirement) is accepted


def test_python_requires_never_silently_ignores_unsupported_bounds():
    with pytest.raises(ValueError, match="Unsupported"):
        setup._python_matches((3, 10, 0), ">=3.11,===3.12")


def test_launch_rejects_different_lock_before_install(
    requirements, tmp_path, monkeypatch
):
    code = tmp_path / "code"
    (code / "integrations/chatgpt").mkdir(parents=True)
    (code / "integrations/chatgpt/bridge.py").write_text("# declared entrypoint\n")
    source = tmp_path / "other-source"
    source.mkdir()
    shutil.copyfile(requirements / "pyproject.toml", source / "pyproject.toml")
    (source / "uv.lock").write_text("different lock\n")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "setup",
            "--requirements-root",
            str(requirements),
            "--source-root",
            str(source),
            "--code-root",
            str(code),
            "--environment",
            str(tmp_path / "runtime"),
            "--launch",
            "bridge",
        ],
    )
    monkeypatch.setattr(
        setup, "install", lambda *args: pytest.fail("install must not run")
    )
    with pytest.raises(SystemExit) as error:
        setup.main()
    assert error.value.code == 2


def test_launch_destination_checks_source_even_when_requirements_are_exported(
    requirements, tmp_path
):
    source = tmp_path / "scientific-source"
    source.mkdir()
    alias = tmp_path / "source-alias"
    alias.symlink_to(source, target_is_directory=True)
    with pytest.raises(ValueError, match="outside"):
        setup._destination(alias / "runtime", (requirements, source))


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX pipe readiness check")
def test_concurrent_setup_lock_serializes_and_releases(tmp_path):
    destination = tmp_path / "runtime"
    script = (
        "from pathlib import Path; from integrations.chatgpt.setup_runtime import _setup_lock; "
        "import sys\n"
        "with _setup_lock(Path(sys.argv[1])): print('acquired',flush=True)\n"
    )
    with setup._setup_lock(destination):
        process = subprocess.Popen(
            [sys.executable, "-c", script, str(destination)],
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ)
                assert selector.select(timeout=0.15) == []
        except BaseException:
            process.kill()
            process.wait()
            raise
    stdout, stderr = process.communicate(timeout=10)
    assert process.returncode == 0, stderr
    assert stdout.strip() == "acquired"
