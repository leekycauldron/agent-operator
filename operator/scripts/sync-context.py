#!/usr/bin/env python3
"""
Sync workspace context to ElevenLabs knowledge base.

Usage:
    echo "context here" | python sync-context.py
    python sync-context.py "context here"
    python sync-context.py --file context.txt
"""

import os
import sys
import requests
import tempfile
from datetime import datetime

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
DOCUMENT_NAME = "workspace-context"


def get_env_or_die(name):
    val = os.getenv(name)
    if not val:
        print(f"Error: {name} not set", file=sys.stderr)
        sys.exit(1)
    return val


def delete_old_documents(api_key):
    """Delete all documents with our document name."""
    headers = {"xi-api-key": api_key}
    deleted = []
    
    next_cursor = None
    while True:
        params = {"page_size": 100}
        if next_cursor:
            params["cursor"] = next_cursor
            
        resp = requests.get(
            f"{ELEVENLABS_API_URL}/convai/knowledge-base",
            headers=headers,
            params=params
        )
        
        if resp.status_code != 200:
            print(f"Warning: Failed to list documents: {resp.text}", file=sys.stderr)
            break
            
        data = resp.json()
        for doc in data.get("documents", []):
            if doc.get("name") == DOCUMENT_NAME:
                doc_id = doc.get("id")
                del_resp = requests.delete(
                    f"{ELEVENLABS_API_URL}/convai/knowledge-base/{doc_id}",
                    headers=headers
                )
                if del_resp.status_code == 200:
                    deleted.append(doc_id)
                    print(f"Deleted old document: {doc_id}")
                    
        if not data.get("has_more"):
            break
        next_cursor = data.get("next_cursor")
    
    return deleted


def upload_context(api_key, context):
    """Upload context text to knowledge base."""
    headers = {
        "xi-api-key": api_key,
    }
    
    # Write to temp file for upload
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(context)
        temp_path = f.name
    
    try:
        with open(temp_path, 'rb') as f:
            files = {'file': (f"{DOCUMENT_NAME}.txt", f, 'text/plain')}
            data = {'name': DOCUMENT_NAME}
            
            resp = requests.post(
                f"{ELEVENLABS_API_URL}/convai/knowledge-base/file",
                headers=headers,
                data=data,
                files=files
            )
        
        if resp.status_code != 200:
            print(f"Error uploading: {resp.text}", file=sys.stderr)
            sys.exit(1)
            
        return resp.json()
    finally:
        os.unlink(temp_path)


def update_agent(api_key, agent_id, doc_id):
    """Update agent to include the new document."""
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    # Get current agent config
    resp = requests.get(
        f"{ELEVENLABS_API_URL}/convai/agents/{agent_id}",
        headers=headers
    )
    
    if resp.status_code != 200:
        print(f"Error getting agent: {resp.text}", file=sys.stderr)
        sys.exit(1)
    
    agent = resp.json()
    
    # Get existing knowledge bases, filter out old workspace-context
    existing_kbs = []
    try:
        existing_kbs = agent["conversation_config"]["agent"]["prompt"].get("knowledge_base", [])
    except (KeyError, TypeError):
        pass
    
    filtered_kbs = [
        kb for kb in existing_kbs
        if kb.get("name") != DOCUMENT_NAME
    ]
    
    # Add new document
    filtered_kbs.append({
        "type": "file",
        "name": DOCUMENT_NAME,
        "id": doc_id,
        "usage_mode": "auto"
    })
    
    # Update agent
    update_data = {
        "conversation_config": {
            "agent": {
                "prompt": {
                    "knowledge_base": filtered_kbs
                }
            }
        }
    }
    
    resp = requests.patch(
        f"{ELEVENLABS_API_URL}/convai/agents/{agent_id}",
        headers=headers,
        json=update_data
    )
    
    if resp.status_code != 200:
        print(f"Error updating agent: {resp.text}", file=sys.stderr)
        sys.exit(1)
    
    return resp.json()


def main():
    api_key = get_env_or_die("ELEVENLABS_API_KEY")
    agent_id = get_env_or_die("ELEVENLABS_AGENT_ID")
    
    # Get context from args, file, or stdin
    context = None
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--file" and len(sys.argv) > 2:
            with open(sys.argv[2], 'r') as f:
                context = f.read()
        else:
            context = sys.argv[1]
    elif not sys.stdin.isatty():
        context = sys.stdin.read()
    
    if not context or not context.strip():
        print("Error: No context provided", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    context = f"Synced: {timestamp}\n\n{context}"
    
    print("Deleting old context documents...")
    delete_old_documents(api_key)
    
    print("Uploading new context...")
    result = upload_context(api_key, context)
    doc_id = result.get("id")
    print(f"Created document: {doc_id}")
    
    print("Updating agent...")
    update_agent(api_key, agent_id, doc_id)
    
    print("Done!")


if __name__ == "__main__":
    main()
