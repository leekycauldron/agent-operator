# ElevenLabs Agent Setup

Files to configure your ElevenLabs conversational agent.

## Files

- **system-prompt.md** — Copy into your agent's system prompt
- **tool-clawdbot-task.json** — Tool schema for task dispatch back to Clawdbot

## Setup Steps

### 1. Create Agent

Go to [ElevenLabs](https://elevenlabs.io) → Conversational AI → Create Agent

### 2. Configure Voice

Pick a voice that fits the Operator persona.

### 3. Set System Prompt & First Message

Copy the contents of `system-prompt.md` into the agent's system prompt field.
Copy the contents of `first-message.md` into the agent's first message field.

### 4. Add Webhook Tool

Add a **webhook tool** using `tool-clawdbot-task.json`. You can import it directly or copy the values.

**Important:** Replace `YOUR_WEBHOOK_URL` with your endpoint that bridges to Clawdbot.

ElevenLabs will POST `{ "task": "..." }` to this URL and expect a response. You need an adapter that:
1. Receives the task from ElevenLabs
2. Sends it to Clawdbot (via chat completions API or similar)
3. Returns the result

See `adapter/` folder for a ready-to-use Python adapter, or build your own with:
- n8n workflow
- Cloud function (AWS Lambda, Cloudflare Worker, etc.)

### 5. Get Agent ID

Copy the Agent ID from the agent settings — you'll need this for `ELEVENLABS_AGENT_ID`.

## Notes

- The tool webhook calls back to Clawdbot to execute tasks
- Your Clawdbot gateway needs to be accessible from ElevenLabs (public URL or tunnel)
- For local testing, you can use ngrok or similar to expose your gateway
