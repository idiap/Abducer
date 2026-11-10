import { tool } from "@opencode-ai/plugin"

export default tool({
  description: "Convert a named severity to a numeric fixture score",
  args: { severity: tool.schema.string() },
  async execute({ severity }) {
    return severity === "high" ? "3" : severity === "medium" ? "2" : "1"
  },
})
