# Adapter

Bridges ElevenLabs webhook calls to Clawdbot's main session (preserves full context).

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export CLAWDBOT_URL="http://localhost:18789"  # default
   export CLAWDBOT_TOKEN="your-token"            # if auth enabled
   export ADAPTER_PORT="8080"                    # default
   export SESSION_KEY="main"                     # target session (default: main)
   ```

3. Run the adapter:
   ```bash
   python adapter.py
   ```

4. Expose with Tailscale Funnel:
   ```bash
   tailscale funnel 8080
   ```

5. Use the funnel URL in your ElevenLabs tool config (`YOUR_WEBHOOK_URL`).

## How It Works

1. ElevenLabs POSTs `{ "task": "..." }`
2. Adapter calls Clawdbot's Tools Invoke API with `sessions_send`
3. Task goes to your main session (full context: workspace, memory, skills)
4. Adapter returns `{ "result": "..." }` to ElevenLabs
