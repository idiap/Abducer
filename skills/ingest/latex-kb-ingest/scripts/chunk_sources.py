# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
# 
# SPDX-License-Identifier: MIT

"""Chunk web/local math sources into JSONL for downstream extraction.

Supported inputs:
- HTTP/HTTPS URLs (HTML -> text)
- Local text-like files (.txt, .md, .tex, .rst, .json, etc.)
- PDF files (.pdf) if pypdf or PyPDF2 is installed
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

_COMMON_DIR = Path(__file__).resolve().parents[3] / "common"
if str(_COMMON_DIR) not in sys.path:
    sys.path.insert(0, str(_COMMON_DIR))

from reasoning_log import ReasoningLogger


class _HTMLTextExtractor(HTMLParser):
    """Extract readable text from HTML while skipping script/style content."""

    def __init__(self) -> None:
        """
        Relevance: Operates within the ingestion and KB writeback layer.
        Concept: Internal helper implementing one deterministic step of this stage.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        super().__init__()
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        """
        Relevance: Operates within the ingestion and KB writeback layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag in {"p", "div", "section", "article", "li", "br", "h1", "h2", "h3", "h4"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        """
        Relevance: Operates within the ingestion and KB writeback layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        if tag in {"script", "style", "noscript"} and self._skip_depth > 0:
            self._skip_depth -= 1
        if tag in {"p", "div", "section", "article", "li", "br"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        """
        Relevance: Operates within the ingestion and KB writeback layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        if self._skip_depth == 0:
            text = data.strip()
            if text:
                self._chunks.append(text)
                self._chunks.append(" ")

    def get_text(self) -> str:
        """
        Relevance: Operates within the ingestion and KB writeback layer.
        Concept: Primary callable implementing a stage-level behavior.
        Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
        """

        return "".join(self._chunks)


def _is_url(source: str) -> bool:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    return source.startswith("http://") or source.startswith("https://")


def _normalize_text(text: str) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Normalization of input structures into stable internal forms.
    Contribution: Reduces runtime ambiguity and prevents malformed artifacts from destabilizing the workflow.
    """

    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    text = re.sub(r"[\t ]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _read_url_text(url: str, timeout: float) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "abducer-kb-ingest/1.0 (+https://local)"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = response.read()
        charset = response.headers.get_content_charset() or "utf-8"
    html = payload.decode(charset, errors="replace")
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return _normalize_text(parser.get_text())


def _read_pdf_text(path: Path) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    reader_cls = None
    try:
        from pypdf import PdfReader  # type: ignore

        reader_cls = PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader  # type: ignore

            reader_cls = PdfReader
        except Exception as exc:
            raise RuntimeError(
                "PDF extraction requires 'pypdf' or 'PyPDF2' to be installed."
            ) from exc

    reader = reader_cls(str(path))
    pages: list[str] = []
    for page_index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            pages.append(f"[page {page_index}]\n{page_text.strip()}")
    return _normalize_text("\n\n".join(pages))


def _read_local_text(path: Path) -> str:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {path}")
    if path.suffix.lower() == ".pdf":
        return _read_pdf_text(path)
    return _normalize_text(path.read_text(encoding="utf-8", errors="replace"))


def _soft_cut(text: str, chunk_size: int, min_ratio: float = 0.6) -> int:
    """Prefer cutting on whitespace/newline near the end of the chunk."""
    if len(text) <= chunk_size:
        return len(text)
    min_cut = int(chunk_size * min_ratio)
    window = text[:chunk_size]
    cut_idx = max(window.rfind("\n", min_cut), window.rfind(" ", min_cut))
    if cut_idx <= 0:
        return chunk_size
    return cut_idx


def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[tuple[int, int, str]]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0:
        raise ValueError("overlap must be >= 0")
    step_floor = chunk_size - overlap
    if step_floor <= 0:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[tuple[int, int, str]] = []
    start = 0
    prev_start = -1
    text_len = len(text)

    while start < text_len:
        remaining = text[start:]
        cut = _soft_cut(remaining, chunk_size)
        end = start + cut
        snippet = text[start:end].strip()
        if snippet:
            chunks.append((start, end, snippet))
        if end >= text_len:
            break
        prev_start, start = start, max(0, end - overlap)
        if start <= prev_start:
            start = prev_start + step_floor

    return chunks


def _load_sources(args: argparse.Namespace) -> list[str]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Loading and structuring external artifacts for deterministic processing.
    Contribution: Provides clean, typed inputs so downstream reasoning steps remain auditable.
    """

    sources: list[str] = []
    sources.extend(args.source)
    if args.source_file:
        lines = Path(args.source_file).read_text(encoding="utf-8").splitlines()
        for line in lines:
            cleaned = line.strip()
            if cleaned and not cleaned.startswith("#"):
                sources.append(cleaned)
    unique_sources = []
    seen: set[str] = set()
    for source in sources:
        if source not in seen:
            unique_sources.append(source)
            seen.add(source)
    return unique_sources


def _iter_records(
    sources: Iterable[str],
    chunk_size: int,
    overlap: int,
    timeout: float,
) -> tuple[list[dict], list[dict]]:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: Internal helper implementing one deterministic step of this stage.
    Contribution: Contributes a deterministic transformation that supports end-to-end reasoning reproducibility.
    """

    records: list[dict] = []
    source_manifest: list[dict] = []

    for source_index, source in enumerate(sources, start=1):
        source_id = f"src.{source_index:03d}"
        source_kind = "web" if _is_url(source) else "file"
        if source_kind == "web":
            text = _read_url_text(source, timeout=timeout)
        else:
            text = _read_local_text(Path(source))

        chunks = _chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        source_manifest.append(
            {
                "source_id": source_id,
                "source": source,
                "kind": source_kind,
                "char_length": len(text),
                "chunk_count": len(chunks),
            }
        )

        for chunk_index, (start, end, snippet) in enumerate(chunks, start=1):
            records.append(
                {
                    "chunk_id": f"{source_id}.{chunk_index:04d}",
                    "source_id": source_id,
                    "source": source,
                    "source_kind": source_kind,
                    "locator": f"chars {start}-{end}",
                    "text": snippet,
                }
            )

    return records, source_manifest


def main() -> int:
    """
    Relevance: Operates within the ingestion and KB writeback layer.
    Concept: CLI entrypoint orchestration for this script.
    Contribution: Binds parsing, computation, and artifact emission into a reproducible script execution.
    """

    logger = ReasoningLogger("latex-kb-ingest")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        default=[],
        help="Input source URL or local file path (repeatable).",
    )
    parser.add_argument(
        "--source-file",
        help="Text file with one source (URL/path) per line.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=2200,
        help="Max characters per chunk (default: 2200).",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=250,
        help="Character overlap between consecutive chunks (default: 250).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="Network timeout in seconds for URL reads (default: 20).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output JSONL path for chunk records.",
    )
    parser.add_argument(
        "--manifest",
        help="Optional output JSON path for per-source chunk stats.",
    )
    args = parser.parse_args()
    logger.step(
        "Parsed chunking arguments",
        "\n".join(
            [
                f"output={args.output}",
                f"manifest={args.manifest or ''}",
                f"chunk_size={args.chunk_size}",
                f"overlap={args.overlap}",
                f"timeout={args.timeout}",
            ]
        ),
    )

    sources = _load_sources(args)
    if not sources:
        parser.error("No sources provided. Use --source or --source-file.")
    logger.step("Loaded sources", f"source_count={len(sources)}")

    try:
        records, source_manifest = _iter_records(
            sources=sources,
            chunk_size=args.chunk_size,
            overlap=args.overlap,
            timeout=args.timeout,
        )
    except Exception as exc:  # pragma: no cover - CLI error path
        log_path = logger.finalize("error", summary=str(exc))
        print(f"[LOG] {log_path}", file=sys.stderr)
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    logger.step(
        "Constructed chunk records",
        f"record_count={len(records)}\nsource_manifest_count={len(source_manifest)}",
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    logger.add_output("chunks_jsonl", output_path)

    if args.manifest:
        manifest_path = Path(args.manifest)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps({"sources": source_manifest}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        logger.add_output("source_manifest_json", manifest_path)

    print(f"[OK] Wrote {len(records)} chunks to {output_path}")
    print(f"[OK] Sources processed: {len(source_manifest)}")
    log_path = logger.finalize(
        "success",
        summary=f"Processed {len(source_manifest)} sources into {len(records)} chunks.",
    )
    print(f"[LOG] {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
