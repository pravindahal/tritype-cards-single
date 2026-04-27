import os
import requests
import re
import sys
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma4:26b"
ARCHETYPES_DIR = "archetypes"

PROMPT_TEMPLATE = """You are an expert on the Enneagram personality typing system, specifically the Tritype theory.

I am generating archetype cards for each Enneagram Tritype. For each Tritype, I need three things:
1. Light Attributes: 4-5 positive personality traits.
2. Shadow Attributes: 4-5 negative personality traits or struggles.
3. Visual Concept: A detailed prompt for an AI image generator to create a contemporary digital painting representing this archetype.

Here is an example for the 379 Ambassador:

===LIGHT===
Diplomatic Mediation, Adaptable Charm, Resilient Optimism, Approachable Leadership
===SHADOW===
Chronic Conflict Avoidance, The Chameleon Effect, Toxic Positivity, Superficial Engagement, Passive-Aggression
===VISUAL===
Imagine a contemporary digital painting of a charismatic woman standing poised with a genuinely warm and engaging smile. Her focused, kind eyes convey both capability and approachability.

Attire & Details: Her clothing is a sophisticated mix. A well-tailored, modern blazer or jacket (3's success) is layered over comfortable, textured fabrics in uplifting colors (7's energy/9's ease) – perhaps a vibrant scarf or interesting jewelry. She wears unique, understated accessories that hint at global travels or personal creativity. Her posture is relaxed but composed, radiating a powerful, accessible confidence.

Environment: She stands in an open, bright space that suggests modern connection and global harmony. This might be a bustling but positive modern atrium overlooking a city at dawn (optimism) or a serene plaza where graceful architectural lines blend with lush greenery (nature/calm). Background elements, slightly blurred, include stylized connecting lines or subtle glows, with diverse figures engaged in conversation further down the path, rather than explicitly identifiable.

Symbolism & Composition: In one hand, she lightly holds a beautifully crafted, artistic compass or a unique globe sculpture (future direction/connection) – held not aggressively, but with gentle strength. The composition uses soft, flowing lines and circular shapes rather than harsh angles to convey a sense of balance and unity. Diffused, warm natural light bathes the entire scene, with soft morning gold or gentle sunset hues.

Color Palette: A balanced and uplifting palette of deep grounded blues and warm grays (professionalism/calm) punctuated by vibrant splashes of turquoise, coral, gold, and soft greens (optimism/nature). The light is essential, creating a sense of warmth and genuine connection.

Now, generate the same three components for the {tritype_name} Tritype. Be sure to reference the specific enneagram numbers ({enneagram_numbers}) and their traits in the visual description like in the example. 
The gender for this archetype is: {gender}. Ensure you use the correct gender pronouns and terms matching "{gender}" in the visual concept. Focus on the core archetype.

Here is the raw text describing the {tritype_name} Tritype:
<raw_text_start>
{raw_text}
<raw_text_end>

Format your output exactly as follows with no extra text before or after:
===LIGHT===
<comma separated list>
===SHADOW===
<comma separated list>
===VISUAL===
<paragraphs>
"""

def generate_for_tritype(tritype_folder):
    match = re.match(r'(\d{3})_(.*)', tritype_folder)
    if not match:
        return
    
    enneagram_numbers = match.group(1)
    name = match.group(2).replace('_', ' ')
    tritype_name = f"{enneagram_numbers} {name}"
    
    folder_path = os.path.join(ARCHETYPES_DIR, tritype_folder)
    
    light_path = os.path.join(folder_path, "Light_Attributes.md")
    shadow_path = os.path.join(folder_path, "Shadow_Attributes.md")
    visual_path = os.path.join(folder_path, "Visual_Concept.md")
    gender_path = os.path.join(folder_path, "Gender.md")
    
    if os.path.exists(light_path) and os.path.exists(shadow_path) and os.path.exists(visual_path):
        print(f"[{tritype_name}] Files already exist. Skipping.")
        return
        
    gender = "Unknown"
    if os.path.exists(gender_path):
        with open(gender_path, 'r', encoding='utf-8') as f:
            gender = f.read().strip()
            
    raw_file_path = os.path.join(ARCHETYPES_DIR + "_raw", f"{tritype_folder}.md")
    raw_text = ""
    if os.path.exists(raw_file_path):
        with open(raw_file_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
    else:
        print(f"[{tritype_name}] Warning: Raw text file not found at {raw_file_path}")
        
    print(f"[{tritype_name}] Generating...")
    
    prompt = PROMPT_TEMPLATE.format(
        tritype_name=tritype_name, 
        enneagram_numbers=enneagram_numbers,
        raw_text=raw_text,
        gender=gender
    )
    
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        output = response.json().get('response', '')
    except Exception as e:
        print(f"[{tritype_name}] Failed to call Ollama: {e}")
        return
        
    # Parsing the output
    light_match = re.search(r'===LIGHT===\n(.*?)\n===SHADOW===', output, re.DOTALL)
    shadow_match = re.search(r'===SHADOW===\n(.*?)\n===VISUAL===', output, re.DOTALL)
    visual_match = re.search(r'===VISUAL===\n(.*)', output, re.DOTALL)
    
    if light_match and shadow_match and visual_match:
        light_content = light_match.group(1).strip()
        shadow_content = shadow_match.group(1).strip()
        visual_content = visual_match.group(1).strip()
        
        with open(light_path, 'w') as f:
            f.write(light_content)
        with open(shadow_path, 'w') as f:
            f.write(shadow_content)
        with open(visual_path, 'w') as f:
            f.write(visual_content)
            
        print(f"[{tritype_name}] Successfully generated and saved files.")
    else:
        print(f"[{tritype_name}] Failed to parse output. You might need to adjust the prompt or parse logic.")
        print(f"Output was:\n{output}")

if __name__ == "__main__":
    if not os.path.exists(ARCHETYPES_DIR):
        print("Archetypes directory not found!")
        sys.exit(1)
        
    folders = sorted([f for f in os.listdir(ARCHETYPES_DIR) if os.path.isdir(os.path.join(ARCHETYPES_DIR, f))])
    for folder in folders:
        generate_for_tritype(folder)
