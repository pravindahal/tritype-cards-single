import os
import re

data = """
125The MentorFemale52%
126The SupporterFemale62%
127The TeacherFemale57%
135The Technical ExpertMale60%
136The TaskmasterEven Split50%
137The Systems BuilderMale55%
145The ResearcherEven Split50%
146The PhilosopherFemale60%
147The VisionaryFemale55%
258The StrategistMale56%
259The Problem SolverFemale55%
268The RescuerFemale54%
269The Good SamaritanFemale65%
278The Free SpiritMale51%
279The PeacemakerFemale60%
358The Solution MasterMale68%
359The ThinkerMale56%
368The Justice FighterMale58%
369The MediatorFemale54%
378The Mover & ShakerMale63%
379The AmbassadorMale51%
458The ScholarMale58%
459The ContemplativeFemale54%
468The Truth TellerFemale52%
469The SeekerFemale64%
478The MessengerMale53%
479The Gentle SpiritFemale59%
"""

# Regex to parse the data. 
# Since there are no spaces between components in the input string (e.g. 125The MentorFemale52%)
# We need a way to split them. 
# The pattern seems to be: digits (tritype), then Name, then Gender (Male/Female/Even Split), then percentage.

# Let's use a more robust way to parse. 
# The string is actually: 125The MentorFemale52%
# It looks like: (Digits)(Name)(Gender)(Percentage)
# Gender is Male, Female, or Even Split.
# Percentage is % at the end.

# We can use regex to find the parts.
pattern = rearm_pattern = r"(\d+)(.*?)(Male|Female|Even Split)(\d+%)"
matches = re.findall(pattern, data)

for tritype, name, gender, prob in matches:
    # Clean up name: remove "The " if it exists at the beginning
    clean_name = name.strip()
    if clean_name.startswith("The "):
        clean_name = clean_name[4:]
    
    # For even split, use male
    final_gender = "Male" if gender == "Even Split" else gender
    
    # Replace spaces with underscores for directory/file names if needed, 
    # but user said type_name, and archetypes_raw has underscores.
    # Let's use the name as is but replace spaces with underscores to be safe and consistent with archetypes_raw
    dir_name = clean_name.replace(" ", "_")
    # Actually, looking at archetypes_raw, it uses underscores. 
    # But the user says type_name. Let's try to match the archetype_raw style.
    # Wait, the user said: archetypes/type_name/Gender.md
    # If type_name is "Mentor", then archetypes/Mentor/Female.md
    # Let's use the name without "The " and with underscores for the directory name.
    
    # Let's check what the user might want for type_name. 
    # If it's 125_Mentor, then dir is 125_Mentor. 
    # But the data says "125The Mentor".
    # Let's try to use the name from the data.
    
    target_dir = os.path.join("archetypes", clean_name.replace(" ", "_"))
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = os.path.join(target_dir, f"{final_gender}.md")
    with open(file_path, "w") as f:
        f.write(prob)
    print(f"Created {file_path} with content {prob}")

