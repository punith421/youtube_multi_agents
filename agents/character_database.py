import google.generativeai as genai
import json

API_KEY = "AQ.Ab8RN6LWIoAdZQlbC9-cpMC3j-HTyLO3ySIklBphVNilFQv7iA"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

with open("outputs/scenes.json", "r", encoding="utf-8") as f:
    scenes = f.read()

prompt = f"""
You are an expert character designer.

Analyze the scenes and create a character database.

For each character provide:

- name
- gender
- role
- age_group
- appearance
- clothing
- personality

Return ONLY valid JSON.

Scenes:

{scenes}
"""

print("👥 Generating character database...")

response = model.generate_content(prompt)

character_text = response.text
character_text = character_text.replace("```json", "").replace("```", "").strip()

with open("outputs/characters.json", "w", encoding="utf-8") as f:
    f.write(character_text)

print("✅ Character database generated!")
print("📄 outputs/characters.json")