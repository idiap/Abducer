---
name: kb-macro-proof-paper-writer
description: Write the current macro-proof state as a mathematical paper-style narrative grounded in the main conjecture, and render it as Markdown, LaTeX, and PDF. Use when the user asks for a conjecture-centered current-state note, a macro-proof paper for a problem such as P vs NP, or a publication-style synthesis of the leading route, supporting routes, and proof frontier.
---

# kb-macro-proof-paper-writer

This entry uses the canonical Abducer skill `skills/reporting/kb-macro-proof-paper-writer/SKILL.md` in a writable
Abducer checkout. The installed plugin contains routing instructions, not the
research runtime.

1. Locate this installed SKILL.md, then run the read-only resolver beside the
   plugin: `python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
   --skill kb-macro-proof-paper-writer`. It uses `ABDUCER_ROOT` when set, otherwise searches
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
