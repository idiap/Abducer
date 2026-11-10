# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Explicit deployment configuration; a missing identity provider fails closed."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from urllib.parse import urlsplit


def https_url(value: str, label: str) -> str:
    parsed = urlsplit(value)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            f"{label} must be an absolute HTTPS URL without credentials/query/fragment"
        )
    return value


@dataclass(frozen=True)
class Config:
    repository_root: Path
    data_root: Path
    public_url: str
    issuer: str
    jwks_url: str
    audience: str
    required_scope: str = "abducer"
    worker_enabled: bool = False
    max_active_jobs: int = 2
    max_timeout_seconds: int = 7200
    max_model_calls: int = 50
    max_output_tokens: int = 32000

    def __post_init__(self):
        for label in ("public_url", "issuer", "jwks_url", "audience"):
            https_url(getattr(self, label), label)
        if self.public_url.endswith("/"):
            raise ValueError("public_url must not end with a slash")
        if self.audience != self.public_url + "/mcp":
            raise ValueError(
                "OAuth audience must equal the canonical public /mcp resource"
            )
        if not self.required_scope or any(c.isspace() for c in self.required_scope):
            raise ValueError("Exactly one nonempty required scope is required")
        if not self.repository_root.is_dir():
            raise ValueError("Repository root does not exist")

    @property
    def database(self) -> Path:
        return self.data_root / "service.sqlite3"

    @classmethod
    def from_env(cls) -> "Config":
        def required(name):
            value = os.environ.get(name)
            if not value:
                raise ValueError(f"Required environment variable is missing: {name}")
            return value

        public = required("ABDUCER_PUBLIC_URL").rstrip("/")
        return cls(
            repository_root=Path(
                os.environ.get(
                    "ABDUCER_REPOSITORY_ROOT", Path(__file__).resolve().parents[2]
                )
            ).resolve(),
            data_root=Path(required("ABDUCER_DATA_ROOT")).resolve(),
            public_url=public,
            issuer=required("ABDUCER_OIDC_ISSUER"),
            jwks_url=required("ABDUCER_OIDC_JWKS_URL"),
            audience=os.environ.get("ABDUCER_OAUTH_AUDIENCE", public + "/mcp"),
            required_scope=os.environ.get("ABDUCER_REQUIRED_SCOPE", "abducer"),
            worker_enabled=os.environ.get("ABDUCER_WORKER_ENABLED", "false").lower()
            == "true",
        )
