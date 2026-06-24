import google.generativeai as genai
import json

API_KEY = "AQ.Ab8RN6LWIoAdZQlbC9-cpMC3j-HTyLO3ySIklBphVNilFQv7iA"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# Load scenes
with open("outputs/scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

# Load characters
with open("outputs/characters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)

prompt = f"""
You are an expert AI image prompt engineer.

Using the scenes and character database below, generate a cinematic image prompt for every scene.

Rules:
- Keep character appearance consistent.
- Use cinematic documentary style.
- Use ultra detailed descriptions.
- Mention lighting, camera angle, mood, environment.
- Suitable for Flux, SDXL, Midjourney, Leonardo AI.
- Return ONLY valid JSON.

Characters:
{json.dumps(characters, indent=2)}

Scenes:
{json.dumps(scenes, indent=2)}
"""

print("🎨 Generating image prompts...")

response = model.generate_content(prompt)

result = response.text
result = result.replace("```json", "").replace("```", "").strip()

with open("outputs/image_prompts.json", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Image prompts generated!")
print("📄 outputs/image_prompts.json")