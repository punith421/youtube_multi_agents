from groq import Groq
import json

client = Groq(
    api_key="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"
)

# Load scenes
with open("outputs/scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

# Load characters
with open("outputs/characters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)

prompt = f"""
You are an expert cinematic image prompt engineer.

Generate one image prompt for each scene.

Requirements:
- Documentary style
- Cinematic lighting
- Ultra detailed
- Consistent characters
- Indian historical aesthetic
- Suitable for Flux, SDXL, Midjourney, Leonardo AI

Return ONLY valid JSON.

Characters:
{json.dumps(characters, indent=2)}

Scenes:
{json.dumps(scenes, indent=2)}
"""

print("🎨 Generating image prompts with Groq...")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.7
)

result = response.choices[0].message.content

# Remove markdown if present
result = result.replace("```json", "")
result = result.replace("```", "")
result = result.strip()

with open("outputs/image_prompts.json", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Image prompts generated!")
print("📄 outputs/image_prompts.json")