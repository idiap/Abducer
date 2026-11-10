#!/usr/bin/env python3
"""Install the exported Yang--Mills skills without overwriting divergent data."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path


BUNDLE_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = BUNDLE_ROOT / ".agents" / "skills"


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def destination(args: argparse.Namespace) -> Path:
    if args.scope == "user":
        if args.repo is not None:
            raise ValueError("--repo is only valid with --scope repo")
        return Path.home() / ".agents" / "skills"
    repo = (args.repo or Path.cwd()).expanduser().resolve()
    return repo / ".agents" / "skills"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("repo", "user"), default="repo")
    parser.add_argument("--repo", type=Path, help="repository root for repo scope")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not SOURCE_ROOT.is_dir():
        print(f"missing bundled skill root: {SOURCE_ROOT}", file=sys.stderr)
        return 2

    try:
        target_root = destination(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    sources = sorted(p for p in SOURCE_ROOT.iterdir() if p.is_dir())
    conflicts: list[str] = []
    unchanged: list[str] = []
    pending: list[tuple[Path, Path]] = []

    for source in sources:
        target = target_root / source.name
        if target.exists():
            if target.is_dir() and tree_digest(source) == tree_digest(target):
                unchanged.append(source.name)
            else:
                conflicts.append(source.name)
        else:
            pending.append((source, target))

    print(f"source skills: {len(sources)}")
    print(f"destination: {target_root}")
    print(f"unchanged: {len(unchanged)}; new: {len(pending)}; conflicts: {len(conflicts)}")
    if conflicts:
        print("refusing to overwrite divergent directories:", file=sys.stderr)
        for name in conflicts:
            print(f"  {name}", file=sys.stderr)
        return 3

    if args.dry_run:
        for _, target in pending:
            print(f"would install {target.name}")
        return 0

    target_root.mkdir(parents=True, exist_ok=True)
    for source, target in pending:
        shutil.copytree(source, target)
        if tree_digest(source) != tree_digest(target):
            print(f"post-copy verification failed: {target}", file=sys.stderr)
            return 4
        print(f"installed {target.name}")

    print("installation verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

