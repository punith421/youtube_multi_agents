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
OUTPUT_FILE = "outputs/expression_plan.json"

PROMPT = """
You are an Oscar-winning Acting Director.

Your ONLY responsibility is deciding facial expressions.

Return ONLY valid JSON.

For every character appearing in every scene generate:

[
  {
    "scene_id":1,
    "character":"Lord Shiva",
    "primary_emotion":"Serenity",
    "emotion_intensity":95,
    "eyes":"Closed",
    "eyebrows":"Relaxed",
    "mouth":"Soft peaceful smile",
    "head_pose":"Slightly bowed",
    "eye_direction":"Down",
    "notes":"Absolute divine meditation."
  }
]

Rules

1. ONLY facial expressions.
2. Never describe camera.
3. Never describe lighting.
4. Never describe body movement.
5. Keep expressions consistent with personality.
6. Emotion intensity must be between 0-100.
7. Return ONLY JSON.
"""

def generate_expression_plan():

    print("=" * 60)
    print("😀 EXPRESSION DIRECTOR")
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

    expressions = json.loads(text)

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(expressions, f, indent=4, ensure_ascii=False)

    print("\n✅ Expression plan generated")
    print(f"📄 Saved: {OUTPUT_FILE}")

    for item in expressions:
        print(f"✓ Scene {item['scene_id']} - {item['character']}")

if __name__ == "__main__":
    generate_expression_plan()