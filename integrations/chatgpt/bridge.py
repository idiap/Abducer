# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Authenticated Sites-to-native bridge over the existing research service.

Sites authenticates the browser and signs a server-to-server request containing
its principal. This boundary maps that principal to an explicitly provisioned
native account; it never accepts a backend subject in tool arguments. Nonces
are consumed durably in the research database, while paid starts retain the
Store's existing idempotency contract. The bridge does not execute model work
in an HTTP request or replace the native workflow and hook admission rules.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import sqlite3
import time
from typing import Mapping
import uuid

from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from .server import Service, public_job
from .store import AccessDenied
from .provider import ProviderError

BRIDGE_PATH = "/bridge/v1/call"
MAX_REQUEST_BYTES = 1024 * 1024
ORDINARY_REQUEST_BYTES = 65536
# A 65,536-character report can expand sixfold when JSON escapes controls.
MAX_RESPONSE_BYTES = 524288
_HEX_KEY = re.compile(r"[a-fA-F0-9]{64}\Z")
_NONCE = re.compile(r"[a-f0-9]{32}\Z")
_SIGNATURE = re.compile(r"[a-f0-9]{64}\Z")


@dataclass(frozen=True)
class BridgeConfig:
    """Operator-owned bridge credentials and Sites-to-native identity bindings."""

    audience: str
    key_hex: str = field(repr=False)
    subjects: Mapping[str, str] = field(default_factory=dict, repr=False)
    max_clock_skew_seconds: int = 60

    def __post_init__(self):
        _text(self.audience, "audience", 200)
        if not isinstance(self.key_hex, str) or not _HEX_KEY.fullmatch(self.key_hex):
            raise ValueError("Bridge key must encode exactly 32 random bytes as hex")
        if (
            not isinstance(self.subjects, Mapping)
            or not self.subjects
            or any(
                not isinstance(value, str) or not value or len(value) > 512
                for pair in self.subjects.items()
                for value in pair
            )
        ):
            raise ValueError("Explicit bounded Sites-to-native subjects are required")
        if not 1 <= self.max_clock_skew_seconds <= 300:
            raise ValueError("Bridge freshness window must be 1–300 seconds")

    @classmethod
    def from_env(cls):
        try:
            subjects = json.loads(os.environ["ABDUCER_NATIVE_BRIDGE_SUBJECTS_JSON"])
            if not isinstance(subjects, dict):
                raise ValueError
            return cls(
                audience=os.environ["ABDUCER_NATIVE_BRIDGE_AUDIENCE"],
                key_hex=os.environ["ABDUCER_NATIVE_BRIDGE_KEY"],
                subjects=subjects,
            )
        except (KeyError, json.JSONDecodeError) as error:
            raise ValueError(
                "Configure the native bridge audience, key and subject map"
            ) from error


@dataclass(frozen=True)
class BridgeRuntimeConfig:
    """Service runtime settings without an unused or fabricated OAuth issuer.

    The Service needs source, state and budget settings. OAuth transport settings
    belong to Config and its MCP server; this separate signed transport does not
    instantiate that server or its JWT verifier.
    """

    repository_root: Path
    data_root: Path
    worker_enabled: bool = False
    require_online_worker: bool = False
    max_active_jobs: int = 2
    max_timeout_seconds: int = 7200
    max_model_calls: int = 50
    max_output_tokens: int = 32000

    @property
    def database(self):
        return self.data_root / "service.sqlite3"

    @classmethod
    def from_env(cls):
        try:
            return cls(
                repository_root=Path(os.environ["ABDUCER_REPOSITORY_ROOT"]).resolve(
                    strict=True
                ),
                data_root=Path(os.environ["ABDUCER_DATA_ROOT"]).resolve(),
                worker_enabled=os.environ.get("ABDUCER_WORKER_ENABLED", "false").lower()
                == "true",
                require_online_worker=True,
            )
        except KeyError as error:
            raise ValueError(
                "Configure ABDUCER_REPOSITORY_ROOT and ABDUCER_DATA_ROOT"
            ) from error


class BridgeError(ValueError):
    """A bounded public error, independent of internal exception messages."""

    def __init__(self, code, message, status=400):
        super().__init__(message)
        self.code, self.status = code, status


def _text(value, label, limit=160):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"Invalid {label}")
    return value


