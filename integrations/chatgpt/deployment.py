# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
# SPDX-License-Identifier: MIT
"""Build a confined container context from the declared research source snapshot.

Never send the developer checkout to Docker. The worker's source selector omits
credentials, local configuration and unselected runs, then records exact hashes.
The resulting context is inspectable before any image build or deployment.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import tempfile


def build_context(source_root: Path, output: Path) -> dict:
    """Publish a fresh context atomically, leaving existing output untouched."""
    from .runtime import build_snapshot

    source_root = source_root.resolve(strict=True)
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ValueError("Build context output must not already exist")
    if output.resolve().is_relative_to(source_root):
        raise ValueError("Build context must be outside the source checkout")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".abducer-context-", dir=output.parent))
    try:
        manifest = build_snapshot(source_root, staging / "source")
        deploy = source_root / "integrations/chatgpt/deploy"
        for name in ("Dockerfile", "compose.yaml", ".env.example"):
            shutil.copyfile(deploy / name, staging / name)
        (staging / ".dockerignore").write_text(
            ".env\n*.key\n*.pem\n__pycache__\n", encoding="utf-8"
        )
        staging.rename(output)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return {"context": str(output), "source_manifest": manifest}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build_context(args.source_root, args.output)
    # Avoid dumping the complete source inventory into routine operator logs.
    print(json.dumps({"context": result["context"], "status": "prepared"}))


if __name__ == "__main__":
    main()
