#!/usr/bin/env python3
"""Create a modular LaTeX paper from the bundled template."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / "assets" / "paper_template"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--author", default="Anonymous")
    parser.add_argument("--date", default="")
    args = parser.parse_args()

    output = args.output_dir.resolve()
    if output.exists():
        print(f"refusing to overwrite existing path: {output}", file=sys.stderr)
        return 2
    if not TEMPLATE.is_dir():
        print(f"missing bundled template: {TEMPLATE}", file=sys.stderr)
        return 3

    shutil.copytree(TEMPLATE, output)
    main_tex = output / "main.tex"
    text = main_tex.read_text(encoding="utf-8")
    replacements = {
        "@@TITLE@@": args.title,
        "@@AUTHOR@@": args.author,
        "@@DATE@@": args.date,
    }
    for token, value in replacements.items():
        text = text.replace(token, value)
    main_tex.write_text(text, encoding="utf-8")
    (output / "build").mkdir()
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
