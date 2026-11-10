# Verification log

Date: 21 July 2026

## Executable suite

- Tests: 15/15 pass.
- Doob row normalization: pass.
- Stationarity and detailed balance: pass.
- Inverse-amplitude cancellation: pass to `4.34e-19`.
- Four-channel Perron residual: below `9e-19`.
- Twelve-step chain enumeration: pass.
- Strict cluster threshold: pass.
- Cross-stage targets and branching constants: agree.

## Frontier audit

- Complete physical SU(2) retained kernel: open.
- Physical vacuum identification: open.
- Uniform root moment and inverse-amplitude control: open.
- One-scale basin entry: open.
- Repeated RG and continuum OS gap: open.

## Document

- Compilation: pass after three `latexmk` runs.
- PDF: 7 letter-size pages, 231459 bytes.
- Stable PDF SHA-256:
  `4413651cba04c0b310e8e977b99df6710ac91a4acf8e84ddbeca9120a8e875c3`.
- Extracted text: pass, 2142 words.
- Undefined references and multiply defined labels: zero.
- Overfull boxes: zero.
- Underfull boxes: four, confined to narrow audit-table cells.
- Visual inspection: pages 1, 3, 6, and 7 pass with no clipping, overlap,
  malformed equations, or unreadable text.
- Machine-readable build and lint reports are stored under `build/`; rendered
  audit images are stored under `previews/`.
