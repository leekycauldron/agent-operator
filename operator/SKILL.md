---
name: operator
description: Syncs workspace context to an ElevenLabs voice agent knowledge base, enabling ambient-aware voice conversations.
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["ELEVENLABS_API_KEY","ELEVENLABS_AGENT_ID"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# Operator Skill

Sync your workspace context to an ElevenLabs voice agent so it knows what you're working on.

## When to Use

This skill activates during heartbeat when the `Operator Context Sync` section is in your HEARTBEAT.md. On each heartbeat, you'll gather context and push it to the ElevenLabs knowledge base.

## Setup

Install dependencies:

```bash
pip install -r {baseDir}/requirements.txt
```

## Environment Variables

- `ELEVENLABS_API_KEY` — Your ElevenLabs API key
- `ELEVENLABS_AGENT_ID` — The ID of your ElevenLabs conversational agent

## Context Sync Process

### Step 1: Gather Context

Read and compile a context snapshot from:
- Today's memory: `memory/YYYY-MM-DD.md`
- Long-term memory: `MEMORY.md`
- Active projects or recent work in workspace

Format it as a concise briefing the voice agent can reference:

```
## Current Context (synced YYYY-MM-DD HH:MM)

### Active Work
- [what you're working on]

### Recent Decisions
- [any recent decisions or direction changes]

### Blockers / Notes
- [anything notable]

### Pending Tasks
- [tasks or reminders]
```

### Step 2: Sync to ElevenLabs

Run the sync script with your compiled context:

```bash
echo "<your compiled context>" | python3 {baseDir}/scripts/sync-context.py
```

Or pass it as an argument:

```bash
python3 {baseDir}/scripts/sync-context.py "<your compiled context>"
```

The script deletes old context documents, uploads the new context, and attaches it to your agent.

## Notes

- Keep context concise — the voice agent needs quick-reference info, not full transcripts
- The knowledge base has a 300k character limit (non-enterprise)
