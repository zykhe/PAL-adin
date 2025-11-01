# PAL_memory.py - FIXED VERSION
import os
from datetime import datetime
import requests
import json

# Configuration
ANYTHING_LLM_API = "http://localhost:3001/api/v1"  # Fixed: added /v1
API_KEY = "93AEMPA-H95MWFE-PTNFECX-JA4G6XV"
WORKSPACE_SLUG = "pal-adin"
MEMORY_DIR = "/Users/dearwolf/zykhe/PAL-adin/personal/memories"

def extract_memory_from_conversation():
    """Ask PAL-adin to summarize what to remember from today"""
    
    date_str = datetime.now().strftime("%B %d, %Y")
    
    prompt = f"""You are PAL-adin. Today is {date_str}. 

Review our actual conversation today and create a factual memory entry about what we discussed, built, or accomplished together. This is YOUR memory being recorded - document what YOU (PAL-adin) should remember about today's development session with your creator.

Use this format:

## What We Discussed
[Actual topics covered in today's conversation]

## What We Built/Accomplished  
[Concrete progress made on PAL-adin or related projects]

## Technical Details
[Any important technical information, code, or configurations]

## Creator's Goals/Interests Observed
[What you learned about your creator's intentions or preferences]

## Context for Future Reference
[Important things you should remember going forward]

Be specific and factual. This is actual development documentation, not a roleplay scenario."""
  
    # Send to PAL-adin via AnythingLLM API
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
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    
    try:
        data = response.json()
        print(f"Response keys: {data.keys()}")
        
        # AnythingLLM might use 'textResponse' or 'response'
        if 'textResponse' in data:
            return data['textResponse']
        elif 'response' in data:
            return data['response']
        elif 'message' in data:
            return data['message']
        else:
            print(f"Unknown response format: {data}")
            return str(data)
            
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(f"Raw response: {response.text}")
        return None

def save_memory(content):
    """Save or append memory to dated markdown file"""
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H:%M:%S")
    filepath = f"{MEMORY_DIR}/{date_str}-memory.md"
    
    # Ensure directory exists
    os.makedirs(MEMORY_DIR, exist_ok=True)
    
    # Check if file exists
    if os.path.exists(filepath):
        # Append to existing file
        mode = 'a'
        header = f"\n---\n\n## Memory Entry - {time_str}\n\n"
    else:
        # Create new file
        mode = 'w'
        header = f"# Memory: {date_str}\n\n## Memory Entry - {time_str}\n\n"
    
    with open(filepath, mode) as f:
        f.write(header)
        f.write(content)
        f.write("\n")
    
    print(f"✓ Memory {'appended to' if mode == 'a' else 'saved to'}: {filepath}")
    return filepath
    
def embed_to_workspace(filepath):
    """Upload memory file to AnythingLLM workspace for embedding"""
    
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        files = {
            'file': (filename, f, 'text/markdown')
        }
        
        response = requests.post(
            f"{ANYTHING_LLM_API}/document/upload",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files,
            data={'workspaceSlug': WORKSPACE_SLUG}
        )
    
    print(f"Upload status: {response.status_code}")
    
    if response.status_code == 200:
        print("✓ Memory embedded successfully!")
    else:
        print(f"Embedding response: {response.text}")
        # Try alternate endpoint
        print("\nTrying alternate upload method...")
        try_workspace_upload(filepath)

def try_workspace_upload(filepath):
    """Alternative upload method"""
    
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as f:
        files = {'file': (filename, f, 'text/markdown')}
        
        response = requests.post(
            f"{ANYTHING_LLM_API}/workspace/{WORKSPACE_SLUG}/upload",
            headers={"Authorization": f"Bearer {API_KEY}"},
            files=files
        )
    
    print(f"Alternate upload status: {response.status_code}")
    if response.status_code == 200:
        print("✓ Upload successful via alternate method!")
    else:
        print(f"Response: {response.text}")

def daily_memory_routine():
    """Main routine - extract, save, and embed"""
    
    print("=" * 60)
    print("PAL-adin Memory System")
    print("=" * 60)
    
    print("\n[1/3] Extracting memories from today's conversations...")
    memory_content = extract_memory_from_conversation()
    
    if not memory_content:
        print("\n✗ Failed to extract memory")
        return
    
    print("\n[2/3] Saving memory...")
    filepath = save_memory(memory_content)
    
    print("\n[3/3] Embedding into workspace...")
    embed_to_workspace(filepath)
    
    print("\n" + "=" * 60)
    print("✓ Daily memory routine complete!")
    print("=" * 60)

if __name__ == "__main__":
    daily_memory_routine()