import os
from dotenv import load_dotenv
import google.generativeai as genai

# ==========================================
# LOAD GEMINI
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

INPUT_FILE = "outputs_v2/story.txt"
OUTPUT_FILE = "outputs_v2/scene_plan.json"

print("=" * 60)
print("🎬 SCENE PLANNER")
print("=" * 60)

# Read story
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    story = f.read()

prompt = f"""
You are an expert Film Director and Scene Planner.

Convert the documentary script into a detailed animation scene plan.

Rules:

1. Do NOT rewrite the narration.
2. Preserve the story exactly.
3. Break long scenes into smaller cinematic scenes.
4. Every scene should last between 5 and 15 seconds.
5. Think like a movie director.
6. Make every scene visually interesting.
7. Return ONLY valid JSON.

JSON format:

[
  {{
    "scene_number": 1,
    "scene_title": "",
    "narration": "",
    "visual_description": "",
    "characters": [],
    "location": "",
    "time_period": "",
    "emotion": "",
    "camera_angle": "",
    "camera_movement": "",
    "lighting": "",
    "background_music": "",
    "sound_effects": "",
    "estimated_duration": ""
  }}
]

Documentary Script:

{story}
"""

response = model.generate_content(prompt)

scene_plan = response.text.strip()

# Remove markdown if Gemini wraps JSON
if scene_plan.startswith("```json"):
    scene_plan = scene_plan.replace("```json", "").replace("```", "").strip()

os.makedirs("outputs_v2", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(scene_plan)

print("\n✅ Scene plan created!")
print(f"📄 Saved: {OUTPUT_FILE}")