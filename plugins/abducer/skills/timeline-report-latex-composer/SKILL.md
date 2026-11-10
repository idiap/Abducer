---
name: timeline-report-latex-composer
description: Compose timeline report tabs into a coherent LaTeX packet by coordinating timeline-cycle-latex-translator, timeline-story-latex-translator, timeline-problem-literature-latex-translator, and timeline-summary-latex-translator. Use when full timeline report content including timeline, story, problem/literature, summary, queue, and contribution state must become TeX sections or a paper draft input.
---

# timeline-report-latex-composer

This entry uses the canonical Abducer skill `skills/reporting/timeline-report-latex-composer/SKILL.md` in a writable
Abducer checkout. The installed plugin contains routing instructions, not the
research runtime.

1. Locate this installed SKILL.md, then run the read-only resolver beside the
   plugin: `python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
   --skill timeline-report-latex-composer`. It uses `ABDUCER_ROOT` when set, otherwise searches
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
