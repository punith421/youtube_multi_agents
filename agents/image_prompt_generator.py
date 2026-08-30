import os
import json
import time
from dotenv import load_dotenv
from google import genai

# ==========================================
# LOAD GEMINI
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ==========================================
# FILE PATHS
# ==========================================

SCENES_FILE = "outputs_v2/scenes.json"
CHARACTERS_FILE = "outputs_v2/characters.json"
OUTPUT_FILE = "outputs_v2/image_prompts.json"

# ==========================================
# PROMPT
# ==========================================

PROMPT = """
You are a Senior Hollywood Concept Artist and AI Cinematic Prompt Engineer.

Your job is to create one production-ready AI image prompt for every scene.

You have two inputs:

1. Character Database
2. Scene Database

Always use the character descriptions from the Character Database.

Never invent or modify a character's appearance.

For every scene return:

{
    "scene_id": 1,
    "title": "",
    "characters": [],
    "image_prompt": ""
}

The image_prompt must include:

- Exact character appearance from the character database
- Exact clothing
- Exact hairstyle
- Exact jewelry
- Exact weapons
- Facial expression
- Body posture
- Scene location
- Environment
- Architecture
- Time of day
- Weather
- Lighting
- Color palette
- Camera angle
- Camera lens
- Composition
- Mood
- Depth of field
- Volumetric lighting
- Ancient Indian mythology
- Cinematic movie frame
- Hyper detailed

Rules:

1. Never change character appearance.
2. Never change hairstyle.
3. Never change costume.
4. Never change jewelry.
5. Always use the Character Database.
6. Follow the Scene Database.
7. Return ONLY a JSON array.
8. No markdown.
9. No explanations.
"""

# ==========================================
# LOAD FILES
# ==========================================

print("=" * 60)
print("🎨 IMAGE PROMPT GENERATOR")
print("=" * 60)

with open(SCENES_FILE, "r", encoding="utf-8") as f:
    scenes = json.load(f)

with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
    characters = json.load(f)

# ==========================================
# GENERATE PROMPTS
# ==========================================

response = None

for attempt in range(5):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=(
                PROMPT
                + "\n\nCharacters:\n"
                + json.dumps(characters, indent=2, ensure_ascii=False)
                + "\n\nScenes:\n"
                + json.dumps(scenes, indent=2, ensure_ascii=False)
            )
        )
        break

    except Exception as e:
        print(f"⏳ Retry {attempt + 1}/5...")
        print(e)
        time.sleep(10)

if response is None:
    raise Exception("❌ Failed after 5 retries.")

# ==========================================
# CLEAN RESPONSE
# ==========================================

text = response.text.strip()

if text.startswith("```json"):
    text = text.replace("```json", "").replace("```", "").strip()

try:
    parsed = json.loads(text)

except json.JSONDecodeError:
    print("❌ Gemini returned invalid JSON.")
    print(text)
    exit()

# ==========================================
# SAVE OUTPUT
# ==========================================

os.makedirs("outputs_v2", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(parsed, f, indent=4, ensure_ascii=False)

print("\n✅ Image prompts generated!")
print(f"📄 Saved: {OUTPUT_FILE}")