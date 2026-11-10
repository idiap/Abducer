<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Software disclosure preparation

The disclosure gate is `check.sh`. It requires the locked development environment,
the local Idiap SD preparation helpers, and Lunar frontend dependencies. Required
checks currently fail; this repository is not ready for disclosure. See
[the verification record](../../.prism/idiap-software-disclosure/06-verification.md).

For a shorter local check, exclude tests marked `expensive`. The marker identifies
test functions with a case taking at least 30 seconds in the preserved JUnit
reports, including timeouts. All parameter variants of those functions carry the
marker. Tests sharing their module fixtures are also marked, including transitive
fixture dependencies, so exclusion does not simply move the same setup cost to
another test. Timing includes setup and teardown, varies by machine, and does not
guarantee a fixed runtime for the remaining tests.

```bash
# Python tests without the measured expensive group:
.venv/bin/python -m pytest -m "not expensive"
# Run the eight check.sh commands, with only that Python group deselected:
PYTEST_ADDOPTS='-m "not expensive"' ./check.sh
# Run the expensive group explicitly and report the slowest phases:
.venv/bin/python -m pytest -m expensive --durations=20
```

Default `pytest` and `check.sh` still include every test. The shorter command is
for local feedback; disclosure acceptance requires the complete suite. Markers
are read during collection and do not change a run already in progress. Other
check commands, including the Git-history attribution audit, still run fully.

The largest measured costs were the world-v3 store-backed facade/replay case
(314 seconds), world-v3 content-graph and authority-attack cases (several reached
120 seconds), proof stale-fork finalization (120 seconds), and proof exact
counterexample execution (116 seconds). These are historical observations rather
than a new benchmark. The full per-case timing/selection evidence is recorded in
`.prism/idiap-software-disclosure/evidence/expensive-test-timings.json`.

The invoked `idiap-sd` skill requires `.idiap-sd/` and root workspace agent
configuration to remain local and ignored, including generated Prism VS Code
onboarding tasks. Existing copies remain available in
the preparation workspace. Nested agent files in conversion fixtures, examples,
and preserved upstream bundles are application inputs and remain tracked.
The attribution enumerator excludes root local settings even if they are still
tracked. Other tracked project assets remain audited, including archives that
match unrelated ignore rules.

Before running the gate in a fresh checkout, provision the reviewed local helper
snapshot from the maintainer's preparation workspace:

```bash
tar -xzf "$SD_PREPARATION_ARCHIVE" -C "$PWD"
bash prism_me/scripts/init_vscode_onboarding.sh
uv sync --locked --dev
PATH="$PWD/.venv/bin:$PATH" ./check.sh
```

`SD_PREPARATION_ARCHIVE` must name the reviewed archive containing only
`.idiap-sd/README.md`, `config.json`, `idiap_sd.py`, `reuse_policy.py`,
`plan_attribution.py`, and `frontend_tests.py`. The preparation workspace exports
this snapshot as `/private/tmp/abducer-idiap-sd-preparation-repairs.tar.gz`; its digest is
recorded in the request evidence. CI must supply that archive before invoking
`check.sh` or the infrastructure tests. The onboarding command recreates ignored
root agent settings from tracked templates; the hook compatibility tests require
that local setup too. Missing helpers are an explicit setup
failure, and checks are never silently skipped.

To recreate preparation without the snapshot, copy `check.sh`, `idiap_sd.py`,
and `config.json` from the installed `idiap-sd` skill assets. Reapply the reviewed
repository policy before applying metadata: MIT for first-party files;
MathJax's Apache-2.0 copyright and combined report licensing; per-path Git author
aliases for Andre Freitas and Danilo Gusicuma; safe comment headers by default;
REUSE.toml for uncommentable data and documented byte-bound evidence; sidecars
only for isolated binaries; and a 5,242,880-byte LFS threshold. Preserve the
strict JSON/YAML and manifest-bound source exceptions. The local snapshot is
needed to reproduce the exact reviewed policy and its regression tests; the
generic skill assets alone do not include these repository-specific refinements.

Skill attribution is maintained in root `REUSE.toml` for every tracked `SKILL.md`.
Maintained `skills`, `proj_skills`, `prism_me` and plugin entries carry no inline
license comments. Preserved upstream and conversion-fixture copies retain their
original bytes and notices; their complete contributor metadata is also recorded
in the table. Never remove earlier copyright or contributor credit while adding
new Git-backed contributors.

The preparation policy must merge existing root and nested REUSE annotations,
headers and sidecars before adding the per-path `git log --follow` author map.
It also audits the tracked `.agents/plugins/marketplace.json` catalog as project
functionality while excluding private local agent settings. The four validator
snapshot files listed in `integrations/workflow_contracts/origin.json` use table
metadata to preserve their checksums. The plugin generator projects reviewed
root-table attribution into the package's own `REUSE.toml`, so installed skills
retain the same contributor credit without access to the source repository.

