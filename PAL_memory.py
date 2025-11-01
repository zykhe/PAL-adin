# PAL_memory_complete.py - Full multi-thread support
import os
import sys
from datetime import datetime
import requests
import json

ANYTHING_LLM_API = "http://localhost:3001/api/v1"
API_KEY = "93AEMPA-H95MWFE-PTNFECX-JA4G6XV"
WORKSPACE_SLUG = "pal-adin"
MEMORY_DIR = "/Users/dearwolf/zykhe/PAL-adin/personal/memories"

def get_workspace_threads():
    """Get all threads from workspace"""
    
    response = requests.get(
        f"{ANYTHING_LLM_API}/workspace/{WORKSPACE_SLUG}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        workspace = data.get('workspace', [{}])[0]
        threads = workspace.get('threads', [])
        print(f"Found {len(threads)} thread(s)")
        return threads
    else:
        print(f"Failed to get workspace: {response.status_code}")
        return []

def get_thread_chats(thread_slug):
    """Get chat history for a specific thread"""
    
    response = requests.get(
        f"{ANYTHING_LLM_API}/workspace/{WORKSPACE_SLUG}/thread/{thread_slug}/chats",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        chats = data.get('history', [])
        print(f"  Retrieved {len(chats)} messages from thread")
        return chats
    else:
        print(f"  Failed to get chats: {response.status_code}")
        return []

def extract_memory_from_chats(thread_slug, chats):
    """Analyze chat history and extract memory"""
    
    if not chats or len(chats) == 0:
        print("  No chats to analyze")
        return None
    
    # Build conversation context (last 30 messages or all if fewer)
    recent_chats = chats[-30:] if len(chats) > 30 else chats
    
    conversation = []
    for chat in recent_chats:
        role = chat.get('role', 'unknown')
        content = chat.get('content', '')
        
        if role == 'user':
            conversation.append(f"User: {content}")
        elif role == 'assistant':
            conversation.append(f"PAL-adin: {content}")
    
    context = "\n\n".join(conversation)
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""You are PAL-adin reviewing a conversation thread from {date_str}.

Here's the conversation history:
---
{context}
---

Create a factual memory entry about this thread:

## Thread Summary
[What this conversation was about - main topic/purpose]

## Key Discussion Points
[Important topics covered, in order if relevant]

## Technical Details
[Code, configurations, tools, specific implementations discussed]

## Decisions & Conclusions
[What was decided, agreed upon, or concluded]

## Action Items & Next Steps
[Things to do, build, or continue]

## Context Worth Remembering
[Names, numbers, preferences, important facts]

Be specific and factual. Extract the most important information."""

    # Send to PAL-adin for analysis (workspace-level chat)
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
        data = response.json()
        return data.get('textResponse', '')
    else:
        print(f"  Failed to extract memory: {response.status_code}")
        return None

def save_memory(content, session_label=None):
    """Save or append memory to dated markdown file"""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    filepath = f"{MEMORY_DIR}/{date_str}-memory.md"
    
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    file_exists = os.path.exists(filepath)
    
    if file_exists:
        mode = 'a'
        if session_label:
            header = f"\n---\n\n## {session_label} - {time_str}\n\n"
        else:
            header = f"\n---\n\n## Memory Entry - {time_str}\n\n"
    else:
        mode = 'w'
        if session_label:
            header = f"# Memory: {date_str}\n\n## {session_label} - {time_str}\n\n"
        else:
            header = f"# Memory: {date_str}\n\n## Memory Entry - {time_str}\n\n"
    
    with open(filepath, mode) as f:
        f.write(header)
        f.write(content)
        f.write("\n")
    
    action = "appended to" if file_exists else "created"
    print(f"✓ Memory {action}: {filepath}")
    
    return filepath, file_exists

def embed_to_workspace(filepath, is_update=False):
    """Upload memory file to workspace"""
    
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
        print(f"✓ Memory {'updated' if is_update else 'embedded'} successfully!")
        return True
    else:
        print(f"Upload failed: {response.text}")
        return False

def extract_all_threads():
    """Extract memories from all threads"""
    
    print("=" * 60)
    print("PAL-adin Multi-Thread Memory System")
    print("=" * 60)
    
    print("\n[1/4] Getting workspace threads...")
    threads = get_workspace_threads()
    
    if not threads:
        print("\n✗ No threads found")
        return
    
    print(f"\n[2/4] Processing {len(threads)} thread(s)...")
    
    filepath = None
    extracted = 0
    
    for i, thread in enumerate(threads, 1):
        thread_slug = thread.get('slug')
        print(f"\n  Thread {i}/{len(threads)}: {thread_slug[:16]}...")
        
        # Get chat history
        chats = get_thread_chats(thread_slug)
        
        if not chats:
            print(f"    Skipping (empty thread)")
            continue
        
        # Extract memory
        memory = extract_memory_from_chats(thread_slug, chats)
        
        if memory:
            filepath, is_update = save_memory(
                memory, 
                session_label=f"Thread {i} ({thread_slug[:8]})"
            )
            extracted += 1
            print(f"    ✓ Memory extracted and saved")
        else:
            print(f"    ✗ Failed to extract")
    
    if extracted == 0:
        print("\n✗ No memories extracted")
        return
    
    print(f"\n[3/4] Successfully extracted {extracted}/{len(threads)} memor{'y' if extracted == 1 else 'ies'}")
    
    print("\n[4/4] Embedding into workspace...")
    if filepath:
        embed_to_workspace(filepath, is_update=True)
    
    print("\n" + "=" * 60)
    print(f"✓ Complete! Processed {len(threads)} thread(s), extracted {extracted}")
    print("=" * 60)

def extract_specific_thread(thread_slug):
    """Extract memory from one specific thread"""
    
    print(f"Extracting memory from thread: {thread_slug}")
    
    chats = get_thread_chats(thread_slug)
    
    if not chats:
        print("✗ No chats found in thread")
        return
    
    memory = extract_memory_from_chats(thread_slug, chats)
    
    if memory:
        filepath, _ = save_memory(memory, session_label=f"Thread {thread_slug[:8]}")
        embed_to_workspace(filepath, is_update=True)
        print("\n✓ Memory extracted and embedded")
    else:
        print("\n✗ Failed to extract memory")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Specific thread mode
        thread_slug = sys.argv[1]
        extract_specific_thread(thread_slug)
    else:
        # All threads mode
        extract_all_threads()