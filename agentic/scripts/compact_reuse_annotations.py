# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Compact ordered REUSE annotations without changing per-path metadata.

Only generalize one path component at a time, below a named top-level directory.
Later attribution exceptions remain authoritative. Every transformation must
preserve the winning annotation for all known paths, including literal entries
for files that are temporarily absent. Future files inherit the compact rules.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import tomllib

from reuse.global_licensing import AnnotationsItem


def signature(row: dict) -> str:
    """Compare metadata as sets, independent of TOML scalar/list spelling."""
    fields = {
        key: sorted(set(value if isinstance(value, list) else [value]))
        for key, value in row.items()
        if key != "path"
    }
    fields.setdefault("precedence", ["closest"])
    return json.dumps(fields, sort_keys=True, ensure_ascii=False)


def known_paths(root: Path) -> list[str]:
    """Include tracked files and visible additions, without inspecting secrets."""
    raw = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
    )
    return sorted({p.decode("utf-8") for p in raw.split(b"\0") if p})


def compact_annotations(rows: list[dict], paths: list[str]) -> list[dict]:
    """Merge equivalent tables and wildcard paths only after equivalence checks."""
    rows = copy.deepcopy(rows)
    for row in rows:
        value = row["path"]
        row["path"] = sorted(set(value if isinstance(value, list) else [value]))
    initial_size = (len(rows), sum(len(row["path"]) for row in rows))
    probes = set()
    for row in rows:
        for pattern in row["path"]:
            # Keep directory defaults meaningful for future files, even when
            # every current child happens to have a narrower exception.
            for recursive in ("__reuse_future_file__", "__reuse_future_dir__/file"):
                probes.add(
                    pattern.replace("**", recursive).replace("*", "__reuse_future__")
                )
    universe = sorted(set(paths) | probes)
    masks: dict[str, int] = {}

    def mask(pattern: str) -> int:
        if pattern not in masks:
            matcher = AnnotationsItem(paths={pattern})
            bits = 0
            for i, path in enumerate(universe):
                if matcher.matches(path):
                    bits |= 1 << i
            masks[pattern] = bits
        return masks[pattern]

    def effective(candidate: list[dict]) -> dict[str, int]:
        """Encode the last matching table's complete metadata for each path."""
        seen = 0
        result: dict[str, int] = {}
        for row in reversed(candidate):
            matched = 0
            for pattern in row["path"]:
                matched |= mask(pattern)
            owned = matched & ~seen
            if owned:
                key = signature(row)
                result[key] = result.get(key, 0) | owned
            seen |= matched
        return result

    original = effective(rows)

    def accept(candidate: list[dict]) -> bool:
        return effective(candidate) == original

    # Combining tables can cross intervening rules only if their final per-file
    # attribution stays identical. Try both positions to retain narrow overrides.
    changed = True
    while changed:
        changed = False
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                if signature(rows[i]) != signature(rows[j]):
                    continue
                for target, removed in ((i, j), (j, i)):
                    candidate = copy.deepcopy(rows)
                    candidate[target]["path"] = sorted(
                        set(rows[i]["path"]) | set(rows[j]["path"])
                    )
                    del candidate[removed]
                    if accept(candidate):
                        rows = candidate
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break

    for i in range(len(rows)):
        while True:
            groups: dict[str, set[str]] = {}
            for pattern in rows[i]["path"]:
                parts = pattern.split("/")
                for position in range(1, len(parts)):
                    # Do not generalize across directory depths or replace an
                    # existing wildcard; recursive ** remains explicit.
                    if "*" in parts[position]:
                        continue
                    replacements = ["*"] if position < len(parts) - 1 else []
                    if "-" in parts[position]:
                        replacements.append(parts[position].split("-", 1)[0] + "-*")
                    for replacement in replacements:
                        wildcard = parts.copy()
                        wildcard[position] = replacement
                        groups.setdefault("/".join(wildcard), set()).add(pattern)
            options = sorted(
                (
                    (pattern, members)
                    for pattern, members in groups.items()
                    if len(members) > 1
                ),
                key=lambda item: (
                    -(sum(len(p) for p in item[1]) - len(item[0])),
                    item[0],
                ),
            )
            for pattern, members in options:
                candidate = copy.deepcopy(rows)
                candidate[i]["path"] = sorted(
                    (set(rows[i]["path"]) - members) | {pattern}
                )
                if accept(candidate):
                    rows = candidate
                    break
            else:
                break

    # Broader defaults may make individual paths or entire tables redundant.
    for i in reversed(range(len(rows))):
        for pattern in list(rows[i]["path"]):
            candidate = copy.deepcopy(rows)
            candidate[i]["path"].remove(pattern)
            if accept(candidate):
                rows = candidate
    rows = [row for row in rows if row["path"]]
    assert effective(rows) == original
    if (len(rows), sum(len(row["path"]) for row in rows)) != initial_size:
        return compact_annotations(rows, universe)
    return rows


def render_annotations(rows: list[dict]) -> str:
    """Render deterministically without changing metadata values or precedence."""
    lines = []
    for row in rows:
        lines.extend(["[[annotations]]", "path = ["])
        lines.extend(f"  {json.dumps(p, ensure_ascii=False)}," for p in row["path"])
        lines.extend(["]", f'precedence = "{row.get("precedence", "closest")}"'])
        for key in sorted(row.keys() - {"path", "precedence"}):
            value = row[key]
            if isinstance(value, list):
                value = sorted(set(value))
            lines.append(f"{json.dumps(key)} = {json.dumps(value, ensure_ascii=False)}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.repository_root.resolve()
    target = root / "REUSE.toml"
    source = target.read_text()
    rows = compact_annotations(tomllib.loads(source)["annotations"], known_paths(root))
    preamble = source.split("[[annotations]]", 1)[0]
    compacted = preamble + render_annotations(rows)
    if args.check:
        if compacted != source:
            print("REUSE.toml can be compacted")
            return 1
    else:
        target.write_text(compacted)
    print(f"{'Checked' if args.check else 'Compacted'} {len(rows)} annotation tables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