Keep annotation tables compact with
`agentic/scripts/compact_reuse_annotations.py`. The local preparation generator
uses this helper after planning directory defaults. It merges equivalent tables,
generalizes repeated path components and retains narrower contributor and license
exceptions. Each transformation must preserve the winning table's complete
metadata for all known paths; probes also protect defaults for future files.
If recreating preparation from generic skill assets, run this command after
applying metadata. `--check` reports whether further compaction is possible.
The helper preserves precedence; converting an `aggregate` rule to `closest`
requires a separate comparison of effective headers, sidecars and nested tables.

For example, after contributor reconciliation, regenerate both workflow and
plugin metadata, then check licensing and placement:

```bash
.venv/bin/python agentic/scripts/compact_reuse_annotations.py
.venv/bin/python agentic/scripts/normalize_workflow_skills.py
.venv/bin/python integrations/agent_plugins/generate.py
.venv/bin/reuse lint
.venv/bin/python .idiap-sd/idiap_sd.py check
.venv/bin/python -m pytest tests/infrastructure/test_reuse_skill_attribution.py -q
```

REUSE validates copyright and licenses; the separate history audit checks
contributor coverage. Preserve the exact Git revision and prior notices in the
audit evidence. An unchanged-HEAD history cache may avoid repeating expensive
Git reads, but metadata and LFS checks must always inspect the current files.

Frontend checks exercise the sibling `../lunar-platform`, or `LUNAR_ROOT` if set,
with its frontend dependencies installed. The separate Markov–Kakutani HTML probe
requires a completed research report and remains an unmet research prerequisite.

Governed subprocess tests require permission to launch macOS `/bin/ps` and
sample child process groups. Run the complete gate in a normal terminal or an
explicitly authorized unrestricted execution environment. A restricted runner
can produce `sampler_launch_failed` followed by worker SIGTERM and many
dependent setup errors. Those results diagnose the runner; do not disable the
sampler, weaken receipt validation, or mark these tests skipped to hide them.

The work-cycle report tests also need TeX Live with `enumitem.sty`. This workspace
uses a temporary user tree, provisioned without replacing the system packages:

```bash
SD_TEXMF_ROOT="$PWD/.idiap-sd/texmf"
tlmgr --usermode --usertree="$SD_TEXMF_ROOT" init-usertree
tlmgr --usermode --usertree="$SD_TEXMF_ROOT" --repository https://mirror.ctan.org/systems/texlive/tlnet install enumitem
TEXINPUTS="$SD_TEXMF_ROOT/tex/latex//:${TEXINPUTS-}" PATH="$PWD/.venv/bin:$PATH" ./check.sh
```

All six previously blocked work-cycle report cases pass with this package and
the venv on `PATH`. A full TeX installation that already provides the package
can use the ordinary gate command. Generated runtime reasoning logs and derived
surfaces are ignored; historical tracked evidence remains in the disclosure.

The current publication tooling cannot migrate the preserved discovery evidence
to an accepted v2 publication. See
[the migration assessment](../../.prism/idiap-software-disclosure/09-publication-migration.md)
for the actual planner failures and missing evidence. Archived discovery bytes
must remain intact; changing schema versions or generating replacement receipts
does not supply the missing scientific provenance.

## Repository-local source inputs

Importer defaults resolve from the repository root, independently of the shell's
working directory. The 2026-07-20 and 2026-07-21 Yang–Mills importers and the
higher-abductive importer use the preserved ZIPs in their existing
`agentic/external/<source>/<date>/source_archives/` directories. Replay keeps
those source archives intact. The dated importers still accept `--archive` or
`--source` for an alternative input.

The cohere source ZIP is absent from this checkout. Supply it at
`agentic/imports/cohere_fast/source_archives/discover-main-repo.zip`, or run:

```bash
python agentic/scripts/validate_cohere_fast_source_manifest.py --archive inputs/discover-main-repo.zip
```

The framework registry expects absent source ZIPs under
`agentic/imports/looper/source_archives/` and
`agentic/imports/hegelian_solver/source_archives/`. The proof-delivery queue's
original draft reference is now
`agentic/imports/pvsnp/source_documents/parity_magnification_full_row_barrier (1).tex`.
These locations identify original inputs; revised papers are not substituted for
missing originals. Historical provenance records retain their recorded paths.

The ignored attribution helper uses `.idiap-sd/evidence/attribution-before.jsonl`
by default and accepts `--cache PATH`. Its audited-HEAD guard remains in force:
the earlier cache cannot be reused after a commit without a new history scan.
