# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

"""
Regression tests for the `cohere` orchestrator intent and its CLI surface.

Concept: Verifies that the framework exposes coherence-oriented orchestration as a first-class inference mode.
Contribution: Prevents routing regressions that would break the connect-plus-coherence execution contract.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _mini_kb_text() -> str:
    """
    Concept: Produces a minimal KB fixture that still satisfies the orchestrator's schema expectations.
    Contribution: Lets the tests exercise `cohere` mode end to end without depending on large problem-specific KB assets.
    """
    return """---
kb_id: mini-problem
title: Mini Problem
domain: mathematics
subdomain: testing
version: 0.1.0
status: draft
created_utc: 2026-03-11T00:00:00Z
updated_utc: 2026-03-11T00:00:00Z
owners:
  - test
source_policy:
  allow_web: false
  allow_local_docs: true
  citation_required: false
---

# Source Index

| source_id | type | citation | locator | reliability | notes |
|---|---|---|---|---|---|
| src.001 | local | inline | section 1 | high | test |

# Symbol Glossary

- `sym.001`: `x` - test symbol.

# Concept Structure

```yaml
concept_nodes:
  - id: cnc.example
    label: Example Concept
    type: concept
method_nodes: []
barrier_nodes: []
relations:
  - from: st.def.example
    to: cnc.example
    relation: defines
  - from: st.thm.example
    to: cnc.example
    relation: uses
```

# Canonical Statements

```yaml
id: st.def.example
kind: definition
status: accepted
latex: |
  Example definition.
informal: |
  Example definition.
source_ids: [src.001]
used_symbols: [sym.001]
depends_on: []
concept_roles: [cnc.example]
method_tags: []
barrier_family: ""
confidence: 0.95
proof_sketch: |
  
notes: |
  
```

```yaml
id: st.thm.example
kind: theorem
status: accepted
latex: |
  If the example definition holds, then the example theorem holds.
informal: |
  Example theorem using the example definition.
source_ids: [src.001]
used_symbols: [sym.001]
depends_on: [st.def.example]
concept_roles: [cnc.example]
method_tags: []
barrier_family: ""
confidence: 0.9
proof_sketch: |
  Apply the definition directly.
notes: |
  
```

# Derived Statements

# Open Gaps

# Change Log

- 2026-03-11: Initialized test KB.
"""


def test_run_orchestrator_help_lists_cohere() -> None:
    """
    Concept: Validates that run orchestrator help lists cohere.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    script = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "run_orchestrator.py"
    result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True, cwd=ROOT)
    assert result.returncode == 0
    merged = (result.stdout or "") + (result.stderr or "")
    assert "cohere" in merged
    assert "conceptual-space-animation" in merged
    assert "search-space-tree" in merged


def test_run_orchestrator_cohere_generates_analysis_and_coherence(tmp_path: Path) -> None:
    """
    Concept: Validates that run orchestrator cohere generates analysis and coherence.
    Contribution: Documents the intended regression boundary so later changes do not silently weaken the framework's reasoning behavior.
    """
    kb_dir = tmp_path / "KB"
    kb_dir.mkdir(parents=True, exist_ok=True)
    kb = kb_dir / "mini-problem.kb.md"
    kb.write_text(_mini_kb_text(), encoding="utf-8")

    script = ROOT / "skills" / "orchestration" / "kb-orchestrator" / "scripts" / "run_orchestrator.py"
    cmd = [
        sys.executable,
        str(script),
        "--intent",
        "cohere",
        "--kb",
        str(kb),
        "--no-export-phyp-docs",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    merged = (result.stdout or "") + (result.stderr or "")

    artifacts = ROOT / "artifacts" / "mini-problem"
    phyp = ROOT / "phyp" / "mini-problem.proof-hypotheses.yaml"
    try:
        assert result.returncode == 0, merged
        assert (artifacts / "connection-analysis.json").exists()
        assert (artifacts / "coherence-report.json").exists()
        assert (artifacts / "reasoning-log-index.md").exists()
        assert (artifacts / "reasoning-surface-index.md").exists()
        assert (artifacts / "conceptual-dynamics.html").exists()
        assert (artifacts / "conceptual-space-animation.html").exists()
        assert (artifacts / "search-space-tree.md").exists()
        assert (ROOT / "artifacts" / "search-space-state" / "mini-problem.json").exists()
        assert phyp.exists()
    finally:
        if artifacts.exists():
            shutil.rmtree(artifacts)
        search_state = ROOT / "artifacts" / "search-space-state" / "mini-problem.json"
        if search_state.exists():
            search_state.unlink()
        if phyp.exists():
            phyp.unlink()
