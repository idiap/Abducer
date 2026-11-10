# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Authenticated MCP HTTP transport over the existing Abducer catalogs.

Every tool resolves a provisioned subject from the request token. Catalog reads
remain independent of scientific execution; starts only enqueue bounded work.
The background worker owns native execution and verified artifact publication.
"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit
from typing import Any

from mcp.server.auth.middleware.auth_context import get_access_token
from mcp.server.auth.settings import AuthSettings
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.responses import JSONResponse

from .auth import JWTVerifier
from .catalog import Catalog, CONTRACT_ID, RUNTIME_ID, TARGETS
from .config import Config
from .store import AccessDenied, Store
from .runtime import verify_snapshot
from .execution_registry import ExecutionRegistry

UI_URI = "ui://abducer/explorer/v1.html"


def public_job(job):
    """Exclude infrastructure paths, credentials and private checkpoint state."""
    keys = (
        "job_id",
        "project_id",
        "status",
        "created",
        "updated",
        "workflow_id",
        "contract_workflow_id",
        "inputs",
        "budget",
        "release",
        "parent_version",
        "cancel_requested",
        "error",
    )
    result = {key: job[key] for key in keys if key in job}
    if job.get("result"):
        # Worker results must not leak its absolute workspace/checkpoint paths.
        value = job["result"].get("structured_value", job["result"])
        result["outcome"] = {
            key: value[key]
            for key in ("target_id", "run_id", "cycle_count", "execution_outcome")
            if key in value
        }
        result["outcome"]["scientific_truth_verified"] = False
        result["outcome"]["verification"] = (
            job["result"].get("report_verification", {}).get("status")
        )
        result["outcome"]["model_calls"] = job["result"].get("model_calls")
        if job["result"].get("native_hook_coverage"):
            result["outcome"]["native_hook_coverage"] = job["result"][
                "native_hook_coverage"
            ]
    return result


