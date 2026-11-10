# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Durable named-user project state and transactionally queued research jobs.

SQLite transactions serialize admission and publication. A lost worker lease
fails the job rather than repeating potentially billable scientific work.
Only a verified successful result advances the project's committed checkpoint.
"""

from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import time
import uuid


class AccessDenied(ValueError):
    """Do not distinguish unknown objects from objects belonging to others."""


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


class Store:
    def __init__(self, db_path: Path | str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with self.connection() as db:
            db.executescript("""
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS users(subject TEXT PRIMARY KEY, name TEXT NOT NULL, active INTEGER NOT NULL DEFAULT 1);
                CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, name TEXT NOT NULL, version INTEGER NOT NULL DEFAULT 0, checkpoint TEXT);
                CREATE TABLE IF NOT EXISTS members(project_id TEXT NOT NULL REFERENCES projects(id), subject TEXT NOT NULL REFERENCES users(subject), role TEXT NOT NULL, PRIMARY KEY(project_id, subject));
                CREATE TABLE IF NOT EXISTS plans(id TEXT PRIMARY KEY, project_id TEXT NOT NULL, subject TEXT NOT NULL, payload TEXT NOT NULL, expires REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY, project_id TEXT NOT NULL, subject TEXT NOT NULL, plan_id TEXT NOT NULL UNIQUE, idempotency_key TEXT NOT NULL, status TEXT NOT NULL, payload TEXT NOT NULL, created REAL NOT NULL, updated REAL NOT NULL, worker_id TEXT, lease_until REAL, cancel_requested INTEGER NOT NULL DEFAULT 0, result TEXT, error TEXT, UNIQUE(subject,idempotency_key));
                CREATE TABLE IF NOT EXISTS artifacts(job_id TEXT NOT NULL REFERENCES jobs(id), id TEXT NOT NULL, payload TEXT NOT NULL, PRIMARY KEY(job_id,id));
                CREATE INDEX IF NOT EXISTS jobs_project ON jobs(project_id,created);
                CREATE TABLE IF NOT EXISTS worker_presence(worker_id TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL, provider TEXT NOT NULL, provider_ready INTEGER NOT NULL, hooks_enabled INTEGER NOT NULL, seen REAL NOT NULL);
            """)
        self.path.chmod(0o600)

    @contextmanager
    def connection(self, *, write=False):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            if write:
                db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    def provision_user(self, subject: str, name: str, active: bool = True):
        if not subject or len(subject) > 512 or not name or len(name) > 200:
            raise ValueError("A bounded stable subject and display name are required")
        with self.connection(write=True) as db:
            db.execute(
                "INSERT INTO users VALUES(?,?,?) ON CONFLICT(subject) DO UPDATE SET name=excluded.name,active=excluded.active",
                (subject, name, int(active)),
            )

    def record_worker(
        self, worker_id, source_sha256, provider, *, provider_ready, hooks_enabled
    ):
        """Advertise a live worker without mistaking configuration for liveness."""
        with self.connection(write=True) as db:
            db.execute(
                "INSERT INTO worker_presence VALUES(?,?,?,?,?,?) ON CONFLICT(worker_id) DO UPDATE SET source_sha256=excluded.source_sha256,provider=excluded.provider,provider_ready=excluded.provider_ready,hooks_enabled=excluded.hooks_enabled,seen=excluded.seen",
                (
                    worker_id,
                    source_sha256,
                    provider,
                    int(provider_ready),
                    int(hooks_enabled),
                    time.time(),
                ),
            )

    def worker_presence(self, source_sha256, *, max_age=45):
        """Read only recent workers running the exact prepared source release."""
        with self.connection() as db:
            return [
                dict(row)
                for row in db.execute(
                    "SELECT provider,provider_ready,hooks_enabled,seen FROM worker_presence WHERE source_sha256=? AND seen>=? ORDER BY seen DESC",
                    (source_sha256, time.time() - max_age),
                )
            ]

    def _user(self, db, subject):
        row = db.execute(
            "SELECT * FROM users WHERE subject=? AND active=1", (subject,)
        ).fetchone()
        if row is None:
            raise AccessDenied("Account is not provisioned or is disabled")
        return dict(row)

    def profile(self, subject: str):
        with self.connection() as db:
            user = self._user(db, subject)
        return {"id": user["subject"], "name": user["name"]}

    def _project(self, db, subject, project_id, write=False):
        self._user(db, subject)
        row = db.execute(
            "SELECT p.*,m.role FROM projects p JOIN members m ON p.id=m.project_id WHERE p.id=? AND m.subject=?",
            (project_id, subject),
        ).fetchone()
        if row is None or (write and row["role"] not in {"researcher", "admin"}):
            raise AccessDenied("Project is unavailable or operation is not permitted")
        result = dict(row)
        result["checkpoint"] = (
            json.loads(result["checkpoint"]) if result["checkpoint"] else None
        )
        return result

    def project(self, subject, project_id, *, write=False):
        with self.connection() as db:
            return self._project(db, subject, project_id, write)

    def create_project(self, subject, name):
        if not isinstance(name, str) or not name.strip() or len(name) > 200:
            raise ValueError("Project name must contain 1–200 characters")
        identity = uuid.uuid4().hex
        with self.connection(write=True) as db:
            self._user(db, subject)
            db.execute(
                "INSERT INTO projects(id,name) VALUES(?,?)", (identity, name.strip())
            )
            db.execute(
                "INSERT INTO members VALUES(?,?,?)", (identity, subject, "admin")
            )
        return self.project(subject, identity)

    def grant_project(self, subject, project_id, role):
        """Operator-only provisioning; this method is deliberately not an MCP tool."""
        if role not in {"viewer", "researcher", "admin"}:
            raise ValueError("Unknown project role")
        with self.connection(write=True) as db:
            self._user(db, subject)
            db.execute(
                "INSERT INTO members VALUES(?,?,?) ON CONFLICT(project_id,subject) DO UPDATE SET role=excluded.role",
                (project_id, subject, role),
            )

    def list_projects(self, subject):
        with self.connection() as db:
            self._user(db, subject)
            return [
                dict(r)
                for r in db.execute(
                    "SELECT p.id,p.name,p.version,m.role FROM projects p JOIN members m ON p.id=m.project_id WHERE m.subject=? ORDER BY p.name,p.id",
                    (subject,),
                )
            ]

    def prepare_plan(
        self,
        subject,
        project_id,
        *,
        workflow_id,
        inputs,
        budget,
        release,
        contract_workflow_id=None,
        runtime_source_sha256=None,
        ttl_seconds=900,
    ):
        payload = {
            "workflow_id": workflow_id,
            "contract_workflow_id": contract_workflow_id or workflow_id,
            "inputs": inputs,
            "budget": budget,
            "release": release,
            "runtime_source_sha256": runtime_source_sha256,
        }
        with self.connection(write=True) as db:
            project = self._project(db, subject, project_id, True)
            payload.update(
                parent_version=project["version"],
                parent_checkpoint=project["checkpoint"],
            )
            plan_id = uuid.uuid4().hex
            expires = time.time() + ttl_seconds
            db.execute(
                "INSERT INTO plans VALUES(?,?,?,?,?)",
                (plan_id, project_id, subject, _json(payload), expires),
            )
        return {
            "plan_id": plan_id,
            "project_id": project_id,
            "expires_at": expires,
            **payload,
        }

    def start_job(
        self,
        subject,
        plan_id,
        idempotency_key,
        *,
        release,
        runtime_source_sha256=None,
        max_active_jobs=2,
    ):
        if not isinstance(idempotency_key, str) or not 1 <= len(idempotency_key) <= 128:
            raise ValueError("Idempotency key must contain 1–128 characters")
        with self.connection(write=True) as db:
            self._user(db, subject)
            existing = db.execute(
                "SELECT * FROM jobs WHERE subject=? AND idempotency_key=?",
                (subject, idempotency_key),
            ).fetchone()
            if existing:
                self._project(db, subject, existing["project_id"], True)
                if existing["plan_id"] != plan_id:
                    raise ValueError("Idempotency key already belongs to another plan")
                return self._job_dict(existing)
            plan = db.execute(
                "SELECT * FROM plans WHERE id=? AND subject=?", (plan_id, subject)
            ).fetchone()
            if not plan:
                raise AccessDenied("Plan is unavailable")
            project = self._project(db, subject, plan["project_id"], True)
            payload = json.loads(plan["payload"])
            if (
                plan["expires"] <= time.time()
                or payload["release"] != release
                or payload.get("runtime_source_sha256") != runtime_source_sha256
                or payload["parent_version"] != project["version"]
            ):
                raise ValueError("Plan is expired or stale; prepare a new plan")
            if db.execute("SELECT 1 FROM jobs WHERE plan_id=?", (plan_id,)).fetchone():
                raise ValueError("Plan has already been started")
            if db.execute(
                "SELECT 1 FROM jobs WHERE project_id=? AND status IN ('queued','running')",
                (plan["project_id"],),
            ).fetchone():
                raise ValueError("Project already has active research")
            active = db.execute(
                "SELECT count(*) FROM jobs WHERE subject=? AND status IN ('queued','running')",
                (subject,),
            ).fetchone()[0]
            if active >= max_active_jobs:
                raise ValueError("Account active-job limit reached")
            identity, now = uuid.uuid4().hex, time.time()
            db.execute(
                "INSERT INTO jobs(id,project_id,subject,plan_id,idempotency_key,status,payload,created,updated) VALUES(?,?,?,?,?,'queued',?,?,?)",
                (
                    identity,
                    plan["project_id"],
                    subject,
                    plan_id,
                    idempotency_key,
                    plan["payload"],
                    now,
                    now,
                ),
            )
            return self._job_dict(
                db.execute("SELECT * FROM jobs WHERE id=?", (identity,)).fetchone()
            )

    def _job_dict(self, row):
        result = dict(row)
        result.update(json.loads(result.pop("payload")))
        result["job_id"] = result["id"]
        result["result"] = json.loads(result["result"]) if result["result"] else None
        result["cancel_requested"] = bool(result["cancel_requested"])
        return result

    def get_job(self, subject, job_id):
        with self.connection() as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if not row:
                raise AccessDenied("Run is unavailable")
            self._project(db, subject, row["project_id"])
            return self._job_dict(row)

    def list_runs(self, subject, project_id, limit=50):
        if not 1 <= limit <= 100:
            raise ValueError("Limit must be 1–100")
        with self.connection() as db:
            self._project(db, subject, project_id)
            return [
                self._job_dict(row)
                for row in db.execute(
                    "SELECT * FROM jobs WHERE project_id=? ORDER BY created DESC LIMIT ?",
                    (project_id, limit),
                )
            ]

    def cancel_job(self, subject, job_id):
        with self.connection(write=True) as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if not row:
                raise AccessDenied("Run is unavailable")
            self._project(db, subject, row["project_id"], True)
            if row["status"] in {"queued", "running"}:
                db.execute(
                    "UPDATE jobs SET cancel_requested=1,status=CASE WHEN status='queued' THEN 'cancelled' ELSE status END,updated=? WHERE id=?",
                    (time.time(), job_id),
                )
        return self.get_job(subject, job_id)

    def claim_job(self, worker_id, lease_seconds=120, *, capabilities=None):
        now = time.time()
        with self.connection(write=True) as db:
            # Expired work is not automatically retried: its provider call may
            # have completed even though the host did not receive the result.
            db.execute(
                "UPDATE jobs SET status=CASE WHEN cancel_requested=1 THEN 'cancelled' ELSE 'failed' END,error='Worker lease expired; no automatic replay',updated=? WHERE status='running' AND lease_until<?",
                (now, now),
            )
            for row in db.execute(
                "SELECT * FROM jobs WHERE status='queued' ORDER BY created"
            ).fetchall():
                try:
                    project = self._project(db, row["subject"], row["project_id"], True)
                    payload = json.loads(row["payload"])
                    # Ineligible workers leave a bound job queued for a compatible
                    # peer. They must not consume it and later fail it, or run it
                    # with weaker hooks/a different model provider.
                    required = payload.get("inputs", {})
                    if required.get("native_hooks_required"):
                        profile = capabilities or {}
                        if (
                            profile.get("source_sha256")
                            != payload.get("runtime_source_sha256")
                            or profile.get("provider") != required.get("model_provider")
                            or profile.get("provider_ready") is not True
                            or profile.get("hooks_enabled") is not True
                        ):
                            continue
                    if project["version"] != payload["parent_version"]:
                        raise ValueError("Parent research state changed")
                except ValueError:
                    db.execute(
                        "UPDATE jobs SET status='failed',error='Authorization or state changed before execution',updated=? WHERE id=?",
                        (now, row["id"]),
                    )
                    continue
                db.execute(
                    "UPDATE jobs SET status='running',worker_id=?,lease_until=?,updated=? WHERE id=?",
                    (worker_id, now + lease_seconds, now, row["id"]),
                )
                return self._job_dict(
                    db.execute("SELECT * FROM jobs WHERE id=?", (row["id"],)).fetchone()
                )
        return None

    def heartbeat(self, job_id, worker_id, lease_seconds=120):
        with self.connection(write=True) as db:
            row = db.execute(
                "SELECT * FROM jobs WHERE id=? AND worker_id=? AND status='running' AND lease_until>=?",
                (job_id, worker_id, time.time()),
            ).fetchone()
            if not row or row["cancel_requested"]:
                return False
            try:
                self._project(db, row["subject"], row["project_id"], True)
            except AccessDenied:
                db.execute("UPDATE jobs SET cancel_requested=1 WHERE id=?", (job_id,))
                return False
            db.execute(
                "UPDATE jobs SET lease_until=?,updated=? WHERE id=?",
                (time.time() + lease_seconds, time.time(), job_id),
            )
            return True

    def cancellation_requested(self, job_id, worker_id):
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM jobs WHERE id=? AND worker_id=?", (job_id, worker_id)
            ).fetchone()
            return (
                not row
                or row["status"] != "running"
                or bool(row["cancel_requested"])
                or row["lease_until"] < time.time()
            )

    def finish_job(
        self,
        job_id,
        worker_id,
        result,
        artifacts,
        checkpoint=None,
        *,
        deadline_monotonic=None,
    ):
        with self.connection(write=True) as db:
            # Lock acquisition can wait: the worker's preceding check alone
            # cannot authorize publication after the approved deadline.
            if (
                deadline_monotonic is not None
                and time.monotonic() >= deadline_monotonic
            ):
                raise TimeoutError("Research deadline exceeded before publication")
            row = db.execute(
                "SELECT * FROM jobs WHERE id=? AND worker_id=? AND status='running' AND lease_until>=?",
                (job_id, worker_id, time.time()),
            ).fetchone()
            if not row:
                raise ValueError("Worker no longer owns the active job lease")
            if row["cancel_requested"]:
                db.execute(
                    "UPDATE jobs SET status='cancelled',updated=? WHERE id=?",
                    (time.time(), job_id),
                )
                return
            project = self._project(db, row["subject"], row["project_id"], True)
            if project["version"] != json.loads(row["payload"])["parent_version"]:
                raise ValueError("Parent research state changed before publication")
            for artifact in artifacts:
                db.execute(
                    "INSERT INTO artifacts VALUES(?,?,?)",
                    (job_id, artifact["id"], _json(artifact)),
                )
            db.execute(
                "UPDATE jobs SET status='succeeded',result=?,updated=? WHERE id=?",
                (_json(result), time.time(), job_id),
            )
            db.execute(
                "UPDATE projects SET version=version+1,checkpoint=? WHERE id=?",
                (
                    _json(checkpoint) if checkpoint is not None else None,
                    row["project_id"],
                ),
            )
            if (
                deadline_monotonic is not None
                and time.monotonic() >= deadline_monotonic
            ):
                raise TimeoutError("Research deadline exceeded during publication")

    def fail_job(self, job_id, worker_id, error):
        with self.connection(write=True) as db:
            db.execute(
                "UPDATE jobs SET status=CASE WHEN cancel_requested=1 THEN 'cancelled' ELSE 'failed' END,error=?,updated=? WHERE id=? AND worker_id=? AND status='running'",
                (str(error)[:2000], time.time(), job_id, worker_id),
            )

    def artifacts(self, subject, job_id):
        self.get_job(subject, job_id)
        with self.connection() as db:
            return [
                json.loads(row[0])
                for row in db.execute(
                    "SELECT payload FROM artifacts WHERE job_id=? ORDER BY id",
                    (job_id,),
                )
            ]
