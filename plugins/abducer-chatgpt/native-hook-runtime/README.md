# Native Abducer hook bundle

This bundle preserves the original five registered lifecycle checks, their shared
helper, and the exact `registry/tasks` membership files. Scripts keep their bytes
and original workspace-relative paths. The existing dispatcher is included as
`runner/native_hooks.py`; `hook-contract.json` describes its decision semantics.
The manifest binds every included file and the native source digest.

## Use from an executor

1. Authenticate the package and its expected bundle digest through your release
   channel. In the Abducer checkout, call
   `integrations.chatgpt.hook_export.validate_bundle(bundle_root, expected_digest=...)`
   before importing the exported runner. A self-consistent manifest is not proof
   of who supplied the code.
2. Keep `source/` immutable. Create a separate writable research workspace containing
   identical hook/registry files and the original workflow's own dependencies and
   state. Python 3.10+ with POSIX `fcntl` is required for the dispatcher.
3. Import `NativeHookDispatcher` from the exported runner, construct it with
   `source_root=<bundle>/source` and `workspace=<research-workspace>`, and explicitly
   call `require(event, payload)` at the appropriate executor boundaries.

For example, `require("PreToolUse", {"command": "rm -rf scratch"})` raises
`NativeHookBlocked` even though the original script exits successfully. A missing
artifact in `require("PostSkillUse", {"expected_artifacts": ["missing.json"]})`
retains the original warning and permits continuation. `dispatch(...)` returns a
receipt for inspection; the caller must enforce it or use `require(...)`.

`PreSkillUse` checks the union of `visible_workflows[].composed_skills[]` from the
native task registry. It does not enforce step order or workflow activation.
Controlled `Stop` requires the five original Looper artifact paths documented in
the contract. Presence of those files is not scientific validation. The executor
owns trusted `controlled`, skill, command and artifact payload values.

Native latest traces and the append-only receipt journal are written only in the
writable workspace. No existing research state, credentials or traces are copied.
Optional `hooks/workflow_local` and `registry/optional-tasks` remain excluded.
Two unregistered COHERE scripts are preserved for native source-digest parity.
They are not activated: their PyYAML and external registry dependencies are not
part of this hook-only bundle.

## Host and workflow boundaries

This is not a ChatGPT host hook manifest or a complete workflow installation.
The native list-form `hooks.json` and its `PreSkillUse`/`PostSkillUse` events must
not be installed directly as host hooks. An explicit host adapter would need to
translate `tool_input.command` into native `command`, map native decisions to
event-specific host responses, and handle host availability and trust review.
There is no automatic personal online ChatGPT hook registration in this package.

The current hosted Marathon adapter supplies a synthesized intake prompt. Error
and cancellation exits can omit finish-time `PostSkillUse` and `Stop` calls. Source
preservation does not establish all-exit coverage or execution parity across all
workflows; use runtime capability evidence for the actual deployment.
