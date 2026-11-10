<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Type gallery

`types.prism` is a compact, checked catalogue of type forms useful during
conversion. Its comments connect syntax with the fuller taxonomy in
`../../references/type-taxonomy.md`.

The module demonstrates declarations, not an assurance ladder. In particular,
the presence of `Generated`, `Evidence`, `Computed`, `Validated`, `Supported`,
or `Verified` in a contract does not create a value of that type.

```sh
./.venv/bin/prism check examples/type_gallery/types.prism
./.venv/bin/prism compile examples/type_gallery/types.prism
```
