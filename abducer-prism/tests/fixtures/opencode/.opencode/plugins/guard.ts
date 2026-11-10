import type { Plugin } from "@opencode-ai/plugin"

export const ReadOnlyGuard: Plugin = async () => ({
  "tool.execute.before": async (input) => {
    if (["write", "edit", "apply_patch"].includes(input.tool)) {
      throw new Error("fixture is read-only")
    }
  },
  event: async ({ event }) => {
    if (event.type === "session.idle") {
      // Observable lifecycle point for the fixture oracle.
    }
  },
})
