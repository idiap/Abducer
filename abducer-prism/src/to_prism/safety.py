# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Source mutation and secret-redaction safeguards."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .fingerprint import IgnoreRule, TreeFingerprint, fingerprint_tree
from .paths import PathSafetyError, canonical_path, is_within

_SECRET_KEY = re.compile(
    r"(?i)(api[_-]?key|access[_-]?token|auth[_-]?token|password|passwd|secret)"
)
_SECRET_VALUE = re.compile(
    r"(?i)(bearer\s+[a-z0-9._~+/=-]{8,}|(?:sk|ghp|github_pat|xox[baprs])[-_][a-z0-9_-]{8,})"
)


def redact_text(value: str) -> str:
    value = _SECRET_VALUE.sub("<redacted>", value)
    return re.sub(
        r"(?i)((?:api[_-]?key|token|password|secret)\s*[:=]\s*)[^\s,;]+",
        r"\1<redacted>",
        value,
    )


def redact(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): "<redacted>" if _SECRET_KEY.search(str(key)) else redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item) for item in value)
    if isinstance(value, str):
        return redact_text(value)
    return value


def assert_write_outside_source(
    requested_path: str | Path, source_root: str | Path
) -> Path:
    target = canonical_path(requested_path)
    if is_within(target, source_root):
        raise PathSafetyError("write target resolves inside protected source root")
    return target


@dataclass(slots=True)
class SourceMutationGuard:
    source: Path
    before: TreeFingerprint
    ignore_rules: tuple[IgnoreRule, ...]

    @classmethod
    def capture(
        cls,
        source: str | Path,
        ignore_rules: tuple[IgnoreRule, ...] | None = None,
    ) -> "SourceMutationGuard":
        root = canonical_path(source, must_exist=True)
        before = fingerprint_tree(root, ignore_rules=ignore_rules)
        return cls(root, before, before.ignore_rules)

    def verify(self) -> TreeFingerprint:
        after = fingerprint_tree(self.source, ignore_rules=self.ignore_rules)
        if after.digest != self.before.digest:
            raise RuntimeError(
                "source mutation detected: " + ", ".join(self.before.diff(after))
            )
        return after
