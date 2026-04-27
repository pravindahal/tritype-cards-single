import os
import shutil

ARCHETYPES_DIR = "archetypes"

def restructure():
    for archetype in os.listdir(ARCHETYPES_DIR):
        arch_path = os.path.join(ARCHETYPES_DIR, archetype)
        if not os.path.isdir(arch_path):
            continue
            
        light_dir = os.path.join(arch_path, "Light")
        shadow_dir = os.path.join(arch_path, "Shadow")
        
        # Files to rescue to the parent directory
        to_rescue = ["Gender.md", "Visual_Concept.md"]
        for f in to_rescue:
            src = os.path.join(light_dir, f)
            dest = os.path.join(arch_path, f)
            if os.path.exists(src) and not os.path.exists(dest):
                shutil.copy2(src, dest)
            elif os.path.exists(os.path.join(shadow_dir, f)) and not os.path.exists(dest):
                shutil.copy2(os.path.join(shadow_dir, f), dest)
                
        # Clean Light
        if os.path.exists(light_dir):
            for f in os.listdir(light_dir):
                fpath = os.path.join(light_dir, f)
                if os.path.isfile(fpath):
                    if f == "Light_Attributes.md":
                        os.rename(fpath, os.path.join(light_dir, "Attributes.md"))
                    elif f != "Attributes.md":
                        os.remove(fpath)
                        
        # Clean Shadow
        if os.path.exists(shadow_dir):
            for f in os.listdir(shadow_dir):
                fpath = os.path.join(shadow_dir, f)
                if os.path.isfile(fpath):
                    if f == "Shadow_Attributes.md":
                        os.rename(fpath, os.path.join(shadow_dir, "Attributes.md"))
                    elif f != "Attributes.md":
                        os.remove(fpath)
                        
    print("Directories restructured successfully!")

if __name__ == "__main__":
    restructure()
