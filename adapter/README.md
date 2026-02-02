# Adapter

Bridges ElevenLabs webhook calls to Clawdbot's chat completions API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Enable chat completions in Clawdbot (`openclaw.json`):
   ```json
   {
     "gateway": {
       "http": {
         "endpoints": {
           "chatCompletions": { "enabled": true }
         }
       }
     }
   }
   ```

3. Set environment variables (optional):
   ```bash
   export CLAWDBOT_URL="http://localhost:18789"  # default
   export CLAWDBOT_TOKEN="your-token"            # if auth enabled
   export ADAPTER_PORT="8080"                    # default
   ```

4. Run the adapter:
   ```bash
   python adapter.py
   ```

5. Expose with Tailscale Funnel:
   ```bash
   tailscale funnel 8080
   ```

6. Use the funnel URL in your ElevenLabs tool config (`YOUR_WEBHOOK_URL`).

## How It Works

1. ElevenLabs POSTs `{ "task": "..." }`
2. Adapter forwards to Clawdbot's `/v1/chat/completions`
3. Clawdbot runs an agent turn
4. Adapter returns `{ "result": "..." }` to ElevenLabs
