# Verification log

Date: 21 July 2026

| Check | Result |
|---|---|
| exact representation certificate | pass; `all_checks_pass: true` |
| unit tests | 13/13 pass |
| arithmetic | integers and `fractions.Fraction` only |
| strict narrative/source lint | 0 errors, 0 warnings |
| LaTeX build | pass |
| labels / references / citation keys | 39 / 44 / 50 |
| unresolved references or citations | 0 |
| overfull boxes | 0 |
| PDF pages | 27 |
| extracted characters / words | 76,016 / 12,505 |
| PDF bytes | 423,956 |
| PDF SHA-256 | `e32b2e3228399efd32d93533cfd501086322e8d7f20508cf20151a95c33580c4` |
| verifier SHA-256 | `f56f016998b04f0d1b25b68c8bdfabfd4db793e910f9d0cbbf3a5273bf911e13` |
| certificate JSON SHA-256 | `bea062cefd67631ecfe7dc3e3218bec3d69c4a52b54ab46d9d95cd688e5b34af` |

The renderer's first automated handoff produced a truncated copy after a valid
compile. The final artifact was rebuilt in a fresh one-use output directory,
copied only after compilation completed, and then checked by `pdfinfo`,
checksum, text extraction, log scan, and page rendering.
