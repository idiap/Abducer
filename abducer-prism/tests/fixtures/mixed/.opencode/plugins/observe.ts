export const Observe = async () => ({
  event: async ({ event }) => {
    if (event.type === "session.idle") return
  },
})
