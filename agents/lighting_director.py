import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SCENES_FILE = "outputs/scenes.json"
OUTPUT_FILE = "outputs/lighting_plan.json"

PROMPT = """
You are an Oscar-winning Hollywood Cinematographer and Lighting Director.

Your ONLY responsibility is lighting.

Return ONLY valid JSON.

For every scene generate:

[
  {
    "scene_id":1,
    "lighting_style":"",
    "key_light":"",
    "fill_light":"",
    "rim_light":"",
    "background_light":"",
    "volumetric_light":"",
    "shadow_style":"",
    "color_temperature":"",
    "fog":"",
    "atmosphere":"",
    "notes":""
  }
]

Rules

1. ONLY lighting.
2. Never describe camera.
3. Never describe characters.
4. Never describe expressions.
5. Never describe body language.
6. Think like a Hollywood cinematographer.
7. Match lighting with emotion.
8. Return ONLY JSON.

Lighting Styles:

- Golden Sunrise
- Blue Hour
- Moonlight
- Divine Aura
- Firelight
- Torch Light
- Storm
- Sunset
- Overcast
- Heavenly Glow
- Cosmic Energy
- Dark Fantasy

Shadow Styles:

- Soft
- Hard
- Dramatic
- High Contrast
- Low Contrast

Color Temperature:

- Warm
- Neutral
- Cool
- Mixed
"""

def generate_lighting_plan():

    print("=" * 60)
    print("💡 LIGHTING DIRECTOR")
    print("=" * 60)

    with open(SCENES_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT + "\n\nScenes:\n" + json.dumps(scenes, indent=2)
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    lighting = json.loads(text)

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(lighting, f, indent=4, ensure_ascii=False)

    print("\n✅ Lighting plan generated")
    print(f"📄 Saved: {OUTPUT_FILE}")

    for item in lighting:
        print(f"✓ Scene {item['scene_id']} - {item['lighting_style']}")

if __name__ == "__main__":
    generate_lighting_plan()