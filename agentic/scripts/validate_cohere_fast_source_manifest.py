#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Generate/check the immutable cohere-fast source intake records."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "agentic/imports/cohere_fast"
ARCHIVE = OUT / "source_archives/discover-main-repo.zip"
YM_PREFIX = "skills/programs/yang-mills/"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def classify(name: str) -> tuple[str, str]:
    p = PurePosixPath(name)
    parts = set(p.parts)
    if name.endswith("/"):
        return "archive", "directory entry"
    if ".git" in parts or ".github" in parts or ".githooks" in parts:
        return "reject", "source control and CI state is not product input"
    if parts & {"cases", "experiments", "outputs", "timed-runs", "__pycache__"}:
        return "reject", "generated or experimental state is excluded"
    if YM_PREFIX in name and name.endswith("/SKILL.md"):
        return "adapt", "procedure is critically rewritten into the isolated YM bundle"
    if name.startswith("tdr/") or "/tdr/" in name or "sqlite" in name.lower():
        return "reference-only", "standalone control-plane semantics are non-authoritative"
    if name.endswith((".py", ".sh", ".tex", ".sty")):
        return "reference-only", "executable or TeX material requires an explicit security review"
    return "archive", "not in the minimal v1 capability closure"


def records(archive: Path = ARCHIVE) -> tuple[dict, dict, dict]:
    if not archive.is_file():
        raise SystemExit(f"missing source archive: {archive}; supply --archive PATH")
    archive_bytes = archive.read_bytes()
    members = []
    source_skills = []
    with zipfile.ZipFile(archive) as zf:
        for info in sorted(zf.infolist(), key=lambda row: row.filename):
            disposition, rationale = classify(info.filename)
            member_digest = None if info.is_dir() else digest(zf.read(info))
            members.append({"path": info.filename, "sha256": member_digest,
                            "size": info.file_size, "disposition": disposition,
                            "rationale": rationale})
            if YM_PREFIX in info.filename and info.filename.endswith("/SKILL.md"):
                source_skills.append(PurePosixPath(info.filename).parent.name)
    current = {p.parent.name for p in (ROOT / "skills/yang_mills").glob("*/SKILL.md")}
    collisions = sorted(set(source_skills) & current)
    collision_rows = []
    for skill in sorted(source_skills):
        collision_rows.append({
            "source_skill": skill,
            "existing_path": f"skills/yang_mills/{skill}" if skill in current else None,
            "adapted_path": f"skills/domain_specific/ym/{skill}",
            "decision": "namespaced-fork" if skill in current else "adapt",
            "rationale": "preserve the existing global skill; use only after explicit cohere-fast ym activation"
                         if skill in current else "adapt source procedure into a domain-private typed contract",
        })
    manifest = {
        "schema_version": "1.0", "archive": str(archive.relative_to(ROOT) if archive.is_relative_to(ROOT) else archive),
        "archive_sha256": digest(archive_bytes), "source_date": "2026-08-05",
        "origin": "user-supplied discover-main-repo.zip",
        "license_status": "blocked-no-repository-license-detected",
        "license_decision": "No source text or executable is copied. Only independently rewritten procedures and factual member metadata are admitted until authorization is documented.",
        "member_count": len(members), "members": members,
    }
    dispositions = {
        "schema_version": "1.0", "archive_sha256": manifest["archive_sha256"],
        "policy": "minimal-v1-closure", "members": [
            {k: row[k] for k in ("path", "disposition", "rationale")} for row in members
        ],
        "counts": {kind: sum(r["disposition"] == kind for r in members)
                   for kind in ("adapt", "reference-only", "archive", "reject", "blocked")},
    }
    collision_report = {
        "schema_version": "1.0", "source_skill_count": len(source_skills),
        "collision_count": len(collisions), "collisions": collisions,
        "skills": collision_rows, "overwrite_count": 0,
    }
    return manifest, dispositions, collision_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--archive", type=Path, default=ARCHIVE,
                        help="Source ZIP (defaults to the repository-local source_archives directory).")
    args = parser.parse_args()
    payloads = dict(zip(("source_manifest.json", "dispositions.json", "collision_report.json"), records(args.archive)))
    if args.write:
        OUT.mkdir(parents=True, exist_ok=True)
        for name, payload in payloads.items():
            (OUT / name).write_text(json.dumps(payload, indent=2) + "\n")
    for name, expected in payloads.items():
        path = OUT / name
        if not path.is_file() or json.loads(path.read_text()) != expected:
            raise SystemExit(f"stale or missing {path}; run with --write")
    manifest = payloads["source_manifest.json"]
    if len(manifest["members"]) != manifest["member_count"]:
        raise SystemExit("member inventory is incomplete")
    if payloads["collision_report.json"]["overwrite_count"]:
        raise SystemExit("collisions may not overwrite existing skills")
    print(f"validated {manifest['member_count']} cohere-fast source members")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
