# Provider contract fixtures

These are synthetic, redistributable fixtures modeled directly on the official
provider documentation recorded in `references/provider-support.md`. They are
not copies of third-party projects and contain no credentials.

- `codex/`: instructions, project TOML, native hooks, a custom agent, a skill,
  and an environment-bound MCP declaration.
- `claude/`: instructions, settings hooks and permissions, a subagent, a legacy
  command, a skill, and `.mcp.json`.
- `opencode/`: JSON configuration, permissions and MCP, an agent, command,
  executable plugin callback, skill, and custom tool.
- `mixed/`: overlapping `.claude/skills` and `.agents/skills` compatibility
  layouts plus exact native hooks/plugins for ownership-conflict tests.

The matching plans in `../provider-pilots/` enumerate every profile-recognized
inventory item, its primary kind/provider, and any expected compatible owners.
The integration suite requires exact coverage, so adding a provider artifact
without updating its pilot fails visibly. Native baselines remain explicitly
unavailable for these synthetic, non-executing discovery fixtures.

Commands and modules named by the fixtures are inventory data only. Discovery
tests must not execute them. Fixture profile date: `2026-08-19`.
