# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Apply native lifecycle hooks around the unchanged Marathon adapter.

The actual host skill is long-horizon-route-portfolio-manager. Internal canonical
operators remain operators; their names do not manufacture extra skill calls.
Known effect boundaries run PreToolUse, while native validators retain authority.
This instrumentation is confined to a fresh worker subprocess and is restored
even when the original execution or a hook fails.
"""

from __future__ import annotations

import functools
import hashlib
from pathlib import Path
import shlex
import sys

from .native_hooks import JOURNAL, NativeHookDispatcher, NativeHookError

OWNER_SKILL = "long-horizon-route-portfolio-manager"
MODULE_SOURCES = {
    "agentic.discovery.receipts": "agentic/discovery/receipts.py",
    "run_discovery_marathon": "agentic/scripts/run_discovery_marathon.py",
}


class _SubprocessBoundary:
    """Delegate the original module interface, checking actual command launches."""

    def __init__(self, original, owner):
        self.original, self.owner = original, owner

    def __getattr__(self, name):
        return getattr(self.original, name)

    def run(self, *args, **kwargs):
        command = args[0] if args else kwargs.get("args")
        if isinstance(command, (list, tuple)):
            rendered = shlex.join(str(value) for value in command)
        elif isinstance(command, str):
            rendered = command
        else:
            raise NativeHookError("Native subprocess did not supply a command")
        self.owner.require(
            "PreToolUse", {"tool": "subprocess.run", "command": rendered}
        )
        self.owner.boundaries.add("native_subprocess")
        return self.original.run(*args, **kwargs)


class _HookedServices:
    """Observe existing native callbacks; do not rewrite model prompts or outputs."""

    def __init__(self, services, state, source_root, prompt, controlled):
        self.services, self.state = services, state
        self.source_root = Path(source_root).resolve(strict=True)
        self.workspace = (Path(state["run_root"]) / "workspace").resolve()
        self.prompt, self.controlled = prompt, controlled
        self.hooks = None
        self.receipts = []
        self.boundaries = set()
        self._patches = []
        self._instrumented = set()

    def __getattr__(self, name):
        return getattr(self.services, name)

    def require(self, event, payload):
        if self.hooks is None:
            raise NativeHookError(
                "Native effect occurred before workspace hook activation"
            )
        receipt = self.hooks.require(event, payload)
        self.receipts.append(receipt)
        return receipt

    def _owner_payload(self):
        return {
            "skill": OWNER_SKILL,
            "workflow_id": "discovery_marathon_loop",
            "target_id": self.state["binding"]["target_id"],
            "run_id": self.state["binding"]["run_id"],
            "controlled": self.controlled,
        }

    def event(self, kind, payload):
        if (
            kind == "stage"
            and payload.get("stage_id") == "workspace"
            and payload.get("status") == "completed"
        ):
            if self.hooks is not None:
                raise NativeHookError("Native workspace activation was emitted twice")
            self.hooks = NativeHookDispatcher(
                source_root=self.source_root, workspace=self.workspace
            )
            self.require(
                "UserPromptSubmit", {"prompt": self.prompt, **self._owner_payload()}
            )
            self.require("PreSkillUse", self._owner_payload())
        if self.hooks is not None:
            self._instrument_available_modules()
        return self.services.event(kind, payload)

    def completion(self, *args, **kwargs):
        self._instrument_available_modules()
        self.require(
            "PreToolUse",
            {"tool": "model.completion", "model_id": self.services.model.model_id},
        )
        self.boundaries.add("host_model_completion")
        return self.services.completion(*args, **kwargs)

    def public_fetch(self, *args, **kwargs):
        self._instrument_available_modules()
        # No content, credentials or arbitrary research prompt enters the hook.
        self.require("PreToolUse", {"tool": "public_literature_fetch"})
        self.boundaries.add("host_public_fetch")
        return self.services.public_fetch(*args, **kwargs)

    def _patch(self, owner, name, replacement):
        original = getattr(owner, name)
        self._patches.append((owner, name, original))
        setattr(owner, name, replacement)

    def _instrument_available_modules(self):
        """Attach only after native imports, and verify their workspace identity."""
        if self.hooks is None:
            raise NativeHookError(
                "Native effect occurred before workspace hook activation"
            )
        for name, relative in MODULE_SOURCES.items():
            module = sys.modules.get(name)
            if module is None or name in self._instrumented:
                continue
            location = Path(getattr(module, "__file__", "")).resolve()
            expected = self.workspace / relative
            source = self.source_root / relative
            if (
                location != expected
                or not source.is_file()
                or hashlib.sha256(location.read_bytes()).digest()
                != hashlib.sha256(source.read_bytes()).digest()
            ):
                raise NativeHookError(
                    "Native instrumentation encountered a module outside its release workspace"
                )
            self._patch(
                module, "subprocess", _SubprocessBoundary(module.subprocess, self)
            )
            if name == "agentic.discovery.receipts":
                self._instrument_operators(module.DiscoveryOperatorDispatcher)
            self._instrumented.add(name)

    def _instrument_operators(self, dispatcher_class):
        """Check executable operator/validator calls, without relabeling them skills."""
        owner = self
        original_operator = dispatcher_class._invoke_operator
        original_validator = dispatcher_class._run_validator

        @functools.wraps(original_operator)
        def invoke(instance, binding, request):
            if Path(instance.workspace).resolve() != owner.workspace:
                raise NativeHookError("Native operator crossed the bound workspace")
            payload = {"tool": "native_operator", "operator_id": binding.operator_id}
            declared = request.get("declared_outputs", [])
            if declared:
                payload["path"] = declared[0]
            owner.require("PreToolUse", payload)
            owner.boundaries.add("native_operator")
            return original_operator(instance, binding, request)

        @functools.wraps(original_validator)
        def validate(instance, binding, request, *args, **kwargs):
            if Path(instance.workspace).resolve() != owner.workspace:
                raise NativeHookError("Native validator crossed the bound workspace")
            owner.require(
                "PreToolUse",
                {"tool": "native_validator", "validator_id": binding.validator_id},
            )
            owner.boundaries.add("native_validator")
            return original_validator(instance, binding, request, *args, **kwargs)

        self._patch(dispatcher_class, "_invoke_operator", invoke)
        self._patch(dispatcher_class, "_run_validator", validate)

    def finish(self, execution):
        if (
            self.hooks is None
            or Path(execution.get("workspace", "")).resolve() != self.workspace
        ):
            raise NativeHookError(
                "Native execution did not retain its activated workspace"
            )
        if set(MODULE_SOURCES) != self._instrumented:
            raise NativeHookError(
                "Native execution did not expose the required instrumentation boundaries"
            )
        binding = self.state["binding"]
        prefix = f"agentic/reports/discovery_marathon/targets/{binding['target_id']}"
        outputs = [
            f"{prefix}/{name}"
            for name in (
                "latest.json",
                "latest.md",
                "latest.html",
                "full_timeline.html",
            )
        ]
        outputs.append(
            f"agentic/runs/discovery_marathons/{binding['run_id']}/run_state.json"
        )
        self.require(
            "PostSkillUse", {**self._owner_payload(), "expected_artifacts": outputs}
        )
        self.require("Stop", self._owner_payload())
        return {
            "status": "completed",
            "source_digest": self.hooks.source_digest,
            "owner_skill": OWNER_SKILL,
            "events": sorted({receipt.event for receipt in self.receipts}),
            "tool_boundaries_observed": sorted(self.boundaries),
            "modules_instrumented": sorted(self._instrumented),
            "journal": JOURNAL,
            "receipt_count": len(self.receipts),
            "warnings": sum(
                receipt.result["decision"] == "warn" for receipt in self.receipts
            ),
            "internal_operators_are_separate_skill_invocations": False,
            "all_filesystem_writes_intercepted": False,
            "chatgpt_global_hooks": False,
        }

    def restore(self):
        for owner, name, original in reversed(self._patches):
            setattr(owner, name, original)
        self._patches.clear()


def run_hooked(adapter, *, state, services, source_root, prompt="", controlled=True):
    """Execute the original adapter with native owner/effect hooks and exact results.

    Run in the dedicated worker subprocess, never concurrently with another
    workspace in the same interpreter. The caller supplies trusted invocation
    mode; an untrusted MCP argument must not select controlled=False.
    """
    if not isinstance(prompt, str) or not isinstance(controlled, bool):
        raise NativeHookError("Expected a prompt and trusted native control mode")
    proxy = _HookedServices(services, state, source_root, prompt, controlled)
    try:
        execution = adapter.execute(state=state, services=proxy)
        coverage = proxy.finish(execution)
        return {**execution, "native_hook_coverage": coverage}
    finally:
        proxy.restore()
