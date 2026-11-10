---
description: Read-only source auditor
mode: primary
permission:
  edit: deny
  bash:
    "*": ask
    "git diff *": allow
---

Inspect the requested files and return evidence-backed risks.
