# Public reasoning trace store

Canonical events live in `runs/<run-id>/events.jsonl`; each run has a compact manifest. Files under `latest/` are compatibility views and are never the historical source of truth.

Writes are lock-protected and atomically replace the complete JSONL stream. Event IDs are idempotency boundaries: retrying the same event returns its original sequence and timestamp, while reusing an ID for different content fails. Causal parents must already exist in the same run, preventing cross-run contamination.

Callers should supply stable `run_id` and `idempotency_key` values. Store only bounded public rationales and artifact references—never prompts, secrets, raw tool payloads, or hidden chain-of-thought.