def signing_message(body: bytes, audience: str, timestamp: str, nonce: str) -> bytes:
    """Bind method, route, deployment audience, freshness and exact bytes."""
    return "\n".join(
        [
            "abducer-bridge-v1",
            "POST",
            BRIDGE_PATH,
            audience,
            timestamp,
            nonce,
            hashlib.sha256(body).hexdigest(),
        ]
    ).encode()


def _strict_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("Duplicate JSON member")
        obj[key] = value
    return obj


class Bridge:
    """Authenticate requests and delegate to unchanged Service/Store operations."""

    def __init__(self, service: Service, config: BridgeConfig):
        self.service, self.config = service, config
        from .chatgpt_model import ModelRendezvous

        self.models = ModelRendezvous(service.store)
        with service.store.connection(write=True) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS bridge_nonces(audience TEXT NOT NULL, nonce TEXT NOT NULL, expires REAL NOT NULL, PRIMARY KEY(audience,nonce))"
            )
            db.execute(
                "CREATE INDEX IF NOT EXISTS bridge_nonce_expiry ON bridge_nonces(expires)"
            )
            db.execute(
                "CREATE TABLE IF NOT EXISTS bridge_projects(audience TEXT NOT NULL, principal TEXT NOT NULL, external_id TEXT NOT NULL, project_id TEXT NOT NULL REFERENCES projects(id), PRIMARY KEY(audience,principal,external_id))"
            )

    def authenticate(self, raw: bytes, headers: Mapping[str, str], *, now=None):
        """Reject unsigned, stale, replayed or unprovisioned requests before work."""
        now = time.time() if now is None else now
        timestamp = headers.get("x-abducer-timestamp", "")
        nonce = headers.get("x-abducer-nonce", "")
        signature = headers.get("x-abducer-signature", "")
        if (
            not re.fullmatch(r"[0-9]{10,11}", timestamp)
            or abs(now - int(timestamp)) > self.config.max_clock_skew_seconds
            or not _NONCE.fullmatch(nonce)
            or not _SIGNATURE.fullmatch(signature)
        ):
            raise BridgeError("unauthenticated", "Bridge authentication failed", 401)
        expected = hmac.new(
            bytes.fromhex(self.config.key_hex),
            signing_message(raw, self.config.audience, timestamp, nonce),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected, signature):
            raise BridgeError("unauthenticated", "Bridge authentication failed", 401)
        try:
            envelope = json.loads(
                raw,
                object_pairs_hook=_strict_object,
                parse_constant=lambda _: (_ for _ in ()).throw(
                    ValueError("Invalid number")
                ),
            )
            if not isinstance(envelope, dict) or set(envelope) != {
                "version",
                "audience",
                "principal",
                "operation",
                "arguments",
            }:
                raise ValueError
            if (
                type(envelope["version"]) is not int
                or envelope["version"] != 1
                or envelope["audience"] != self.config.audience
            ):
                raise ValueError
            if (
                len(raw) > ORDINARY_REQUEST_BYTES
                and envelope["operation"] != "submit_model_response"
            ):
                raise BridgeError(
                    "request_too_large",
                    "Only model response submission may exceed 64 KiB",
                    413,
                )
            principal = _text(envelope["principal"], "principal", 512)
            subject = self.config.subjects.get(principal)
            if not subject:
                raise AccessDenied("Account is not linked to native execution")
            self.service.store.profile(subject)
        except (ValueError, TypeError, UnicodeError) as error:
            if isinstance(error, BridgeError):
                raise
            if isinstance(error, AccessDenied):
                raise BridgeError(
                    "forbidden", "Account is not linked or is disabled", 403
                ) from error
            raise BridgeError("invalid_request", "Invalid bridge envelope") from error
        # Persist nonce consumption before dispatch, across workers and restarts.
        # A fresh nonce may retry a start using the same durable idempotency key.
        try:
            with self.service.store.connection(write=True) as db:
                db.execute("DELETE FROM bridge_nonces WHERE expires < ?", (now,))
                db.execute(
                    "INSERT INTO bridge_nonces VALUES(?,?,?)",
                    (
                        self.config.audience,
                        nonce,
                        now + 2 * self.config.max_clock_skew_seconds + 1,
                    ),
                )
        except sqlite3.IntegrityError as error:
            raise BridgeError(
                "replayed_request", "Bridge request was already consumed", 409
            ) from error
        return principal, subject, envelope["operation"], envelope["arguments"]

    def bind_project(self, principal, subject, external_id, title):
        """Idempotently bind one owned Sites project to one existing Store project."""
        external_id = _text(external_id, "Sites project ID", 80)
        title = _text(title, "project title", 200)
        with self.service.store.connection(write=True) as db:
            self.service.store._user(db, subject)
            row = db.execute(
                "SELECT project_id FROM bridge_projects WHERE audience=? AND principal=? AND external_id=?",
                (self.config.audience, principal, external_id),
            ).fetchone()
            if row:
                return self.service.store._project(
                    db, subject, row["project_id"], True
                )["id"]
            if (
                db.execute(
                    "SELECT count(*) FROM bridge_projects WHERE audience=? AND principal=?",
                    (self.config.audience, principal),
                ).fetchone()[0]
                >= 100
            ):
                raise ValueError("Native project binding limit reached")
            project_id = uuid.uuid4().hex
            db.execute(
                "INSERT INTO projects(id,name) VALUES(?,?)", (project_id, title.strip())
            )
            db.execute(
                "INSERT INTO members VALUES(?,?,?)", (project_id, subject, "admin")
            )
            db.execute(
                "INSERT INTO bridge_projects VALUES(?,?,?,?)",
                (self.config.audience, principal, external_id, project_id),
            )
            return project_id

    def dispatch(self, principal, subject, operation, arguments):
        """Keep bridge commands explicit; never expose arbitrary Service methods."""
        allowed = {
            "get_execution_capabilities": (set(), set()),
            "bind_project": ({"project_id", "title"}, {"project_id", "title"}),
            "prepare_research_run": (
                {
                    "project_id",
                    "title",
                    "workflow_id",
                    "inputs",
                    "budget_seconds",
                    "max_model_calls",
                    "max_output_tokens",
                },
                {"project_id", "title", "workflow_id", "inputs"},
            ),
            "start_research_run": (
                {"plan_id", "idempotency_key"},
                {"plan_id", "idempotency_key"},
            ),
            "get_run_status": ({"job_id"}, {"job_id"}),
            "list_runs": ({"project_id", "title", "limit"}, {"project_id", "title"}),
            "list_run_artifacts": ({"job_id"}, {"job_id"}),
            "get_report": (
                {"job_id", "artifact_id", "offset", "length"},
                {"job_id", "artifact_id"},
            ),
            "cancel_run": ({"job_id"}, {"job_id"}),
            "get_pending_model_request": ({"job_id", "offset", "limit"}, {"job_id"}),
            "submit_model_response": (
                {"job_id", "request_id", "content"},
                {"job_id", "request_id", "content"},
            ),
            "get_workflow_dependencies": (
                {"workflow_id", "offset", "limit"},
                {"workflow_id"},
            ),
            "get_workflow_dependency_source": (
                {"workflow_id", "path", "offset", "limit"},
                {"workflow_id", "path"},
            ),
            "validate_hypothesis_map": (
                {"project_id", "title", "content"},
                {"project_id", "title", "content"},
            ),
            "get_validation_receipt": (
                {"project_id", "title", "receipt_id"},
                {"project_id", "title", "receipt_id"},
            ),
            "list_validation_receipts": (
                {"project_id", "title", "limit"},
                {"project_id", "title"},
            ),
        }
        if not isinstance(operation, str) or operation not in allowed:
            raise ValueError("Unknown native bridge operation")
        keys, required = allowed[operation]
        if (
            not isinstance(arguments, dict)
            or not required <= arguments.keys()
            or arguments.keys() - keys
        ):
            raise ValueError("Invalid native bridge arguments")
        args = dict(arguments)
        for name in (
            "job_id",
            "artifact_id",
            "plan_id",
            "idempotency_key",
            "workflow_id",
            "request_id",
            "receipt_id",
        ):
            if name in args:
                _text(args[name], name, 160)
        if operation == "get_execution_capabilities":
            capabilities = {**self.service.capabilities(), "bridge_authenticated": True}
            if "chatgpt" in capabilities.get("model_providers", []):
                capabilities["chatgpt_model_limits"] = {
                    "token_limit_enforcement": "requested_guidance_only",
                    "token_usage_observed": False,
                    "response_byte_limit": 384 * 1024,
                }
            return capabilities
        if operation == "get_workflow_dependencies":
            return self.service.dependencies(subject, **args)
        if operation == "get_workflow_dependency_source":
            return self.service.dependency_source(subject, **args)
        if operation in {
            "bind_project",
            "prepare_research_run",
            "list_runs",
            "validate_hypothesis_map",
            "get_validation_receipt",
            "list_validation_receipts",
        }:
            project_id = self.bind_project(
                principal, subject, args.pop("project_id"), args.pop("title")
            )
            if operation == "bind_project":
                return {"native_project_id": project_id}
            if operation == "prepare_research_run":
                return self.service.prepare(subject, project_id, **args)
            if operation == "validate_hypothesis_map":
                from .validation_service import validate_conceptual

                return validate_conceptual(
                    self.service, subject, project_id, args["content"]
                )
            if operation == "get_validation_receipt":
                from .validation_service import get_validation

                return get_validation(
                    self.service, subject, project_id, args["receipt_id"]
                )
            if operation == "list_validation_receipts":
                from .validation_service import list_validations

                return list_validations(self.service, subject, project_id, **args)
            limit = args.get("limit", 50)
            if type(limit) is not int or not 1 <= limit <= 100:
                raise ValueError("Invalid run list limit")
            return {
                "runs": [
                    public_job(job)
                    for job in self.service.store.list_runs(subject, project_id, limit)
                ]
            }
        if operation == "start_research_run":
            return self.service.start(subject, **args)
        if operation == "get_run_status":
            return {
                **public_job(self.service.store.get_job(subject, **args)),
                **self.models.metadata(subject, args["job_id"]),
            }
        if operation == "get_pending_model_request":
            return self.models.pending(subject, **args)
        if operation == "submit_model_response":
            return self.models.submit(subject, **args)
        if operation == "list_run_artifacts":
            return self.service.artifacts(subject, **args)
        if operation == "get_report":
            return self.service.report(subject, **args)
        return public_job(self.service.store.cancel_job(subject, **args))

    def call(self, raw, headers):
        principal, subject, operation, args = self.authenticate(raw, headers)
        return self.dispatch(principal, subject, operation, args)