class Service:
    """Testable application boundary shared by MCP and the worker store."""

    def __init__(self, config: Config, store=None):
        self.config = config
        self.store = store or Store(config.database)
        self.catalog = Catalog(config.repository_root)
        self.execution_registry = ExecutionRegistry(
            config.repository_root, catalog=self.catalog
        )
        from .startup import preload

        self.startup = preload(self.execution_registry)
        self.runtime_source_sha256 = None
        self.readiness_reason = "Operator has not enabled the hosted worker"
        if config.worker_enabled:
            try:
                self.runtime_source_sha256 = verify_snapshot(config.repository_root)[
                    "content_sha256"
                ]
                self.readiness_reason = "Verified immutable worker source configured"
            except (ValueError, OSError, KeyError):
                self.readiness_reason = "Worker source must be built and verified as an immutable deployment snapshot"

    @property
    def executable(self):
        configured = (
            self.config.worker_enabled
            and self.runtime_source_sha256 is not None
            and self.startup["packages"]["status"] == "ready"
        )
        if not configured or not getattr(self.config, "require_online_worker", False):
            return configured
        return any(
            row["provider_ready"] and row["hooks_enabled"]
            for row in self.store.worker_presence(self.runtime_source_sha256)
        )

    def capabilities(self):
        presence = (
            self.store.worker_presence(self.runtime_source_sha256)
            if self.runtime_source_sha256
            else []
        )
        reason = self.readiness_reason
        if self.startup["packages"]["status"] != "ready":
            reason = "Runtime dependencies are missing or differ from the source lock; run Abducer setup"
        elif (
            getattr(self.config, "require_online_worker", False)
            and self.runtime_source_sha256
            and not self.executable
        ):
            reason = "No recent worker with this source release, configured model provider and native hooks"
        return {
            "release": self.catalog.release,
            "dependency_setup": self.startup,
            "skills_count": len(self.catalog.skills),
            "workflows_count": len(self.catalog.native.rows),
            "viewer_count": len(self.catalog.viewers),
            "executable_workflows": [CONTRACT_ID] if self.executable else [],
            "execution_reason": reason,
            "worker_online": bool(presence),
            "model_providers": sorted(
                {row["provider"] for row in presence if row["provider_ready"]}
            ),
            "native_hooks_enabled": any(row["hooks_enabled"] for row in presence),
            "workflow_execution": self.execution_registry.list(
                runtime_enabled=bool(self.executable)
            )["workflows"],
            "targets": list(TARGETS),
            "limits": {
                "timeout_seconds": self.config.max_timeout_seconds,
                "max_model_calls": self.config.max_model_calls,
                "max_output_tokens": self.config.max_output_tokens,
                "active_jobs_per_user": self.config.max_active_jobs,
            },
            "scientific_truth_verified": False,
        }

    def prepare(
        self,
        subject,
        project_id,
        workflow_id,
        inputs,
        budget_seconds=7200,
        max_model_calls=50,
        max_output_tokens=32000,
    ):
        self.store.project(subject, project_id, write=True)
        if not self.executable or workflow_id != CONTRACT_ID:
            raise ValueError(
                "This workflow is inspectable but not enabled for hosted execution"
            )
        if (
            not isinstance(inputs, dict)
            or set(inputs) != {"target_id", "allow_public_network"}
            or inputs["target_id"] not in TARGETS
            or not isinstance(inputs["allow_public_network"], bool)
        ):
            raise ValueError(
                "Inputs require a registered target_id and explicit allow_public_network boolean"
            )
        project = self.store.project(subject, project_id, write=True)
        previous = project.get("checkpoint")
        if (
            previous
            and previous.get("binding", {}).get("target_id") != inputs["target_id"]
        ):
            raise ValueError(
                "A project continuation must retain its original target; create another project"
            )
        if not previous and not inputs["allow_public_network"]:
            raise ValueError(
                "New research initialization requires declared public literature reads"
            )
        limits = (
            (budget_seconds, self.config.max_timeout_seconds),
            (max_model_calls, self.config.max_model_calls),
            (max_output_tokens, self.config.max_output_tokens),
        )
        if any(
            type(value) is not int or not 1 <= value <= ceiling
            for value, ceiling in limits
        ):
            raise ValueError("Requested budget is outside the configured bounds")
        if max_output_tokens < 32000:
            raise ValueError(
                "The canonical research route requires a 32000-token per-call output allowance"
            )
        # Bind the advertised provider to this plan. An operator switching from
        # in-chat responses to API completion cannot silently change a queued run.
        if getattr(self.config, "require_online_worker", False):
            providers = {
                row["provider"]
                for row in self.store.worker_presence(self.runtime_source_sha256)
                if row["provider_ready"] and row["hooks_enabled"]
            }
            if len(providers) != 1:
                raise ValueError(
                    "Native admission requires one unambiguous model provider"
                )
            inputs = {
                **inputs,
                "model_provider": next(iter(providers)),
                "native_hooks_required": True,
            }
        plan = self.store.prepare_plan(
            subject,
            project_id,
            workflow_id=RUNTIME_ID,
            contract_workflow_id=CONTRACT_ID,
            inputs=inputs,
            budget={
                "timeout_seconds": budget_seconds,
                "max_model_calls": max_model_calls,
                "max_output_tokens": max_output_tokens,
            },
            release=self.catalog.release,
            runtime_source_sha256=self.runtime_source_sha256,
        )
        return {key: value for key, value in plan.items() if key != "parent_checkpoint"}

    def dependencies(self, subject, workflow_id, offset=0, limit=100):
        """Page exact declared sources without asserting untested runtime closure."""
        self.store.profile(subject)
        if (
            type(offset) is not int
            or offset < 0
            or type(limit) is not int
            or not 1 <= limit <= 100
        ):
            raise ValueError("Invalid dependency pagination")
        manifest = self.execution_registry.dependency_manifest(workflow_id)
        entries = manifest.pop("entries")
        end = min(offset + limit, len(entries))
        return {
            **manifest,
            "entries": entries[offset:end],
            "offset": offset,
            "total": len(entries),
            "next_offset": end if end < len(entries) else None,
        }

    def dependency_source(self, subject, workflow_id, path, offset=0, limit=16000):
        """Read only a file admitted by this workflow's dependency manifest."""
        self.store.profile(subject)
        return self.execution_registry.read_dependency(
            workflow_id, path, offset=offset, limit=limit
        )

    def start(self, subject, plan_id, idempotency_key):
        if not self.executable:
            raise ValueError("Hosted execution is disabled")
        current = verify_snapshot(self.config.repository_root)["content_sha256"]
        if current != self.runtime_source_sha256:
            raise ValueError(
                "Worker source changed; restart service with a verified release"
            )
        return public_job(
            self.store.start_job(
                subject,
                plan_id,
                idempotency_key,
                release=self.catalog.release,
                runtime_source_sha256=current,
                max_active_jobs=self.config.max_active_jobs,
            )
        )

    def artifacts(self, subject, job_id):
        return {
            "artifacts": [
                {key: value for key, value in item.items() if key != "relative_path"}
                for item in self.store.artifacts(subject, job_id)
            ]
        }

    def report(self, subject, job_id, artifact_id, offset=0, length=20000):
        if (
            type(offset) is not int
            or offset < 0
            or type(length) is not int
            or not 1 <= length <= 65536
        ):
            raise ValueError(
                "Report range must be nonnegative and at most 65536 characters"
            )
        matches = [
            item
            for item in self.store.artifacts(subject, job_id)
            if item["id"] == artifact_id
        ]
        if len(matches) != 1:
            raise AccessDenied("Artifact is unavailable")
        item = matches[0]
        relative = item["relative_path"]
        pure = PurePosixPath(relative)
        if (
            pure.is_absolute()
            or any(p in {".", "..", ""} for p in relative.split("/"))
            or "\\" in relative
        ):
            raise ValueError("Artifact path is not confined")
        path = self.config.data_root / relative
        if any(
            part.is_symlink() for part in (path, *path.parents)
        ) or not path.resolve().is_relative_to(self.config.data_root.resolve()):
            raise ValueError("Artifact path is not confined")
        # Full timeline HTML includes embedded mathematics and can exceed
        # 32 MiB. Keep reads paginated while admitting these original reports.
        if path.stat().st_size > 64 * 1024 * 1024:
            raise ValueError("Artifact exceeds the bounded report reader")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != item["sha256"]:
            raise ValueError("Published artifact digest changed")
        text = raw.decode("utf-8")
        return {
            "artifact_id": artifact_id,
            "job_id": job_id,
            "media_type": item["media_type"],
            "sha256": item["sha256"],
            "offset": offset,
            "total_characters": len(text),
            "text": text[offset : offset + length],
            "next_offset": offset + length if offset + length < len(text) else None,
        }


