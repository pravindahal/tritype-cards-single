import os
import requests
import re
import sys

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:26b"
ARCHETYPES_DIR = "/Users/pravindahal/tritype-cards/archetypes"
RAW_DIR = "/Users/pravindahal/tritype-cards/archetypes_raw"

PROMPT_TEMPLATE = """You are an expert character designer and psychologist working with the Enneagram Tritype system.
We are assigning an archetypal gender representation (Male or Female) for the {aspect} aspect of the "{tritype_name}" Tritype.

Here is the raw text describing this Tritype:
<raw_text_start>
{raw_text}
<raw_text_end>

Here are the specific {aspect} Attributes for this aspect:
{attributes}

Based on these traits and the overall archetype description, which gender representation (Male or Female) would visually and thematically best personify the {aspect} aspect of this archetype? 
Please respond with ONLY ONE WORD: Male or Female. No other text.
"""

def reevaluate_gender_for_aspect(archetype_folder, aspect):
    folder_path = os.path.join(ARCHETYPES_DIR, archetype_folder, aspect)
    if not os.path.isdir(folder_path):
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
            
    gender_path = os.path.join(folder_path, "Gender.md")
    
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
    
    print(f"[{archetype_folder}/{aspect}] Re-evaluating gender...")
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        output = response.json().get('response', '').strip()
        
        # Clean up output
        cleaned_output = re.sub(r'[^A-Za-z]', '', output)
        if cleaned_output.lower() in ['male', 'female']:
            final_gender = cleaned_output.capitalize()
        else:
            if 'female' in output.lower():
                final_gender = 'Female'
            elif 'male' in output.lower():
                final_gender = 'Male'
            else:
                print(f"[{archetype_folder}/{aspect}] Unexpected output: {output}. Defaulting to Female.")
                final_gender = "Female"
            
        with open(gender_path, 'w', encoding='utf-8') as f:
            f.write(final_gender)
            
        print(f"[{archetype_folder}/{aspect}] Gender updated to: {final_gender}")
        
    except Exception as e:
        print(f"[{archetype_folder}/{aspect}] Failed to call Ollama: {e}")

if __name__ == "__main__":
    if not os.path.exists(ARCHETYPES_DIR):
        print("Archetypes directory not found!")
        sys.exit(1)
        
    folders = sorted([f for f in os.listdir(ARCHETYPES_DIR) if os.path.isdir(os.path.join(ARCHETYPES_DIR, f))])
    for archetype in folders:
        reevaluate_gender_for_aspect(archetype, "Light")
        reevaluate_gender_for_aspect(archetype, "Shadow")
