"""Safe adapters for optional formal and computational tools."""

from __future__ import annotations

from dataclasses import dataclass
import shutil
import subprocess
from typing import Any


@dataclass(frozen=True, slots=True)
class ToolAdapter:
    name: str
    executable: str
    version_args: tuple[str, ...] = ("--version",)

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def probe(self, timeout: float = 5.0) -> dict[str, Any]:
        if not self.available():
            return {"adapter": self.name, "available": False, "executable": self.executable, "status": "unavailable"}
        try:
            run = subprocess.run(
                [self.executable, *self.version_args],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            text = (run.stdout or run.stderr).strip().splitlines()
            return {
                "adapter": self.name,
                "available": True,
                "executable": self.executable,
                "status": "ready" if run.returncode == 0 else "probe_failed",
                "version": text[0] if text else "unknown",
                "returncode": run.returncode,
            }
        except (OSError, subprocess.TimeoutExpired) as error:
            return {"adapter": self.name, "available": True, "status": "probe_failed", "error": str(error)}

    def run(self, args: list[str], *, timeout: float = 30.0, execute: bool = False) -> dict[str, Any]:
        command = [self.executable, *args]
        if not execute:
            return {"adapter": self.name, "status": "dry_run", "command": command, "available": self.available()}
        if not self.available():
            return {"adapter": self.name, "status": "blocked", "command": command, "reason": "executable unavailable"}
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
            return {
                "adapter": self.name,
                "status": "passed" if run.returncode == 0 else "failed",
                "command": command,
                "returncode": run.returncode,
                "stdout": run.stdout[-20000:],
                "stderr": run.stderr[-20000:],
            }
        except (OSError, subprocess.TimeoutExpired) as error:
            return {"adapter": self.name, "status": "blocked", "command": command, "reason": str(error)}


ADAPTERS = {
    "lean": ToolAdapter("Lean", "lean", ("--version",)),
    "mmt": ToolAdapter("MMT", "mmt", ("--help",)),
    "gatlab": ToolAdapter("GATlab", "julia", ("--version",)),
    "cubical_agda": ToolAdapter("Cubical Agda", "agda", ("--version",)),
    "smt_z3": ToolAdapter("Z3 SMT", "z3", ("--version",)),
    "simulation_python": ToolAdapter("Python simulation", "python", ("--version",)),
}


def adapter_report() -> list[dict[str, Any]]:
    return [adapter.probe() for adapter in ADAPTERS.values()]

