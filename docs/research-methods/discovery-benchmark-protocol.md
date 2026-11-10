<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Conceptual Discovery Benchmark Protocol

This protocol tests whether the discovery cycle reconstructs or transforms conceptual structure without leaking frozen answers. It has two non-interchangeable evidence lanes. `synthetic_protocol_fixture` validates the harness only. `live_external_hidden_task` is a requested future evidence lane, but the repository-local subprocess adapter does not currently provide the deny-by-construction isolation or out-of-band signed authority needed to authorize it. Route reconstruction, conceptual transformation, understanding, empirical support, proof validity, and human preference remain separate outcomes. None is automatically proof.

## Split and authorship discipline

Tasks use domain-level train, development, and frozen splits. No domain may straddle development and frozen evaluation. Frozen ground truth is authored independently of the searched KB, carries provenance, and is loaded only by the evaluator after the candidate packet is closed. Hyperparameters and stopping policy may use train and development only.

The executable frozen fixture covers functional analysis, complexity theory, and mathematical physics. Its rubric values are explicitly synthetic. The report always returns `efficacy_authorized: false` and `replicated: false`, even when every fixture check passes.

## Leakage controls

Before scoring, the evaluator scans the working context and generation-input manifest for:

- normalized target labels and aliases;
- whitespace/brace-normalized LaTeX signatures;
- paired dependency endpoints that expose the hidden route;
- frozen-answer paths or artifact-presence markers.

Seeded decoys prove that every channel is detectable. A detected channel invalidates the case; it is not repaired by lowering the score.

## Time-sliced literature

Every case declares a publication cutoff. The discovery context contains only sources at or before that date. A later source is withheld until output closure, then supplied to the literature rebase evaluator. Success requires a source-bound `absorb`, `reframe`, `merge`, `split`, `retire`, or `new_question` effect. Mere citation growth is not assimilation.

## Live capture, baselines, and budgets

The live harness runs an exact task × condition × repetition matrix and closes every output before the evaluator loads ground truth. It requires at least five repetitions in each of six conditions: full discovery, conservative baseline, literature-only baseline, no reflection, no literature, and no parallelism. Every output receives the same preregistered token, wall-time, and cost-unit opportunity budget; actual usage and output bytes are captured and content-bound. Low plausibility or counter-consensus posture never counts as creativity without relevance, mechanism, value if right, learning if wrong, and a correction condition.

External commands run in invocation-specific process groups and working directories under `agentic/runs/discovery_benchmark_processes/<run-id>/`. These are lifecycle and accounting controls, not a security sandbox. A local worker can still traverse host paths, follow links, inherit environment data, create processes or sockets, and perform undeclared reads; the receipt therefore records `unisolated_protocol_only` and `external_efficacy_eligible: false`. JSON stdin and stdout/stderr have explicit byte caps; wall time, CPU, process-group memory, and attempt-local disk growth are measured. Each call creates an immutable receipt and each role creates an immutable aggregate index. A timeout, descendant leak, stream cap, launch error, or malformed JSON is an operational failure only: no candidate is scored and no hypothesis is updated.

Index replay is linear in the number of receipts. One validation context structurally replays an index and each receipt once, validates each distinct live command authority once, serves later memberships from detached deep copies, and finishes with one byte-exact drift sweep. Warm calls check the requested receipt's immutable metadata, so caller mutation cannot poison the cache and on-disk mutation fails before reuse. The terminal sweep catches drift in any other cached receipt without rehashing the whole index for every output.

The benchmark opportunity field `cost_units` is deliberately not relabeled as USD. Generic process supervision cannot independently observe provider network traffic or monetary cost, so those dimensions remain unavailable unless a real adapter reports them. Runner token counts are explicitly externally reported rather than independently measured.

## Authenticated blinded-human review

Live outputs are randomized and shown without condition labels. At least two disclosed, independent raters score every output on target relevance, conceptual depth, explanatory understanding, unification with preserved difference, philosophical clarity, generativity, coherence, and honest truth boundaries. The rating artifact is external and byte-digested. A governed verifier can authenticate its bytes, blinding declaration, rater declarations, and immutability under caller policy. The current trust-anchor builder deliberately emits `caller_policy_eligibility_only` with `out_of_band_signature_status: unavailable_no_independent_trust_store`; a repository author cannot mint external independence by hashing another local JSON object. Consequently even a positive local rating effect is reported as `positive_caller_policy_only`, while `efficacy_authorized` and `replicated` remain false.

The report keeps five decisions separate: process-chain authentication, caller-policy eligibility, external-authority eligibility, the primary positive-effect gate, and the all-comparison replication gate. Negative, null, and underpowered outcomes retain their own statuses. External efficacy can only become available in a future adapter that both denies input/filesystem/environment/process/network exfiltration by construction and verifies an authority-distinct signed trust store out of band; neither property may be asserted by the worker, evidence packet, or repository-local fixture itself.

Verifier execution and verifier judgment are different axes. A successfully executed verifier may return `authentication_rejected`. Failure to launch, timeout, descendant leakage, stream exhaustion, or invalid JSON returns `verifier_operational_failure` with no epistemic effect; infrastructure failure is never treated as evidence that the rating artifact is inauthentic.

## Repetitions, uncertainty, and effects

The evaluator pairs full and control ratings within task and repetition. For each baseline/ablation it reports the number of pairs, arm means, mean difference, sample standard deviation, standard error, 95% interval, standardized effect size, positive-pair fraction, and a degenerate-variance flag. Replication requires every preregistered comparison to have a positive lower interval bound, nondegenerate variation, and the minimum standardized effect. Automatic held-out matching remains a secondary diagnostic.

## Replication gate

`simulate_theorem_discovery.py --benchmark-manifest ... --require-replicated` returns nonzero unless an externally authorized replicated lane passes. Therefore both the synthetic fixture and all current local subprocess runs intentionally return nonzero with `--require-replicated`; use them without that flag to inspect protocol validity, caller-policy authentication, and effect diagnostics. Live capture accepts a local runner as JSON argv on stdin/stdout. Live rating evaluation accepts a local verifier command, but it remains protocol-only.

External commands require a unique `--benchmark-run-id`. Use an executable on `PATH` or absolute script paths because the command runs from its isolated attempt directory. Operational caps are configurable through the `--benchmark-process-*-bytes`, `--benchmark-process-grace-seconds`, and `--human-verifier-wall-seconds` options.

```bash
uv run python -m pytest -q tests/experiments/test_discovery_benchmark_integrity.py
uv run python skills/orchestration/kb-orchestrator/scripts/simulate_theorem_discovery.py \
  --benchmark-manifest tests/fixtures/discovery_benchmarks/frozen.json
```
