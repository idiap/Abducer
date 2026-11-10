<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Layered release review

This runnable example makes the generated-project layers explicit:

- `types.prism` owns domain records and the proposition;
- `occurrences.prism` owns pure reasoning-method signatures and semantic joins;
- `relations.prism` owns relation and certificate contracts;
- `reasoning.prism` owns only imports and the high-level topology;
- `materialization.prism` owns evidence capture, deterministic checks, policy,
  relation builders, and concrete bindings; and
- `main.prism` owns the fixture and solve call.

Run from the unpacked `to_prism` directory:

```sh
./.venv/bin/prism check examples/layered_release_review/main.prism
./.venv/bin/prism compile examples/layered_release_review/main.prism
./.venv/bin/prism run examples/layered_release_review/main.prism --handler fake
```

The result is `Supported[ReadyToDeploy()]`, because this organizational
decision uses traceable evidence and a named material policy. It is not
`Proof[ReadyToDeploy()]`: no kernel theorem establishes release readiness.

This hand-authored example demonstrates the full Prism language's separation
of reasoning declaration from evidence capture, deterministic checks,
defeater review, material policy, and relation builders. It is not the narrower
external-skill conversion profile. Generated `to_prism` conversions declare
every epistemic occurrence as `Input -> Generated[Output]`; any evidence,
computation, validation, support, or proof transition remains a later explicit
material boundary.
