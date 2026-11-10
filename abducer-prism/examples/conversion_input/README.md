<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# End-to-end conversion input

`source/` is a minimal provider-native Codex project. The converter reads it
without modifying it. `approved-plan.json` is the explicit review decision that
permits generation.

From the unpacked `to_prism` directory:

```sh
workdir=$(mktemp -d)
./to-prism inspect \
  --source examples/conversion_input/source \
  --output "$workdir/conversion"
./to-prism model \
  --source examples/conversion_input/source \
  --output "$workdir/conversion"
./to-prism generate \
  --source examples/conversion_input/source \
  --output "$workdir/conversion" \
  --plan examples/conversion_input/approved-plan.json \
  --handler fake
./to-prism verify \
  --source examples/conversion_input/source \
  --output "$workdir/conversion" \
  --portable \
  --handler fake
```

Generation is portable by default and copies the bundled Prism dependency
closure into the generated project. The reviewed skill becomes a typed Prism
skill artifact and the final orchestration is canonical `.prism`.
