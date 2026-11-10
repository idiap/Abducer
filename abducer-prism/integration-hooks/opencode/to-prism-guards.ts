// SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
//
// SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
// Neuro-symbolic AI Group
//
// SPDX-License-Identifier: MIT
import type { Plugin } from "@opencode-ai/plugin"

// This frontend contains no conversion policy. It only adapts OpenCode's
// executable plugin callbacks to the provider-neutral installed guard command.
async function runGuard(event: string, payload: unknown): Promise<void> {
  const process = Bun.spawn(
    ["to-prism", "guard", "--provider", "opencode", "--event", event],
    {
      stdin: new Blob([JSON.stringify(payload)]),
      stdout: "pipe",
      stderr: "pipe",
    },
  )
  const exitCode = await process.exited
  if (exitCode !== 0) {
    const reason = (await new Response(process.stderr).text()).trim()
    throw new Error(reason || `to_prism guard rejected ${event}`)
  }
}

export const ToPrismGuards: Plugin = async () => ({
  "tool.execute.before": async (input, output) => {
    await runGuard("tool.execute.before", { input, output })
  },
  "tool.execute.after": async (input, output) => {
    await runGuard("tool.execute.after", { input, output })
  },
  event: async ({ event }) => {
    if (event.type === "session.idle") {
      await runGuard("session.idle", { event })
    }
  },
})
