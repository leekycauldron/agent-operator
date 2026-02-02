# Agent Operator

A Clawdbot skill that syncs your workspace context to an ElevenLabs voice agent. Call in and it already knows what you're working on.

## How It Works

1. **Heartbeat syncs context** — Every 30 minutes (or whatever the interval is for your heartbeat; default=30mins), Clawdbot reads your memory files and workspace state, then pushes a context snapshot to ElevenLabs
2. **You call in** — Talk to your Operator voice agent via web widget or phone
3. **It already knows** — No briefing needed, it has your latest context from the last sync

## Prerequisites

- [Clawdbot](https://github.com/clawdbot/clawdbot) installed and running
- [ElevenLabs](https://elevenlabs.io) account with API access
- An ElevenLabs conversational agent created (you'll need the agent ID)
- Python 3 with pip

## Installation

### 1. Copy the skill

Copy the `operator/` folder to your skills directory:

```bash
# Workspace-level (recommended)
cp -r operator/ /path/to/your/workspace/skills/operator/

# Or user-level
mkdir -p ~/.clawdbot/skills
cp -r operator/ ~/.clawdbot/skills/operator/
```

### 2. Install dependencies

```bash
pip install -r /path/to/skills/operator/requirements.txt
```

### 3. Set environment variables
```json
{
  "skills": {
    "entries": {
      "operator": {
        "enabled": true,
        "env": {
          "ELEVENLABS_API_KEY": "your-api-key",
          "ELEVENLABS_AGENT_ID": "your-agent-id"
        }
      }
    }
  }
}
```

### 4. Add heartbeat section

Paste the contents of `HEARTBEAT-OPERATOR.md` into your workspace's `HEARTBEAT.md` file.

## Creating Your ElevenLabs Agent

See `elevenlabs/README.md` for detailed setup, or quick version:

1. Go to [ElevenLabs](https://elevenlabs.io) → Conversational AI → Create Agent
2. Configure voice (professional, calm)
3. Copy system prompt from `elevenlabs/system-prompt.md`
4. Add custom tool from `elevenlabs/tool-clawdbot-task.json` (update webhook URL)
5. Copy the Agent ID → use for `ELEVENLABS_AGENT_ID`

## Usage

Once set up, the skill runs automatically on each heartbeat. Clawdbot will:

1. Read your memory files (`memory/YYYY-MM-DD.md`, `MEMORY.md`)
2. Compile a context snapshot
3. Push it to your ElevenLabs agent's knowledge base

Then just call your Operator — it knows what you're working on.

## Files

```
operator/
├── README.md                 # This file
├── HEARTBEAT-OPERATOR.md     # Paste into your HEARTBEAT.md
├── adapter/                  # ElevenLabs → Clawdbot bridge
│   ├── README.md
│   ├── adapter.py
│   └── requirements.txt
├── elevenlabs/               # ElevenLabs agent setup
│   ├── README.md
│   ├── system-prompt.md      # Operator persona
│   ├── first-message.md      # Agent's greeting
│   └── tool-clawdbot-task.json  # Task dispatch tool
└── operator/                 # The skill (copy to skills/)
    ├── SKILL.md
    ├── requirements.txt
    └── scripts/
        └── sync-context.py
```

## License

MIT
