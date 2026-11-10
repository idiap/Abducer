---
name: pvsnp-forcedrows-proof-workflow
description: Deliver the P vs NP EF+SAT_U occurrence-row ForcedRows proof packet. Use when the highest-priority P vs NP queue item asks to formalize Psys=EF+SAT_U^{occ}, extract Q_pi from a proof transcript, define ForcedRows(Q_pi), prove acceptance transcript invariance under private occurrence-label perturbations A_Q, and decide whether the beta-zero XOR row-forcing obstruction becomes a scoped no-go theorem or a blocked extraction obligation for full EF+SAT_U.
---

# pvsnp-forcedrows-proof-workflow

This entry uses the canonical Abducer skill `skills/proof_delivery/pvsnp-forcedrows-proof-workflow/SKILL.md` in a writable
Abducer checkout. The installed plugin contains routing instructions, not the
research runtime.

1. Locate this installed SKILL.md, then run the read-only resolver beside the
   plugin: `python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
   --skill pvsnp-forcedrows-proof-workflow`. It uses `ABDUCER_ROOT` when set, otherwise searches
   the current directory and its parents. An explicit checkout can be passed
   with `--root "/path/to/abducer"`. Quote paths, including paths with spaces.
2. If resolution fails, stop this route and report the resolver's error. Request
   a checkout path or the documented runtime setup; do not fabricate outputs.
3. Read the returned `skill_file` in full. Follow that canonical procedure and
   resolve its relative scripts and references from its original skill directory.
4. Execute repository-relative commands with the returned `root` as working
   directory. Preserve the source skill's target, budget, evidence, claim-status
   and validation gates. Write research artifacts only in the selected checkout,
   never in the installed plugin cache.

When the procedure names a public companion skill, use the matching entry in
this plugin, or read its canonical source in the same checkout. Domain-private
skills remain accessible only through their canonical activation procedure;
generic domain prose does not authorize an opt-in workflow.
