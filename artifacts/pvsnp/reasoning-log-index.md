# Reasoning Log Index

This index consolidates reasoning logs for a run and highlights whether expected stages emitted logs.

## Run Context

- Generated (UTC): 2026-03-11T11:48:43.201263+00:00
- KB: KB/p-vs-np.kb.md
- Artifacts directory: /Users/user/files/abducer/abducer/artifacts/pvsnp
- Log root: /Users/user/files/abducer/abducer/artifacts/reasoning-logs
- Run ID filter: 20260311T114842Z-17245

## Coverage Summary

- Logs indexed: 3
- Status counts: {"success": 3}
- Observed agents: kb-interpretation-reporter, kb-log-indexer, kb-orchestrator
- Expected agents: kb-interpretation-reporter, kb-log-indexer, kb-orchestrator
- Missing expected agents: none
- Coverage verdict: complete

## Run Timeline

| start_utc | end_utc | agent | status | duration_s | key_step |
|---|---|---|---|---:|---|
| 2026-03-11T11:48:42.883797+00:00 | 2026-03-11T11:48:43.133919+00:00 | kb-orchestrator | success | 0.25 | Parsed orchestrator arguments |
| 2026-03-11T11:48:42.930816+00:00 | 2026-03-11T11:48:42.981473+00:00 | kb-interpretation-reporter | success | 0.051 | Parsed interpretation-report arguments |
| 2026-03-11T11:48:43.037622+00:00 | 2026-03-11T11:48:43.115602+00:00 | kb-log-indexer | success | 0.078 | Parsed reasoning-log-index arguments |

## Log Table

| agent | status | duration_s | steps | key_steps | summary | log_path |
|---|---|---:|---:|---|---|---|
| kb-orchestrator | success | 0.25 | 5 | Parsed orchestrator arguments; Running stage: interpretation-reports; Completed stage: interpretation-reports | Intent `interpretation-reports` completed. | /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-orchestrator/20260311T114842Z-17245.md |
| kb-interpretation-reporter | success | 0.051 | 1 | Parsed interpretation-report arguments | Generated human-readable interpretation reports in /Users/user/files/abducer/abducer/artifacts/pvsnp. | /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-interpretation-reporter/20260311T114842Z-17246.md |
| kb-log-indexer | success | 0.078 | 1 | Parsed reasoning-log-index arguments | Indexed 2 reasoning logs (1 missing expected agents). | /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-log-indexer/20260311T114843Z-17247.md |

## Agent Details

### kb-orchestrator

- Log: /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-orchestrator/20260311T114842Z-17245.md
- Run ID: 20260311T114842Z-17245
- Status: success
- Started: 2026-03-11T11:48:42.883797+00:00
- Ended: 2026-03-11T11:48:43.133919+00:00
- Duration (s): 0.25
- Steps: 5
- Key steps: Parsed orchestrator arguments; Running stage: interpretation-reports; Completed stage: interpretation-reports; Running stage: reasoning-log-index; Completed stage: reasoning-log-index
- Summary: Intent `interpretation-reports` completed.
- Declared outputs:
  - interpretation-reports.reasoning_log.1: /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-interpretation-reporter/20260311T114842Z-17246.md
  - reasoning_process_report_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-process-report.md
  - discovery_interpretation_report_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/discovery-interpretation-report.md
  - reasoning-log-index.reasoning_log.1: /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-log-indexer/20260311T114843Z-17247.md
  - reasoning_log_index_json: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-log-index.json
  - reasoning_log_index_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-log-index.md

### kb-interpretation-reporter

- Log: /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-interpretation-reporter/20260311T114842Z-17246.md
- Run ID: 20260311T114842Z-17245
- Status: success
- Started: 2026-03-11T11:48:42.930816+00:00
- Ended: 2026-03-11T11:48:42.981473+00:00
- Duration (s): 0.051
- Steps: 1
- Key steps: Parsed interpretation-report arguments
- Summary: Generated human-readable interpretation reports in /Users/user/files/abducer/abducer/artifacts/pvsnp.
- Declared outputs:
  - reasoning_process_report_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-process-report.md
  - discovery_interpretation_report_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/discovery-interpretation-report.md

### kb-log-indexer

- Log: /Users/user/files/abducer/abducer/artifacts/reasoning-logs/kb-log-indexer/20260311T114843Z-17247.md
- Run ID: 20260311T114842Z-17245
- Status: success
- Started: 2026-03-11T11:48:43.037622+00:00
- Ended: 2026-03-11T11:48:43.115602+00:00
- Duration (s): 0.078
- Steps: 1
- Key steps: Parsed reasoning-log-index arguments
- Summary: Indexed 2 reasoning logs (1 missing expected agents).
- Declared outputs:
  - reasoning_log_index_json: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-log-index.json
  - reasoning_log_index_md: /Users/user/files/abducer/abducer/artifacts/pvsnp/reasoning-log-index.md
