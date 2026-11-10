<!--
SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>

SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
Neuro-symbolic AI Group

SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
Neuro-symbolic AI Group

SPDX-License-Identifier: MIT
-->
# Provider support snapshot

Profile schema: `1`
Profile facts retrieved: `2026-08-19`

This document records the primary-source basis for the bundled provider
profiles. Vendor documentation is mutable and generally does not publish a
machine-readable hook-schema version. The date-stamped `profile_version` is
therefore a reviewed documentation snapshot, not a claim about a vendor CLI
release number. A profile update must update its fixture and conformance tests
in the same change.

## Support boundary

| Provider | Project contracts inventoried | Native hook contract | Guard frontend | Prism runtime disposition |
| --- | --- | --- | --- | --- |
| Codex | `AGENTS.md`, `.codex/config.toml`, `.codex/agents/*.toml`, `.agents/skills/*/SKILL.md`, rules and MCP declarations | `hooks.json` or inline `[hooks]` tables | Declarative command hooks | Typed Codex hooks can be built and Codex activation requires separate runtime evidence |
| Claude Code | `CLAUDE.md`, project settings, skills, agents, legacy commands, rules, `.mcp.json`, plugin manifests | `hooks` in settings, plugin `hooks/hooks.json`, or skill/agent frontmatter | Declarative command hooks | Typed Claude hooks can be preserved; native activation is not established by the current Prism runner |
| OpenCode | `opencode.json[c]`, agents, commands, plugins, tools, skills, compatible skill locations and MCP declarations | JavaScript/TypeScript plugin callbacks | Executable TypeScript plugin adapter | No `Hooks[OpenCode]` or OpenCode Prism model adapter; executable plugin semantics remain explicit debt |
| Open Agent Skills | Any `SKILL.md` boundary and its resources | None | None | Compatible script-free skills may be built after contract review |

Discovery is additive. Shared layouts intentionally return more than one
provider owner: `.claude/skills` is native Claude Code and OpenCode-compatible;
`.agents/skills` is native to the current Codex skill contract and also
OpenCode-compatible. The inventory layer must retain both facts and resolve
workflow ownership later from configuration and evidence.

## Codex

Primary sources:

- [Hooks](https://developers.openai.com/codex/hooks/) (official OpenAI page,
  retrieved 2026-08-19; currently redirects to ChatGPT Learn)
- [Build skills](https://developers.openai.com/codex/skills/) (official OpenAI
  page, retrieved 2026-08-19)
- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md/)
  (official OpenAI page, retrieved 2026-08-19)
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
  (official OpenAI documentation, retrieved 2026-08-19)
- [MCP](https://learn.chatgpt.com/docs/extend/mcp) (official OpenAI
  documentation, retrieved 2026-08-19)

