<!-- Paste this into your HEARTBEAT.md -->

## Operator Context Sync

Sync workspace context to the Operator voice agent's knowledge base.

**On each heartbeat:**
1. Read today's memory: `memory/YYYY-MM-DD.md` (use current date)
2. Read long-term memory: `MEMORY.md`
3. Check for active projects or recent work in the workspace
4. Compile a concise context snapshot:
   - What I'm currently working on
   - Recent decisions or blockers
   - Pending tasks or reminders
   - Anything useful for a quick voice conversation
5. Push the context to ElevenLabs using the Operator skill instructions

Keep it concise — the voice agent needs quick-reference info, not full transcripts.
