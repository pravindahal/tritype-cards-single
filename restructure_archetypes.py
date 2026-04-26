import os
import shutil

def restructure_archetypes(base_dir):
    # Ensure the base directory exists
    if not os.path.exists(base_dir):
        print(f"Error: Directory {base_dir} does not exist.")
        return

    # Iterate through all items in the base directory
    for item in os.listdir(base_dir):
        item_path = os.path.join(base_dir, item)
        
        # Check if it's a directory (e.g., '125_Mentor')
        if os.path.isdir(item_path):
            print(f"Processing archetype: {item}")
            
            # Paths for the new Light and Shadow directories
            light_dir = os.path.join(item_path, "Light")
            shadow_dir = os.path.join(item_path, "Shadow")
            
            # Create the directories if they don't exist
            os.makedirs(light_dir, exist_ok=True)
            os.makedirs(shadow_dir, exist_ok=True)
            
            # Get all files in the current archetype directory
            files_to_move = [
                f for f in os.listdir(item_path) 
                if os.path.isfile(os.path.join(item_path, f))
            ]
            
            for file_name in files_to_move:
                source_file = os.path.join(item_path, file_name)
                
                # Destination paths
                light_dest = os.path.join(light_dir, file_name)
                shadow_dest = os.path.join(shadow_dir, file_name)
                
                # Copy to Light and Shadow
                shutil.copy2(source_file, light_dest)
                shutil.copy2(source_file, shadow_dest)
                
                # Remove the original file
                os.remove(source_file)
                print(f"  Moved {file_name} -> Light/ and Shadow/")

if __name__ == "__main__":
    archetypes_dir = os.path.join(os.path.dirname(__file__), "archetypes")
    print(f"Starting restructuring in: {archetypes_dir}")
    restructure_archetypes(archetypes_dir)
    print("Done!")
