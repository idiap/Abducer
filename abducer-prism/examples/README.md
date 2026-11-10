<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# `to_prism` examples

These examples are part of the transferable package and require no Prism
source checkout. From the unpacked `to_prism` directory, bootstrap once:

```sh
./bootstrap
```

Then explore them in this order:

1. `epistemic_incident_diagnosis/` derives specific epistemic objects and
   operations from an incident-triage request. Its data distinguishes
   observations, hypotheses, ranked assessments, critiques, defeaters,
   recommendations, decisions, and actions.
2. `type_gallery/` shows representative structural, provenance, assurance,
   callable, and failure types in one checked module.
3. `layered_release_review/` shows how domain, reasoning, materialization, and
   application layers form one runnable general-Prism workflow. It demonstrates
   layer separation; the narrower conversion profile always makes epistemic
   occurrence outputs `Generated[T]`.
4. `conversion_input/` is a tiny provider-native Codex project plus a reviewed
   plan that can be converted into a portable Prism project.

Check all hand-authored Prism examples:

```sh
./.venv/bin/prism check examples/type_gallery/types.prism
./.venv/bin/prism compile examples/type_gallery/types.prism
./.venv/bin/prism check examples/layered_release_review/main.prism
./.venv/bin/prism compile examples/layered_release_review/main.prism
./.venv/bin/prism run examples/layered_release_review/main.prism --handler fake
```

The examples deliberately avoid credentials, external services, and native
provider execution. A fake-handler run is an executability smoke test, not an
equivalence result.
