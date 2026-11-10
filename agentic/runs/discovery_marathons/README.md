# Discovery Marathon Runs

This directory stores long-horizon recursive discovery runs. A marathon is not a background note dump: it has a run state, branch-local memory, cycle packets, skill-dispatch traces, validator history, reports, and deep reviews.

The active pointer is `active_run.json`. The durable state lives under `agentic/runs/discovery_marathons/<run_id>/`.

Core commands:

```bash
python agentic/scripts/init_discovery_marathon.py --target yang-mills-existence-and-mass-gap-target --hours 6 --cycle-minutes 30
python agentic/scripts/run_discovery_marathon.py --resume --max-cycles 3
python agentic/scripts/validate_discovery_marathon_state.py
python agentic/scripts/build_discovery_marathon_report.py
```

The runner does not sleep for the cycle duration during tests. `cycle_minutes` is a budget and checkpoint unit; external orchestration can call one cycle at a time.