def create_server(config: Config, store=None, verifier=None) -> FastMCP:
    service = Service(config, store)
    verifier = verifier or JWTVerifier(config, service.store)
    authority = urlsplit(config.public_url).netloc
    server = FastMCP(
        "Abducer",
        instructions="Use get_capabilities before planning research. Read-only catalog visibility does not imply executable support. Prepare and review a bounded plan before starting a job. Preserve evidence and scientific claim status.",
        token_verifier=verifier,
        auth=AuthSettings(
            issuer_url=config.issuer,
            resource_server_url=config.audience,
            required_scopes=[config.required_scope],
            validate_token_resource=True,
        ),
        stateless_http=True,
        json_response=True,
        max_request_body_size=1024 * 1024,
        transport_security=TransportSecuritySettings(
            allowed_hosts=[authority, "127.0.0.1:*", "localhost:*"],
            allowed_origins=[
                config.public_url,
                "https://chatgpt.com",
                "https://chat.openai.com",
            ],
        ),
    )

    def subject():
        token = get_access_token()
        if token is None or not token.subject:
            raise AccessDenied("Authenticated named account required")
        service.store.profile(token.subject)
        return token.subject

    read = ToolAnnotations(
        readOnlyHint=True, destructiveHint=False, openWorldHint=False
    )
    write = ToolAnnotations(
        readOnlyHint=False, destructiveHint=False, openWorldHint=False
    )

    @server.tool(annotations=read, meta={"openai/profile": True})
    def get_profile() -> dict[str, Any]:
        """Identify the linked, provisioned Abducer account."""
        return {**service.store.profile(subject()), "dependency_setup": service.startup}

    @server.tool(annotations=read)
    def list_projects() -> dict[str, Any]:
        """List only projects accessible to the linked account."""
        return {"projects": service.store.list_projects(subject())}

    @server.tool(annotations=write)
    def create_project(name: str) -> dict[str, Any]:
        """Create a private research project owned by the linked account."""
        project = service.store.create_project(subject(), name)
        return {key: value for key, value in project.items() if key != "checkpoint"}

    @server.tool(annotations=read)
    def list_workflows() -> dict[str, Any]:
        """List normalized workflow contracts; executable status is explicit."""
        subject()
        return service.catalog.list_workflows(service.executable)

    @server.tool(annotations=read)
    def get_workflow(workflow_id: str) -> dict[str, Any]:
        """Read a canonical contract and its source-backed typed viewer graph."""
        subject()
        return service.catalog.get_workflow(workflow_id)

    @server.tool(annotations=read)
    def search_skills(
        query: str = "", cursor: int = 0, limit: int = 25
    ) -> dict[str, Any]:
        """Search canonical public skills with bounded pagination; inspection only."""
        subject()
        return service.catalog.search_skills(query, cursor, limit)

    @server.tool(annotations=read)
    def get_skill(skill_id: str) -> dict[str, Any]:
        """Read release-pinned original skill instructions without executing them."""
        subject()
        return service.catalog.get_skill(skill_id)

    @server.tool(annotations=read)
    def get_capabilities() -> dict[str, Any]:
        """Inspect current runtime admission, supported targets and budget ceilings."""
        subject()
        return service.capabilities()

    @server.tool(annotations=write)
    def prepare_research_run(
        project_id: str,
        workflow_id: str,
        inputs: dict,
        budget_seconds: int = 7200,
        max_model_calls: int = 50,
        max_output_tokens: int = 32000,
    ) -> dict[str, Any]:
        """Persist a bounded 15-minute plan without launching model work. Review its inputs and budget before start."""
        return service.prepare(
            subject(),
            project_id,
            workflow_id,
            inputs,
            budget_seconds,
            max_model_calls,
            max_output_tokens,
        )

    @server.tool(
        annotations=ToolAnnotations(
            readOnlyHint=False,
            destructiveHint=False,
            openWorldHint=True,
            idempotentHint=True,
        )
    )
    def start_research_run(plan_id: str, idempotency_key: str) -> dict[str, Any]:
        """Queue one reviewed plan. Starts billable model/public-literature work; repeat the same key only to recover this exact start."""
        return service.start(subject(), plan_id, idempotency_key)

    @server.tool(annotations=read)
    def get_run_status(job_id: str) -> dict[str, Any]:
        """Read durable job status, including failed/cancelled outcomes."""
        return public_job(service.store.get_job(subject(), job_id))

    @server.tool(annotations=read)
    def list_runs(project_id: str, limit: int = 50) -> dict[str, Any]:
        """Read the most recent authorized project runs."""
        return {
            "runs": [
                public_job(job)
                for job in service.store.list_runs(subject(), project_id, limit)
            ]
        }

    @server.tool(annotations=read)
    def list_run_artifacts(job_id: str) -> dict[str, Any]:
        """List verified published artifacts; failures do not substitute historical reports."""
        return service.artifacts(subject(), job_id)

    @server.tool(annotations=read)
    def get_report(
        job_id: str, artifact_id: str, offset: int = 0, length: int = 20000
    ) -> dict[str, Any]:
        """Read a bounded digest-checked UTF-8 report excerpt from an authorized run."""
        return service.report(subject(), job_id, artifact_id, offset, length)

    @server.tool(annotations=write)
    def cancel_run(job_id: str) -> dict[str, Any]:
        """Request termination; running remains running until the worker records its terminal outcome."""
        return public_job(service.store.cancel_job(subject(), job_id))

    @server.tool(
        annotations=read,
        meta={
            "ui": {"resourceUri": UI_URI},
            "openai/ui": {"entrypoints": [{"type": "global"}, {"type": "thread"}]},
        },
    )
    def open_explorer(
        project_id: str | None = None,
        workflow_id: str | None = None,
        job_id: str | None = None,
    ) -> dict[str, Any]:
        """Open Explorer for validated catalog/project/run IDs. Data tools remain usable without this UI."""
        identity = subject()
        if project_id:
            service.store.project(identity, project_id)
        job = service.store.get_job(identity, job_id) if job_id else None
        if job and project_id and job["project_id"] != project_id:
            raise ValueError("Run does not belong to the selected project")
        result = {
            "release": service.catalog.release,
            "selection": {
                "project_id": project_id or (job["project_id"] if job else None),
                "workflow_id": workflow_id,
                "job_id": job_id,
            },
            "projects": service.store.list_projects(identity),
            "workflows": service.catalog.list_workflows(service.executable)[
                "workflows"
            ],
        }
        if workflow_id:
            result.update(service.catalog.get_workflow(workflow_id))
        if job:
            result["run"] = public_job(job)
        return result

    @server.resource(
        UI_URI,
        mime_type="text/html;profile=mcp-app",
        meta={
            "ui": {
                "prefersBorder": True,
                "csp": {"connectDomains": [], "resourceDomains": []},
            }
        },
    )
    def explorer_resource() -> str:
        """Serve the bundled UI shell; private research data arrives through authorized tools."""
        subject()
        from integrations.chatgpt.ui import explorer_html

        return explorer_html()

    @server.custom_route("/healthz", methods=["GET"])
    async def health(request):
        return JSONResponse(
            {"status": "ok", "service": "abducer", "release": service.catalog.release}
        )

    return server


