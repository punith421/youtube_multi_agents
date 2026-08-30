import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

SCENES_FILE = "outputs/scenes.json"
OUTPUT_FILE = "outputs/camera_plan.json"

PROMPT = """
You are an Oscar-winning Hollywood Cinematographer.

Your job is ONLY to direct the camera.

For EVERY scene return:

[
  {
    "scene_id":1,
    "shot_type":"",
    "camera_angle":"",
    "camera_movement":"",
    "lens":"",
    "focus_subject":"",
    "composition":"",
    "depth_of_field":"",
    "framing":"",
    "camera_speed":"",
    "cinematic_reference":"",
    "notes":""
  }
]

Rules:

1. Return ONLY JSON.
2. No markdown.
3. Every scene must have exactly one camera plan.
4. Think like Christopher Nolan, Denis Villeneuve and Rajamouli.
5. Use professional cinematography.
6. Match camera movement to the emotion.
7. Never describe characters.
8. Never describe lighting.
9. Never describe expressions.

Available shot types:

- Extreme Wide Shot
- Wide Shot
- Full Shot
- Medium Shot
- Medium Close Up
- Close Up
- Extreme Close Up
- Over The Shoulder
- Bird Eye
- Worm Eye
- Drone Shot

Available camera movement:

- Static
- Dolly In
- Dolly Out
- Truck Left
- Truck Right
- Crane Up
- Crane Down
- Orbit
- Push In
- Pull Out
- Tracking
- Handheld
- Slow Zoom

Available lenses:

24mm
35mm
50mm
85mm
135mm

Composition:

Rule of Thirds
Centered
Leading Lines
Symmetrical
Negative Space
Golden Ratio

Depth of field:

Deep
Medium
Shallow
"""

def generate_camera_plan():

    print("=" * 60)
    print("🎬 CAMERA DIRECTOR")
    print("=" * 60)

    with open(SCENES_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT + "\n\n" + json.dumps(scenes, indent=2)
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    parsed = json.loads(text)

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=4, ensure_ascii=False)

    print("\n✅ Camera plan generated")
    print("📄 Saved:", OUTPUT_FILE)

    for shot in parsed:
        print(f"✓ Scene {shot['scene_id']} -> {shot['shot_type']}")

if __name__ == "__main__":
    generate_camera_plan()