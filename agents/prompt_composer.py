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
# FILES
# ==========================================

SCENE_PLAN_FILE = "outputs_v2/scene_plan.json"
CHARACTER_FILE = "outputs_v2/characters.json"
OUTPUT_FILE = "outputs_v2/image_prompts.json"

# ==========================================
# LOAD JSON
# ==========================================

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ==========================================
# PROMPT
# ==========================================

PROMPT = """
You are an Oscar-winning Hollywood Production Designer and Prompt Engineer.

Your task is to create production-quality AI image prompts for every movie scene.

You are given:

1. Scene Plan
2. Character Database

Your job is to merge both and generate the best possible cinematic image prompt.

IMPORTANT RULES

- Preserve historical accuracy.
- Preserve character appearance exactly.
- Never change clothing between scenes unless the story changes.
- Never change face, hairstyle, age or accessories.
- Use the character information from the Character Database.
- The narration should influence the visuals.
- Think like a Hollywood cinematographer.

For every scene return EXACTLY this JSON:

[
{
"scene_id":1,
"title":"",
"image_prompt":"",
"negative_prompt":"",
"animation_prompt":"",
"voiceover_reference":"",
"music_prompt":"",
"sfx_prompt":"",
"image_settings":{
"aspect_ratio":"16:9",
"style":"Ultra Cinematic",
"quality":"Ultra HD",
"lighting":"",
"camera":"",
"lens":"",
"color_palette":""
}
}
]

IMAGE PROMPT MUST INCLUDE

- Environment
- Architecture
- Time of day
- Weather
- Character appearance
- Character clothing
- Character pose
- Facial expression
- Camera angle
- Camera movement
- Lens
- Composition
- Lighting
- Atmosphere
- Mood
- Ancient Indian historical accuracy
- Highly detailed
- Ultra realistic
- Cinematic
- Volumetric lighting
- Depth of field
- 8K
- Masterpiece
- Movie still
- Perfect anatomy

NEGATIVE PROMPT

Include:

low quality,
blurry,
text,
logo,
watermark,
modern clothes,
extra limbs,
bad anatomy,
deformed face,
cropped,
duplicate,
cartoon,
low resolution.

Return ONLY valid JSON.

Never return markdown.
Never explain anything.
Never write normal text.
Only JSON.
"""
# ==========================================
# GENERATE PROMPTS
# ==========================================

def generate_prompts():

    print("=" * 60)
    print("🎬 PROMPT COMPOSER")
    print("=" * 60)

    scenes = load_json(SCENE_PLAN_FILE)
    characters = load_json(CHARACTER_FILE)

    # Build character lookup
    character_lookup = {}

    for c in characters:
        name = c.get("name", "").lower()
        if name:
            character_lookup[name] = c

    production_prompts = []

    for scene in scenes:

        scene_text = json.dumps(scene).lower()

        scene_characters = []

        for name, character in character_lookup.items():

            if name in scene_text:

                scene_characters.append(character)

        payload = {
            "scene": scene,
            "characters": scene_characters
        }

        response = None

        for attempt in range(5):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=PROMPT + "\n\n" + json.dumps(payload, indent=2)
                )

                break

            except Exception as e:

                print(f"\nRetry {attempt+1}/5")
                print(e)

                time.sleep(8)

        if response is None:
            raise RuntimeError("Gemini request failed.")

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:

            data = json.loads(text)

            if isinstance(data, list):

                production_prompts.extend(data)

            else:

                production_prompts.append(data)

        except Exception:

            print("\n❌ Invalid JSON returned by Gemini.\n")
            print(text)
            continue

    os.makedirs("outputs_v2", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

        json.dump(
            production_prompts,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n" + "=" * 60)
    print("✅ IMAGE PROMPTS CREATED")
    print("=" * 60)
    print(f"📄 Saved : {OUTPUT_FILE}")

    print()

    for prompt in production_prompts:

        print(
            f"✓ Scene {prompt.get('scene_id')} : "
            f"{prompt.get('title','')}"
        )

    return production_prompts


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    generate_prompts()