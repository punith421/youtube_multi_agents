import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SCENES_FILE = "outputs/scenes.json"
CHARACTERS_FILE = "outputs/character_reference.json"
OUTPUT_FILE = "outputs/body_language_plan.json"

PROMPT = """
You are a Hollywood Action Director and Body Language Expert.

Your ONLY responsibility is deciding body language.

Return ONLY valid JSON.

For every character appearing in every scene generate:

[
  {
    "scene_id":1,
    "character":"Lord Shiva",
    "body_pose":"",
    "head_position":"",
    "left_hand":"",
    "right_hand":"",
    "spine":"",
    "shoulders":"",
    "legs":"",
    "feet":"",
    "weight_distribution":"",
    "movement":"",
    "gesture":"",
    "notes":""
  }
]

Rules:

1. ONLY body language.
2. Never describe expressions.
3. Never describe camera.
4. Never describe lighting.
5. Match body language to emotion.
6. Match body language to personality.
7. Return ONLY JSON.
"""

def generate_body_plan():

    print("=" * 60)
    print("🚶 BODY LANGUAGE DIRECTOR")
    print("=" * 60)

    with open(SCENES_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        characters = json.load(f)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT
        + "\n\nCharacters:\n"
        + json.dumps(characters, indent=2)
        + "\n\nScenes:\n"
        + json.dumps(scenes, indent=2)
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    body = json.loads(text)

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=4, ensure_ascii=False)

    print("\n✅ Body language plan generated")
    print(f"📄 Saved: {OUTPUT_FILE}")

    for item in body:
        print(f"✓ Scene {item['scene_id']} - {item['character']}")

if __name__ == "__main__":
    generate_body_plan()