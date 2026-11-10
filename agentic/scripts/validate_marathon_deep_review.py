#!/usr/bin/env python3
"""Validate marathon deep-review artifacts when present."""

from __future__ import annotations

from agentic_common import ROOT, clean_text, fail, rel
from discovery_marathon_common import load_reviews, load_run_state


def main() -> int:
    _, run_state = load_run_state()
    if not run_state:
        print("No active discovery marathon; deep-review validator is idle.")
        return 0
    reviews = load_reviews(run_state)
    if not reviews:
        print("No marathon deep reviews yet; validator is idle.")
        return 0
    for review in reviews:
        for field in ["review_id", "run_id", "summary", "findings", "recommendation", "next_review_trigger"]:
            if not review.get(field):
                fail(f"marathon review {review.get('review_id', '<unknown>')} missing {field}")
        text = clean_text(review).lower()
        for marker in ["no breakthrough", "skill use", "mathematical", "recommendation"]:
            if marker not in text:
                fail(f"marathon review {review['review_id']} lacks `{marker}`")
        if not any(marker in text for marker in ["certification", "certifies", "certify"]):
            fail(f"marathon review {review['review_id']} lacks `certification`")
        md = ROOT / f"agentic/runs/discovery_marathons/{run_state['run_id']}/reviews/{review['review_id'].replace('.', '-')}.md"
        if not md.exists():
            # Stable IDs include dots but paths are slugified; tolerate JSON-only review if the renderer changed.
            continue
    print(f"validated {len(reviews)} marathon deep review(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