def create_bridge_app(service: Service, config: BridgeConfig) -> Starlette:
    """Build a bounded ASGI endpoint; native job processing remains asynchronous."""
    bridge = Bridge(service, config)

    async def endpoint(request: Request):
        try:
            if request.headers.get("origin"):
                raise BridgeError("forbidden", "Server-to-server requests only", 403)
            if (
                request.headers.get("content-type", "").split(";", 1)[0].lower()
                != "application/json"
            ):
                raise BridgeError("invalid_request", "JSON content type required")
            raw = bytearray()
            async for chunk in request.stream():
                if len(raw) + len(chunk) > MAX_REQUEST_BYTES:
                    raise BridgeError(
                        "request_too_large", "Bridge request exceeds 1 MiB", 413
                    )
                raw.extend(chunk)
            result = await run_in_threadpool(bridge.call, bytes(raw), request.headers)
            body = json.dumps(
                {"result": result},
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode()
            if len(body) > MAX_RESPONSE_BYTES:
                raise BridgeError(
                    "response_too_large", "Native result requires bounded paging", 502
                )
            return Response(
                body,
                media_type="application/json",
                headers={"Cache-Control": "no-store"},
            )
        except BridgeError as error:
            return JSONResponse(
                {"error": {"code": error.code, "message": str(error)}},
                status_code=error.status,
            )
        except AccessDenied:
            return JSONResponse(
                {
                    "error": {
                        "code": "forbidden",
                        "message": "Native object is unavailable or operation is not permitted",
                    }
                },
                status_code=403,
            )
        except ProviderError as error:
            return JSONResponse(
                {
                    "error": {
                        "code": "execution_state_conflict",
                        "message": str(error)[:400],
                    }
                },
                status_code=409,
            )
        except ValueError as error:
            # Service validation messages are designed for users and contain no
            # credentials. Unexpected internal errors never disclose tracebacks.
            return JSONResponse(
                {"error": {"code": "invalid_request", "message": str(error)[:400]}},
                status_code=400,
            )
        except Exception:
            return JSONResponse(
                {
                    "error": {
                        "code": "native_unavailable",
                        "message": "Native bridge request failed",
                    }
                },
                status_code=503,
            )

    return Starlette(routes=[Route(BRIDGE_PATH, endpoint, methods=["POST"])])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    args = parser.parse_args()
    import uvicorn

    service = Service(BridgeRuntimeConfig.from_env())
    uvicorn.run(
        create_bridge_app(service, BridgeConfig.from_env()),
        host=args.host,
        port=args.port,
        access_log=False,
    )


if __name__ == "__main__":
    main()
