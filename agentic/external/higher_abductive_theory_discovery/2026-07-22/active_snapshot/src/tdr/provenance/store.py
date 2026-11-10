"""Immutable content-addressed artifacts and a transactional SQLite index."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import sqlite3
from typing import Any, Iterator

from tdr.domain.models import canonical_json, jsonable, utc_now


class ArtifactStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def put_bytes(self, data: bytes, suffix: str = ".bin") -> str:
        digest = hashlib.sha256(data).hexdigest()
        path = self.root / digest[:2] / f"{digest}{suffix}"
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_bytes(data)
        elif path.read_bytes() != data:
            raise IOError("content-address collision or corrupted artifact")
        return digest

    def put_json(self, value: Any) -> str:
        return self.put_bytes(canonical_json(value).encode("utf-8"), ".json")

    def get_bytes(self, digest: str) -> bytes:
        candidates = list((self.root / digest[:2]).glob(f"{digest}.*"))
        if len(candidates) != 1:
            raise FileNotFoundError(digest)
        data = candidates[0].read_bytes()
        if hashlib.sha256(data).hexdigest() != digest:
            raise IOError(f"artifact checksum mismatch: {digest}")
        return data

    def get_json(self, digest: str) -> Any:
        return json.loads(self.get_bytes(digest).decode("utf-8"))


class Repository:
    def __init__(self, project_dir: str | Path):
        self.project_dir = Path(project_dir)
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.artifacts = ArtifactStore(self.project_dir / "artifacts")
        self.db_path = self.project_dir / "tdr.sqlite3"
        self._initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connection() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS records (
                  record_id TEXT PRIMARY KEY,
                  record_type TEXT NOT NULL,
                  lifecycle TEXT NOT NULL,
                  schema_version TEXT NOT NULL,
                  artifact_hash TEXT NOT NULL,
                  parent_ids_json TEXT NOT NULL,
                  created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS records_type_idx ON records(record_type);
                CREATE TABLE IF NOT EXISTS runs (
                  run_id TEXT PRIMARY KEY,
                  context_id TEXT NOT NULL,
                  phase TEXT NOT NULL,
                  revision INTEGER NOT NULL,
                  state_hash TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS events (
                  event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  run_id TEXT NOT NULL,
                  sequence INTEGER NOT NULL,
                  skill_name TEXT NOT NULL,
                  input_hash TEXT NOT NULL,
                  result_hash TEXT NOT NULL,
                  role TEXT NOT NULL,
                  created_at TEXT NOT NULL,
                  UNIQUE(run_id, sequence)
                );
                """
            )

    def save_record(self, value: Any, record_type: str, *, parent_ids: list[str] | None = None) -> str:
        data = jsonable(value)
        record_id = str(data.get("record_id") or data.get(f"{record_type}_id") or data.get("candidate_id") or data.get("validation_id"))
        if not record_id or record_id == "None":
            raise ValueError("record has no stable identifier")
        digest = self.artifacts.put_json(data)
        with self.connection() as db:
            db.execute(
                "INSERT OR IGNORE INTO records VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    record_id,
                    record_type,
                    str(data.get("lifecycle", "staged")),
                    str(data.get("schema_version", "1.0")),
                    digest,
                    json.dumps(parent_ids or []),
                    utc_now(),
                ),
            )
        return digest

    def get_record(self, record_id: str) -> dict[str, Any]:
        with self.connection() as db:
            row = db.execute("SELECT artifact_hash FROM records WHERE record_id = ?", (record_id,)).fetchone()
        if row is None:
            raise KeyError(record_id)
        return self.artifacts.get_json(row["artifact_hash"])

    def list_records(self, record_type: str | None = None) -> list[dict[str, Any]]:
        query = "SELECT * FROM records"
        args: tuple[Any, ...] = ()
        if record_type:
            query += " WHERE record_type = ?"
            args = (record_type,)
        query += " ORDER BY created_at, record_id"
        with self.connection() as db:
            rows = db.execute(query, args).fetchall()
        return [dict(row) for row in rows]

    def save_run(self, state: Any) -> str:
        data = jsonable(state)
        digest = self.artifacts.put_json(data)
        with self.connection() as db:
            db.execute(
                """INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?)
                   ON CONFLICT(run_id) DO UPDATE SET phase=excluded.phase,
                   revision=excluded.revision, state_hash=excluded.state_hash,
                   updated_at=excluded.updated_at""",
                (data["run_id"], data["context_id"], data["phase"], data["revision"], digest, utc_now()),
            )
        return digest

    def load_run(self, run_id: str) -> dict[str, Any]:
        with self.connection() as db:
            row = db.execute("SELECT state_hash FROM runs WHERE run_id = ?", (run_id,)).fetchone()
        if row is None:
            raise KeyError(run_id)
        return self.artifacts.get_json(row["state_hash"])

    def append_event(self, run_id: str, skill_name: str, role: str, inputs: Any, result: Any) -> dict[str, Any]:
        input_hash = self.artifacts.put_json(inputs)
        result_hash = self.artifacts.put_json(result)
        with self.connection() as db:
            row = db.execute("SELECT COALESCE(MAX(sequence), 0) + 1 AS next FROM events WHERE run_id = ?", (run_id,)).fetchone()
            sequence = int(row["next"])
            db.execute(
                "INSERT INTO events(run_id, sequence, skill_name, input_hash, result_hash, role, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, sequence, skill_name, input_hash, result_hash, role, utc_now()),
            )
        return {"sequence": sequence, "input_hash": input_hash, "result_hash": result_hash}

    def run_events(self, run_id: str) -> list[dict[str, Any]]:
        with self.connection() as db:
            rows = db.execute("SELECT * FROM events WHERE run_id = ? ORDER BY sequence", (run_id,)).fetchall()
        return [dict(row) for row in rows]

