import os
import re

data = """
125The MentorFemale52%
126The SupporterFemale62%
127The TeacherFemale57%
135The Technical ExpertMale60%
13cand6The TaskmasterEven Split50%
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

# Pattern to extract tritype and gender
# Note: I'll fix the typo in '13cand6' which was clearly '136' in the user's text
data = data.replace("13cand6", "136")
pattern = r"(\d+).*?(Male|Female|Even Split)"
gender_map = dict(re.findall(pattern, data))

# For "Even Split", the user said "choose male"
for tritype, gender in gender_map.items():
    if gender == "Even Split":
        gender_map[tritype] = "Male"

raw_dir = "archetypes_raw"
target_base = "archetypes"

if not os.path.exists(target_base):
    os.makedirs(target_base)

for filename in os.listdir(raw_dir):
    if filename.endswith(".md"):
        folder_name = filename.replace(".md", "")
        # Extract digits from start of folder_name
        match = re.match(r"(\d+)", folder_name)
        if match:
            tritype = match.group(1)
            gender = gender_map.get(tritype, "Unknown")
            
            target_dir = os.path.join(target_base, folder_name)
            os.makedirs(target_dir, exist_ok=True)
            
            file_path = os.path.join(target_dir, "Gender.md")
            with open(file_path, "w") as f:
                f.write(gender)
            print(f"Created {file_path} with {gender}")
