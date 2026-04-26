import os
import sys

ARCHETYPES_DIR = "/Users/pravindahal/tritype-cards/archetypes"

def delete_root_genders():
    if not os.path.exists(ARCHETYPES_DIR):
        print("Archetypes directory not found!")
        sys.exit(1)
        
    folders = sorted([f for f in os.listdir(ARCHETYPES_DIR) if os.path.isdir(os.path.join(ARCHETYPES_DIR, f))])
    
    for archetype in folders:
        gender_path = os.path.join(ARCHETYPES_DIR, archetype, "Gender.md")
        if os.path.exists(gender_path):
            os.remove(gender_path)
            print(f"Deleted: {gender_path}")

if __name__ == "__main__":
    delete_root_genders()
    print("Done removing root Gender.md files.")
