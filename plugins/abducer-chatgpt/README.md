# Abducer hosted plugin

Generated profile; edit `integrations/chatgpt/generate_plugin.py`, not this directory. The canonical research library stays in Abducer; these five skills coordinate authenticated tools.

This source profile is **unconfigured** and cannot connect until a real service is deployed.

Generate a release with `python -m integrations.chatgpt.generate_plugin --endpoint https://YOUR_HOST/mcp --output /path/to/release`. Use the actual deployed hostname. Verify the same output with `--check` and the same endpoint. Never include credentials or private datasets. Keep the existing `plugins/abducer` for checkout-backed clients.

Install the configured package, connect the named account through OAuth, run setup, select a project, and inspect capabilities. Source visibility does not authorize execution. The service enforces currentness, permissions and budgets.

## Preserved workflow hooks

`native-hook-runtime/` contains the original five-event configuration, scripts, helpers, membership registries, dispatcher, a hash manifest and an explicit fidelity contract. Read `native-hook-runtime/README.md` before use. These are native runtime sources; they are not registered as host lifecycle hooks. Their source preservation does not imply that all workflow events or exits have been instrumented. An authenticated runtime must supply the real workspace, inputs and canonical artifacts. The hook bundle alone cannot execute a scientific workflow.

For a run presented as preserving native hooks, check the current worker's `native_hooks_enabled` and the selected workflow's coverage. Inspect the actual run's `native_hook_coverage` and receipts afterward. Report absent or incomplete coverage explicitly. Keep native `warn` distinct from `block`; enabling the optional workflow-local policies would be a separate policy change.

The default five entry skills target the standalone Python service (`get_capabilities`). The separately provisioned Sites plugin uses `get_execution_capabilities`; do not reconfigure this client to Sites without adapting its tool contract. Exporting this package does not install scripts in online ChatGPT.

Optional local host integration must use the host event schema and reviewed/trusted hooks. Native `PreSkillUse`/`PostSkillUse` remain runtime events. Personal cloud orchestration does not load plugin lifecycle hooks. Public directory submission of hook-dependent packages has separate restrictions. See [official hook documentation](https://learn.chatgpt.com/docs/hooks).
