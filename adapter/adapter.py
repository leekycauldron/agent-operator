#!/usr/bin/env python3
"""
ElevenLabs → Clawdbot Adapter

Receives webhook calls from ElevenLabs and forwards to Clawdbot's
chat completions API.

Usage:
    python adapter.py

Environment variables:
    CLAWDBOT_URL      - Clawdbot gateway URL (default: http://localhost:18789)
    CLAWDBOT_TOKEN    - Gateway auth token (optional)
    ADAPTER_PORT      - Port to listen on (default: 8080)

Then expose with: tailscale funnel <port>
"""

import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

CLAWDBOT_URL = os.getenv("CLAWDBOT_URL", "http://localhost:18789")
CLAWDBOT_TOKEN = os.getenv("CLAWDBOT_TOKEN", "")
ADAPTER_PORT = int(os.getenv("ADAPTER_PORT", "8080"))


@app.route("/", methods=["POST"])
def handle_task():
    """Receive task from ElevenLabs, forward to Clawdbot."""
    try:
        data = request.get_json() or {}
        task = data.get("task", "")
        
        if not task:
            return jsonify({"error": "No task provided"}), 400
        
        # Forward to Clawdbot chat completions
        headers = {"Content-Type": "application/json"}
        if CLAWDBOT_TOKEN:
            headers["Authorization"] = f"Bearer {CLAWDBOT_TOKEN}"
        
        payload = {
            "model": "openclaw",
            "messages": [{"role": "user", "content": task}]
        }
        
        resp = requests.post(
            f"{CLAWDBOT_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if resp.status_code != 200:
            return jsonify({"error": f"Clawdbot error: {resp.text}"}), 502
        
        result = resp.json()
        
        # Extract the assistant's response
        try:
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            content = str(result)
        
        return jsonify({"result": content})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print(f"Adapter listening on port {ADAPTER_PORT}")
    print(f"Forwarding to Clawdbot at {CLAWDBOT_URL}")
    print(f"Expose with: tailscale funnel {ADAPTER_PORT}")
    app.run(host="0.0.0.0", port=ADAPTER_PORT)
