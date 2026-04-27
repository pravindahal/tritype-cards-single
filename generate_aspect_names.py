import os
import requests
import re
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:26b"
ARCHETYPES_DIR = "archetypes"
RAW_DIR = "archetypes_raw"

PROMPT_TEMPLATE = """You are an expert on the Enneagram Tritype system.
We are splitting the overarching archetype "{tritype_name}" into two distinct sub-archetypes: a Light (positive/healthy) aspect and a Shadow (negative/unhealthy) aspect.

We need a short, evocative name for the {aspect} aspect of this archetype.
For example, if the overarching archetype is "The Mentor", the Light aspect might be named "The Guide" and the Shadow aspect might be named "The Perfectionist". If the archetype is "The Supporter", the Light aspect might be "The Caretaker" and the Shadow aspect "The Martyr".

Here is the raw text describing the overarching "{tritype_name}" Tritype:
<raw_text_start>
{raw_text}
<raw_text_end>

Here are the specific traits of the {aspect} aspect:
{attributes}

Based on this, what is the best 1-3 word name for the {aspect} aspect of this archetype? 
Do not include any explanation, quotes, or extra text. Only output the name itself.
"""

def generate_name_for_aspect(archetype_folder, aspect):
    folder_path = os.path.join(ARCHETYPES_DIR, archetype_folder, aspect)
    if not os.path.isdir(folder_path):
        return

    name_path = os.path.join(folder_path, "Name.md")
    if os.path.exists(name_path):
        print(f"[{archetype_folder}/{aspect}] Name.md already exists. Skipping.")
        return

    # Extract tritype name from folder (e.g., "125_Mentor" -> "125 Mentor")
    match = re.match(r'(\d{3})_(.*)', archetype_folder)
    if not match:
        return
    tritype_name = f"{match.group(1)} {match.group(2).replace('_', ' ')}"

    # Read raw text
    raw_file_path = os.path.join(RAW_DIR, f"{archetype_folder}.md")
    raw_text = ""
    if os.path.exists(raw_file_path):
        with open(raw_file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    else:
        print(f"[{archetype_folder}/{aspect}] Warning: Raw text file not found at {raw_file_path}")
        
    # Read specific attributes
    attributes_file = "Attributes.md"
    attr_path = os.path.join(folder_path, attributes_file)
    attributes = ""
    if os.path.exists(attr_path):
        with open(attr_path, 'r', encoding='utf-8') as f:
            attributes = f.read().strip()
            
    prompt = PROMPT_TEMPLATE.format(
        aspect=aspect,
        tritype_name=tritype_name,
        raw_text=raw_text,
        attributes=attributes
    )
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    print(f"[{archetype_folder}/{aspect}] Generating new name...")
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        output = response.json().get('response', '').strip()
        
        # Clean up output (remove quotes, newlines, etc.)
        output = output.replace('"', '').replace("'", '').split('\n')[0].strip()
        
        # Fallback if something went terribly wrong and we got a huge paragraph
        if len(output) > 50:
            print(f"[{archetype_folder}/{aspect}] Output too long, defaulting to standard name.")
            output = f"The {aspect} {match.group(2).replace('_', ' ')}"
            
        with open(name_path, 'w', encoding='utf-8') as f:
            f.write(output)
            
        print(f"[{archetype_folder}/{aspect}] Name generated: {output}")
        
    except Exception as e:
        print(f"[{archetype_folder}/{aspect}] Failed to call Ollama: {e}")

if __name__ == "__main__":
    if not os.path.exists(ARCHETYPES_DIR):
        print("Archetypes directory not found!")
        sys.exit(1)
        
    folders = sorted([f for f in os.listdir(ARCHETYPES_DIR) if os.path.isdir(os.path.join(ARCHETYPES_DIR, f))])
    for archetype in folders:
        generate_name_for_aspect(archetype, "Light")
        generate_name_for_aspect(archetype, "Shadow")
