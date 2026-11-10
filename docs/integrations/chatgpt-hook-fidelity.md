<!-- SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch> -->
<!-- SPDX-License-Identifier: MIT -->
# Exporting Abducer workflow hooks

Export the native policy implementation together with its dependencies and a
verifiable execution contract. For personal online ChatGPT, enforce these hooks
inside the Abducer executor. The plugin's installed files alone cannot enforce
the workflow in that environment. Supported local Codex/Work sessions can add
trusted host lifecycle adapters, with different event and output contracts.

This distinction follows the current [host hook documentation](https://learn.chatgpt.com/docs/hooks)
and [cloud orchestration restrictions](https://learn.chatgpt.com/docs/enterprise/managed-configuration#agent-security-and-local-computer-access-with-work-cloud),
checked on 2026-10-26. A native hook export is not an installation or host-hook
activation, and this guide does not claim either has happened.

## The exported native baseline

The generated `plugins/abducer-chatgpt/native-hook-runtime/` package contains
the original configuration, all helper scripts, original task registries, the
existing dispatcher, a hash manifest and a fidelity contract. The generator
binds the contract and bundle hashes in `release.json`. It does not register the
native list-form configuration as a host's object-form `hooks/hooks.json`.

The hash inventory also preserves dormant COHERE helper modules that are not
registered by the native configuration. Their additional dependencies are not
included or activated by this five-event bundle. Dependency completeness applies
to the configured native hook entrypoints, not every dormant module or workflow.

| Native hook | Behavior preserved | What it does not establish |
| --- | --- | --- |
| `UserPromptSubmit` | Warns on controlled-navigation language and suggests the original intake skill. | A warning does not instantiate a target or run an intake workflow. |
| `PreSkillUse` | Checks controlled skill membership in the original visible-workflow registry. | Membership is not proof of step order, satisfied prerequisites or full DAG execution. |
| `PreToolUse` | Applies original command blocks and protected-path warnings to native payload fields. | It does not inspect every possible effect or uninstrumented external tool. |
| `PostSkillUse` | Warns when declared expected artifacts are absent. | Artifact presence is not content validation; a native warning remains a warning. |
| `Stop` | Checks the original controlled-iteration Looper artifact requirements. | Presence is not proof completeness or verified scientific truth. |

Preserve the canonical `accept`, `warn` and `block` result, including an exit-zero
script returning `block`. The dispatcher binds source, payload and native trace
hashes and adds a separate receipt journal. It retains native latest-trace
behavior. The complete original `registry/tasks` namespace is required because
the pre-skill hook computes membership across it.

Keep `hooks/workflow_local` and `registry/optional-tasks` outside this baseline.
Their activation and completion rules are separate policies. Enabling stronger
checks would change the workflow semantics and must be represented as a distinct
profile.

## Generate and inspect the package

From the repository root, generate a reproducible source ZIP:

```sh
.venv/bin/python -m integrations.chatgpt.generate_plugin \
  --output /tmp/abducer-hook-export \
  --archive /tmp/abducer-hook-export.zip
.venv/bin/python -m integrations.chatgpt.generate_plugin \
  --output /tmp/abducer-hook-export --check
```

The source export is deliberately unconfigured. To connect this five-skill client,
provide the actual standalone Python service `/mcp` endpoint with `--endpoint`.
The already provisioned Sites plugin has its own tool contract; pointing this
standalone client at Sites does not convert it. Both can use the same canonical
native source and policy implementation.

Validate an extracted hook bundle:

```python
from pathlib import Path
from integrations.chatgpt.hook_export import validate_bundle

manifest = validate_bundle(Path("/tmp/abducer-hook-export/native-hook-runtime"))
print(manifest["bundle_digest"])
```

Digest validation detects corruption or drift relative to the manifest. Authenticity
requires comparing the bundle digest to a release obtained through a trusted
channel; an attacker replacing files and their manifest is not authenticated by
that manifest. Execute only trusted native source. Supply a separate writable
research workspace and actual workflow inputs/artifacts; the bundle is not the
entire scientific runtime.

## Additional hooks for a supported local host

These adapters are a recommended separate profile, not registered by the native
export. Use [the plugin manifest extension](https://developers.openai.com/plugins/build/plugins#configure-installed-server-policy)
and review/trust the resulting definition before running it. `PLUGIN_ROOT` locates
installed code; `PLUGIN_DATA` locates adapter-owned writable metadata.

| Host event | Recommended role | Required distinction |
| --- | --- | --- |
| `SessionStart` | Restore workflow/target/source identity, current step, artifact pointers and pending model request on start, resume or compaction. | Restore recorded state; do not reconstruct a successful checkpoint from chat prose. |
| `UserPromptSubmit` | Preserve actual user intent and call the native intake policy for an explicitly active Abducer invocation. | A synthesized execution prompt is not the original user prompt. |
| `PreToolUse` | Check a translated native command/path payload before a supported effect. | Flatten real `tool_input` fields; do not treat a tool call as a skill invocation. |
| `PostToolUse` | Reconcile actual result/receipt state after supported effects. | It cannot roll back effects or stand in for native `PostSkillUse`. |
| `PreCompact` | Persist bounded workflow context for restoration through `SessionStart`. | Compaction hooks do not document an `additionalContext` output channel. |
| `SubagentStart` / `SubagentStop` | Bind delegated scope and collect explicit handoff receipts. | These are delegation events, not native skill lifecycle events. |
| `Interrupt` | Persist an interruption marker within the host's short deadline. | It cannot prevent interruption or claim successful workflow completion. |
| `Stop` | Report missing obligations and optionally request bounded continuation. | Host `block` requests another model turn; the native executor still controls completion admission. |

Scope all adapters to an explicitly active Abducer session/workspace. Host prompt
and stop events do not honor matchers, and a globally installed plugin must not
apply Looper completion requirements to unrelated tasks. Matching handlers can
run concurrently; receipt identities and state updates must tolerate concurrency.

Whitelist native payload fields rather than forwarding the host envelope. The
original evidence-marker helper scans serialized payload text; metadata keys such
as `permissionDecision` could otherwise accidentally satisfy its evidence rule.
Translate a native `warn` into nonblocking host feedback, and native pre-tool
`block` into the supported host denial shape. An unknown or malformed host output
can fail to block. Do not infer a skill invocation from arbitrary tool names.

MCP hook connection errors, missing tools and timeouts can allow the operation
to proceed. Some hosted tools also bypass local tool hooks. For this reason the
native executor's synchronous admission and validation checks remain authoritative.
The [public submission guide](https://developers.openai.com/plugins/guides/submit-claude-plugin#review-what-openai-supports)
also requires a separate distribution path for lifecycle-hook-dependent packages.

## Current execution gaps

The exported sources are preserved; complete execution parity is not established.
The current Marathon adapter supplies a synthesized `UserPromptSubmit` prompt,
so original language-dependent intake warnings can differ. Its final
`PostSkillUse`/`Stop` calls run on the normal completion path; exceptions and
process cancellation can omit them. Instrumented effect boundaries are a subset
of all filesystem and external effects. Only actual declared skill invocations
receive native skill hooks. Other workflow executors remain individually gated.

To close these gaps, bind actual invocation intent to the prepared plan, add
explicit failure/interruption lifecycle handling without fabricating post-skill
success, and compare each adapter's event trace against native allowed, rejected,
interrupted and resumed cases. Treat these as runtime changes with independent
acceptance evidence. Adding hook names to an export manifest cannot establish
those guarantees.
