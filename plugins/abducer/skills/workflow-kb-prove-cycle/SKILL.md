---
name: workflow-kb-prove-cycle
description: Inspect the kb_prove_cycle_workflow workflow contract, native steps, source owner and unresolved execution gaps. Use when this normalized workflow or its source mapping is requested; native execution retains its original activation gates.
---

# kb_prove_cycle_workflow

This entry exposes `abducer:kb_prove_cycle_workflow@1.0.0`.
The packaged `../../workflows.json` contains its complete contract. The MCP
`get_workflow` tool, resource `abducer://workflows/kb_prove_cycle_workflow` and prompt
`kb_prove_cycle_workflow` expose the same contract without requiring a checkout.

To inspect the canonical checkout source, run:
`python3 "<this-skill-directory>/../../scripts/resolve_checkout.py"
--workflow kb_prove_cycle_workflow`. Set `ABDUCER_ROOT` or add `--root "/path/to/abducer"`
when outside the checkout. Read the returned `workflow_file` and `skill_file`
in full; resolve relative paths from those original source directories.

This contract is draft and interface-only. Normalized execution adapters are
unavailable. Explain source steps, conditions, artifacts, authority and gaps;
do not treat inspection as workflow execution or approval. Stop checkout routing
if resolution fails and report its setup/version error; the packaged contract
remains available for inspection.

If the user explicitly requests native execution, follow the canonical owning
skill `skills/discovery/kb-prove-cycle/SKILL.md` in the resolved checkout and preserve its activation,
target, domain receipt, budget and evidence gates. Loading this entry does not
satisfy opt-in or private-domain prerequisites. Write research artifacts only
in the checkout, never in the installed plugin cache. No normalized adapter,
scientific validity, proof, publication or promotion authority is added here.
