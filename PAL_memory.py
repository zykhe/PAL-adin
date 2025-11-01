# PAL_memory_final.py - Pragmatic version
import os
from datetime import datetime
import requests

ANYTHING_LLM_API = "http://localhost:3001/api/v1"
API_KEY = "93AEMPA-H95MWFE-PTNFECX-JA4G6XV"
WORKSPACE_SLUG = "pal-adin"
MEMORY_DIR = "/Users/dearwolf/zykhe/PAL-adin/personal/memories"

def extract_daily_memory():
    """Extract comprehensive memory from today"""
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""You are PAL-adin. Today is {date_str}.

Review everything we discussed and worked on today across all our conversations.

Create a comprehensive memory entry:

## Today's Overview
[Main themes, projects, or goals we focused on]

## Technical Work
[Systems built, code written, tools configured, problems solved]

## Key Decisions & Insights
[Important choices made, things learned or understood better]

## Context & Details
[Specific information worth remembering - names, numbers, approaches]

## Momentum
[What we should continue, what's working well]

## Questions or Blockers
[Anything unresolved or needing attention]

Be specific, factual, and thorough. This is your actual memory being recorded."""

    response = requests.post(
        f"{ANYTHING_LLM_API}/workspace/{WORKSPACE_SLUG}/chat",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "message": prompt,
            "mode": "chat"
        }
    )
    
    if response.status_code == 200:
        return response.json().get('textResponse', '')
    return None

def save_memory(content):
    """Save memory to dated file"""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    filepath = f"{MEMORY_DIR}/{date_str}-memory.md"
    
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    file_exists = os.path.exists(filepath)
    
    if file_exists:
        with open(filepath, 'a') as f:
            f.write(f"\n---\n\n## Update - {time_str}\n\n")
            f.write(content)
            f.write("\n")
    else:
        with open(filepath, 'w') as f:
            f.write(f"# Memory: {date_str}\n\n")
            f.write(content)
            f.write("\n")
    
    print(f"✓ Memory {'updated' if file_exists else 'saved'}: {filepath}")
    return filepath

def embed_to_workspace(filepath):
    """Upload to workspace"""
    
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'text/markdown')}
        response = requests.post(
            f"{ANYTHING_LLM_API}/document/upload",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files,
            data={'workspaceSlug': WORKSPACE_SLUG}
        )
    
    if response.status_code == 200:
        print("✓ Memory embedded successfully!")
    else:
        print(f"Embedding failed: {response.text}")

if __name__ == "__main__":
    print("Extracting daily memory...")
    memory = extract_daily_memory()
    
    if memory:
        filepath = save_memory(memory)
        embed_to_workspace(filepath)
        print("\n✓ Daily memory complete!")
    else:
        print("\n✗ Failed to extract memory")