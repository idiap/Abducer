# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Portable read-only asset snapshots for source-owned MCP integrations.

This module is copied into each participating server so it has no Lunar runtime
dependency. Native registries select workflows and provenance; canonical skill
registries select instructions. Scripts are bytes to inspect, never imports.
"""

import base64
import hashlib
import json
import mimetypes
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}


class AssetCatalog:
    """Freeze a declared closure and serve only those immutable bytes."""

    def __init__(
        self, root, *, skills, workflows, contracts=(), source_files=(), schema_files=()
    ):
        self.root = Path(root).resolve()
        self.assets = {}
        self.kinds = {}
        self._schemas = set()
        for skill in sorted(skills, key=str):
            path = self.relative(skill)
            self.add(path, "skill")
            self.directory(self.root / path.parent, frozenset())
        for workflow in sorted(workflows, key=str):
            self.add(self.relative(workflow), "workflow")
        for descriptor_path, contract in contracts:
            base = self.root / self.relative(descriptor_path).parent
            for definition in contract["types"].values():
                reference = definition["schema"]
                if isinstance(reference, str):
                    self.schema(self.reference(base, reference))
            for source in contract["provenance"]["sources"]:
                self.add(self.relative(source["path"]))
        for path in source_files:
            self.add(self.relative(path))
        for path in schema_files:
            self.schema(self.root / self.relative(path))
        self.entries = [
            {
                "path": path,
                "kind": self.kinds[path],
                "sha256": self.assets[path]["sha256"],
            }
            for path in sorted(self.assets)
        ]

    def relative(self, value):
        path = Path(value)
        if path.is_absolute():
            try:
                path = path.relative_to(self.root)
            except ValueError:
                raise ValueError("Asset is outside the source repository") from None
        logical = PurePosixPath(path.as_posix())
        if (
            not logical.parts
            or any(part in {".", ".."} for part in logical.parts)
            or "\\" in str(value)
            or "\0" in str(value)
        ):
            raise ValueError("Asset paths must be repository-relative and normalized")
        # Check the original spelling as pathlib normalizes './' and duplicate '/'.
        if not Path(value).is_absolute() and logical.as_posix() != str(value):
            raise ValueError("Asset paths must be normalized")
        target = self.root / logical
        if not target.resolve().is_relative_to(self.root):
            raise ValueError("Asset symlink escapes the source repository")
        physical = target.resolve().relative_to(self.root)
        if any(
            part in IGNORED_DIRECTORIES for part in (*logical.parts, *physical.parts)
        ):
            raise ValueError("Generated environments and caches are not source assets")
        return logical

    def add(self, path, kind="asset"):
        logical = self.relative(path)
        key = logical.as_posix()
        if key in self.assets:
            if kind != "asset":
                if self.kinds[key] not in {kind, "asset"}:
                    raise ValueError("Conflicting source asset kinds")
                self.kinds[key] = kind
            return
        target = self.root / logical
        for name in (logical.name.lower(), target.resolve().name.lower()):
            if (
                name.startswith(".env")
                or name in {"credentials.json", "id_rsa", "id_ed25519"}
                or name.endswith(
                    (
                        ".pem",
                        ".key",
                        ".p12",
                        ".pfx",
                        ".keystore",
                        ".local.toml",
                        ".local.yaml",
                        ".local.yml",
                        ".local.json",
                    )
                )
            ):
                raise ValueError(
                    "Credential or private configuration files cannot be exported as skill assets"
                )
        if not target.is_file():
            raise ValueError("Declared source asset is missing: " + key)
        payload = target.read_bytes()
        try:
            content, encoding = payload.decode("utf-8"), "text"
        except UnicodeDecodeError:
            content, encoding = base64.b64encode(payload).decode("ascii"), "base64"
        self.assets[key] = {
            "path": key,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "content": content,
            "encoding": encoding,
            "media_type": mimetypes.guess_type(key)[0] or "application/octet-stream",
        }
        self.kinds[key] = kind

    def directory(self, directory, ancestors):
        resolved = directory.resolve()
        if not resolved.is_relative_to(self.root):
            raise ValueError("Skill resource directory escapes the source repository")
        if resolved in ancestors:
            raise ValueError("Skill resource symlink cycle")
        for child in sorted(directory.iterdir()):
            if child.name in IGNORED_DIRECTORIES:
                continue
            if child.is_dir():
                self.directory(child, ancestors | {resolved})
            elif child.is_file():
                self.add(self.relative(child))

    def reference(self, base, reference):
        uri = urlsplit(reference)
        if (
            uri.scheme
            or uri.netloc
            or uri.query
            or Path(unquote(uri.path)).is_absolute()
        ):
            raise ValueError("Only local relative schema references can be exported")
        target = (base / unquote(uri.path)).resolve()
        if not target.is_relative_to(self.root):
            raise ValueError("Payload schema reference escapes the source repository")
        return target

    def schema(self, path):
        logical = self.relative(path)
        key = logical.as_posix()
        if key in self._schemas:
            return
        self._schemas.add(key)
        self.add(logical)
        raw = json.loads(self.assets[key]["content"])

        def walk(value):
            if isinstance(value, dict):
                if "$ref" in value and not value["$ref"].startswith("#"):
                    self.schema(
                        self.reference((self.root / logical).parent, value["$ref"])
                    )
                for item in value.values():
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(raw)

    def list(self, cursor=None):
        if cursor is not None and (
            not isinstance(cursor, str) or not cursor.isdecimal()
        ):
            raise ValueError("Invalid asset manifest cursor")
        index = int(cursor) if cursor else 0
        if not 0 <= index <= len(self.entries):
            raise ValueError("Asset manifest cursor is outside the snapshot")
        page = self.entries[index : index + 100]
        next_index = index + len(page)
        return {
            "schema_version": "agent-skills.mcp-assets/v1",
            "entries": page,
            "next_cursor": str(next_index) if next_index < len(self.entries) else None,
        }

    def read(self, path):
        if not isinstance(path, str) or Path(path).is_absolute():
            raise ValueError("Asset reads require a declared repository-relative path")
        key = self.relative(path).as_posix()
        if key not in self.assets:
            raise ValueError("Asset is not declared in this source snapshot")
        return dict(self.assets[key])
