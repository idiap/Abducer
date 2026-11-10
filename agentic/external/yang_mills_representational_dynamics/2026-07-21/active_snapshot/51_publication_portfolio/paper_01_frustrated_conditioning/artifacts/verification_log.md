# Verification log

Date: 21 July 2026.

| Gate | Result |
|---|---|
| New exact incidence verifier | 5/5 tests passed for dimensions 2–6 |
| Legacy SU(2) obstruction calibration | 17/17 tests passed; numerical results remain non-theorem-critical |
| Strict manuscript lint | passed; 0 errors, 0 narrative warnings |
| LaTeX/BibTeX compilation | passed |
| Unresolved citations/references | 0 |
| Overfull boxes | 0 |
| PDF pages | 21 |
| Extracted text | 48,476 characters |
| PDF visual inspection | first, middle, and last pages clean; no clipping, overlap, broken glyphs, or unreadable tables |
| Manuscript JSON parse | all JSON files valid |
| Exact-computation trust boundary | standard library; integers and GF(2); analytic proof available independently |
| Submission ZIP integrity | passed with `unzip -t` |

Hashes:

```text
a2f339a7bad9b02c5ec9c53973ac09006c530ffc7311effd39d3a10c4063812a  build/main.pdf
d4b16a8b28db75ca2d2b4b029ecb72c904cb513735b661a69d9cadbc051285ea  supplement/verify_incidence.py
a7baf5f70d512baac190ae7326e3afc55f25c987fd61819b439a283744e5915b  supplement/incidence_certificate.json
```

Underfull boxes in narrow table cells were visually reviewed and accepted; they do not create clipping or overflow.