def create_app(config: Config, store=None, verifier=None):
    """Return the production ASGI application, also used by HTTP integration tests."""
    return create_server(config, store, verifier).streamable_http_app()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    serve = commands.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=8000)
    provision = commands.add_parser("provision-user")
    provision.add_argument("--subject", required=True)
    provision.add_argument("--name", required=True)
    provision.add_argument("--disabled", action="store_true")
    grant = commands.add_parser("grant-project")
    grant.add_argument("--subject", required=True)
    grant.add_argument("--project-id", required=True)
    grant.add_argument(
        "--role", choices=["viewer", "researcher", "admin"], required=True
    )
    args = parser.parse_args()
    if args.command != "serve":
        data_root = os.environ.get("ABDUCER_DATA_ROOT")
        if not data_root:
            parser.error("ABDUCER_DATA_ROOT is required")
        store = Store(Path(data_root) / "service.sqlite3")
        if args.command == "provision-user":
            store.provision_user(args.subject, args.name, not args.disabled)
            print("Account provisioning updated")
        else:
            store.grant_project(args.subject, args.project_id, args.role)
            print("Project membership updated")
        return
    import uvicorn

    uvicorn.run(
        create_app(Config.from_env()), host=args.host, port=args.port, access_log=False
    )


if __name__ == "__main__":
    main()