Codex reads project hooks from `.codex/hooks.json` and inline `[hooks]` tables
in `.codex/config.toml`; it merges hook sources rather than applying ordinary
config replacement. The documented events in this snapshot are
`SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `PreToolUse`,
`PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`,
`UserPromptSubmit`, and `Stop`. Only exact names are accepted by the profile.

The hook shape is event -> matcher group -> handler list. Matchers are regular
expressions, but `UserPromptSubmit` and `Stop` do not support matching.
`command` is the only currently executed handler type; `prompt` and `agent` are
parsed and skipped. Commands run with the session working directory, multiple
matching command hooks start concurrently, project hooks require trust, and
non-managed hook changes require renewed trust. Async command hooks cannot
block or rewrite the triggering action.

Codex currently discovers repository skills under `.agents/skills` while
instruction layering uses `AGENTS.override.md` before `AGENTS.md` at each
applicable directory. Project custom agents are TOML files in
`.codex/agents/`; their required semantic fields are `name`, `description`,
and `developer_instructions`. MCP servers are configured in project or user
`config.toml` under `mcp_servers`.

The shipped guard config uses only command handlers and the exact documented
events `PreToolUse`, `PermissionRequest`, `PostToolUse`, and `Stop`. It calls an
installed logical command, not a checkout-relative script.

## Claude Code

Primary sources:

- [Hooks reference](https://code.claude.com/docs/en/hooks) (Anthropic,
  retrieved 2026-08-19)
- [Explore the .claude directory](https://code.claude.com/docs/en/claude-directory)
  (Anthropic, retrieved 2026-08-19)
- [Extend Claude with skills](https://code.claude.com/docs/en/slash-commands)
  (Anthropic, retrieved 2026-08-19)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
  (Anthropic, retrieved 2026-08-19)
- [Settings](https://code.claude.com/docs/en/configuration) (Anthropic,
  retrieved 2026-08-19)
- [MCP](https://code.claude.com/docs/en/mcp) (Anthropic, retrieved 2026-08-19)

Claude Code project hooks live under `hooks` in `.claude/settings.json` (or
the non-shareable `.claude/settings.local.json`). There is explicitly no
standalone `.claude/hooks.json`. A distributable plugin can use
`hooks/hooks.json`; skills and subagents can scope the same hook structure in
frontmatter.

The profile enumerates the current reference event set instead of reducing it
to the older subset understood by Prism's existing hook builder. It also
records all five current handler categories: `command`, `http`, `mcp_tool`,
`prompt`, and experimental `agent`. Exact native preservation and executable
Prism activation are different claims: recognizing a newer Claude event does
not mean the current Prism CLI can build or activate it.

Claude project assets include `CLAUDE.md`, `.claude/rules`, skills, agents,
commands, settings, and `.mcp.json`. Local settings and `CLAUDE.local.md` are
private/local scope and are inventoried without an assumption that they may be
vendored.

## OpenCode

Primary sources:

- [Configuration](https://opencode.ai/docs/config/) (OpenCode, retrieved
  2026-08-19)
- [Plugins](https://opencode.ai/docs/plugins/) (OpenCode, retrieved 2026-08-19;
  page reports last update 2026-08-19)
- [Agents](https://opencode.ai/docs/agents/) (OpenCode, retrieved 2026-08-19)
- [Commands](https://opencode.ai/docs/commands/) (OpenCode, retrieved
  2026-08-19)
- [Agent Skills](https://opencode.ai/docs/skills/) (OpenCode, retrieved
  2026-08-19)
- [MCP servers](https://opencode.ai/docs/mcp-servers/) (OpenCode, retrieved
  2026-08-19)
- [Tools](https://opencode.ai/docs/tools/) (OpenCode, retrieved 2026-08-19)

OpenCode supports JSON and JSONC project configuration. Current project
directories use plural names (`agents`, `commands`, `plugins`, `skills`,
`tools`); singular directories remain backward-compatible. Skills are also
discovered from `.claude/skills` and `.agents/skills`.

OpenCode does not expose a declarative hook configuration corresponding to
Codex or Claude `hooks.json`. Local `.js` or `.ts` plugin modules return
callbacks such as `tool.execute.before`, `tool.execute.after`, `shell.env`, and
an `event` subscriber. Those modules are arbitrary executable code and must
never be imported during inspection. The full documented event vocabulary is
stored in the profile for exact-name evidence, but a computed callback key or
unknown event stays `opaque_executable`, not a guessed nearest event.

The optional OpenCode guard frontend is itself an explicit TypeScript plugin.
It forwards the two tool lifecycle callbacks and `session.idle` to the same
installed logical guard command as other frontends. Failure to launch the
command, malformed behavior, or nonzero exit throws and therefore fails the
intercepted operation closed. This frontend does not imply that arbitrary
source plugins can be translated automatically.

## Updating a profile

1. Re-read only official provider documentation and record retrieval date and
   exact URLs.
2. Diff layouts, precedence, event names, matcher semantics, handler types,
   input/output control, trust, cwd, concurrency, and timeout behavior.
3. Add or update a realistic fixture. Unknown constructs must first produce an
   unsupported or opaque disposition.
4. Update the profile version and tests in one change.
5. Re-evaluate the separate Prism build and activation capability matrix.

Do not infer one provider from another, fuzzy-match event names, execute a
plugin to discover its callbacks, or treat static recognition as native
activation evidence.
