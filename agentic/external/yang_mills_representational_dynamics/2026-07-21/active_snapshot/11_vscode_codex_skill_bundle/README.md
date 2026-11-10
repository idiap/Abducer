# Yang--Mills workflow skills for VS Code Codex

This bundle exports the 30 validated skills used by the representation-aware
Yang--Mills research workflow. It is a direct Codex skill bundle, not a plugin,
so it works with the Codex IDE extension as repository-scoped or user-scoped
skills.

The scientific status remains conservative: the workflow organizes, tests, and
audits a constructive programme. It does not claim a solution of the Clay
Yang--Mills problem.

## Fast installation

From the unpacked bundle, install into one repository:

```bash
python3 install_skills.py --scope repo --repo /path/to/repository
```

On Windows PowerShell, `py` can replace `python3`:

```powershell
py install_skills.py --scope repo --repo C:\path\to\repository
```

For skills available in every repository owned by the current user:

```bash
python3 install_skills.py --scope user
```

The installer has no third-party dependencies. It checks the whole destination
before copying anything and refuses to overwrite a divergent skill directory.
Use `--dry-run` to inspect the operation first.

You can also copy the included `.agents/skills` directory directly:

- repository scope: `<repo>/.agents/skills/`
- user scope: `$HOME/.agents/skills/`

Codex scans `.agents/skills` from the current directory to the repository root.
If newly copied skills do not appear immediately, reload the Codex IDE extension
or start a new Codex session.

## Verify and invoke

Before installation:

```bash
python3 verify_bundle.py
```

After opening the repository in VS Code, type `/skills` or type `$` in the Codex
composer to select a skill. The end-to-end entry point is:

```text
Use $ym-run-clay-program to assess the current frontier, select the next
highest-value noncircular target, implement its finite certificates and tests,
and finish with $ym-audit-frontier.
```

For durable repository guidance, adapt `templates/AGENTS.md` and place it at the
repository root as `AGENTS.md`.

`CURRENT_FRONTIER.md` contains the numerical starting point produced through
Stage 50. Copy or cite it in a new research repository when the workflow
should resume from the boundary-uniform normalized comparison target rather
than repeat the earlier local or single-star repair calculations.

## Workflow map

1. **Target and language**
   - `ym-freeze-clay-target`
   - `ym-build-observable-core`
   - `ym-build-representation-calculus`
   - `ym-define-relational-rigidity`
2. **Regulators and scale dynamics**
   - `ym-design-regulator-atlas`
   - `ym-build-gauge-covariant-rg`
   - `ym-design-infrared-basin`
3. **Constructive frontier**
   - `ym-control-large-fields-and-topology`
   - `ym-prove-adaptive-block-domination`
   - `ym-prove-state-weighted-defect-transfer`
   - `ym-prove-conditional-partition-ratio`
   - `ym-prove-basin-entry`
   - `ym-prove-rg-to-rigidity`
4. **Continuum and spectrum**
   - `ym-prove-continuum-coherence`
   - `ym-prove-rigidity-transfer`
   - `ym-reconstruct-os-gap`
5. **Publication drafting**
   - `ym-develop-paper-proofs`
   - `ym-ground-paper-literature`
   - `ym-frame-paper-narrative`
   - `ym-build-proof-appendix`
   - `ym-build-latex-paper`
   - `ym-draft-frustration-obstruction`
   - `ym-draft-finite-block-certificate`
   - `ym-draft-representational-dynamics`
   - `ym-draft-heat-kernel-enclosures`
   - `ym-draft-staple-dispersion`
6. **Verification and governance**
   - `ym-calibrate-restricted-models`
   - `ym-mechanize-proof-core`
   - `ym-audit-frontier`
   - `ym-run-clay-program`

The orchestrator keeps the key implications separate:

```text
regulated construction
  -> controlled RG trajectory
  -> noncircular basin entry
  -> uniform physical rigidity
  -> coherent continuum Schwinger data
  -> OS reconstruction
  -> Hamiltonian spectral gap.
```

Each arrow is a proof obligation. Numerical calibration, finite-volume gaps,
standalone one-plaquette tails, and conditional theorems are never promoted past
their actual scope.

## Bundle contents

- `.agents/skills/`: 30 complete skill directories, each with `SKILL.md` and
  `agents/openai.yaml`.
- `skill_manifest.json`: public names, roles, phase order, and expected count.
- `SKILL_CHECKSUMS.sha256`: checksums for every file inside the skill tree.
- `install_skills.py`: guarded repository/user installer.
- `verify_bundle.py`: dependency-free structural and checksum validator.
- `templates/AGENTS.md`: optional durable repository instructions.
- `CURRENT_FRONTIER.md`: current restricted nonlinear-transfer closure,
  repair obstruction, topology split, and next physical proof target.

## Automated manuscript production

The five paper-specific skills orchestrate five shared specialists. A standard
paper run is:

```text
ym-develop-paper-proofs
  -> ym-ground-paper-literature
  -> ym-frame-paper-narrative
  -> ym-build-proof-appendix
  -> ym-build-latex-paper
  -> ym-audit-frontier
```

`ym-build-latex-paper` includes a modular article template and deterministic
scripts to scaffold a manuscript, lint citations/labels/placeholders and
workflow language, compile with `latexmk`, validate PDF metadata and extracted
text, render first/middle/last page previews, and emit a JSON build report.
