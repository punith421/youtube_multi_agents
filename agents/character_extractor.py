import os
import json
from dotenv import load_dotenv
from google import genai

# ==========================================
# LOAD GEMINI
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

INPUT_FILE = "outputs_v2/scene_plan.json"
OUTPUT_FILE = "outputs_v2/characters.json"

# ==========================================
# PROMPT
# ==========================================

PROMPT = """
You are a world-class Character Designer for cinematic animated historical documentaries.

Your task is to analyze the ENTIRE scene plan before extracting characters.

IMPORTANT RULES

- Read every scene completely.
- Extract ONLY important recurring characters.
- Ignore narrator.
- Ignore crowd.
- Ignore villagers.
- Ignore soldiers unless they are important.
- Ignore background people.

Include:

- Gods
- Goddesses
- Kings
- Queens
- Princes
- Princesses
- Sages
- Warriors
- Demons
- Important recurring animals
- Every important recurring historical or mythological character

VERY IMPORTANT

If a character appears in multiple scenes:

- Merge all appearances.
- Create ONE complete profile.
- Keep appearance identical across the entire movie.
- Never create duplicate characters.

If appearance is not fully described:

Infer only visually necessary details that are historically accurate for the Mahabharata period.

Return EVERY character using this format:

{
  "character_id":"",
  "name":"",
  "gender":"",
  "approximate_age":"",
  "role":"",
  "importance":"",
  "skin_tone":"",
  "face":"",
  "eyes":"",
  "hair":"",
  "beard":"",
  "body":"",
  "height":"",
  "dress":"",
  "jewelry":"",
  "weapon":"",
  "accessories":"",
  "personality":"",
  "expression":"",
  "walking_style":"",
  "voice":"",
  "image_prompt":""
}

IMAGE PROMPT RULES

Generate one highly detailed cinematic image prompt for each character.

Include:

- Historical accuracy
- Ancient Indian clothing
- Facial details
- Hairstyle
- Jewelry
- Accessories
- Body posture
- Lighting
- Ultra realistic
- Cinematic
- High detail
- Consistent appearance
- Suitable for AI image generation

Return ONLY a JSON ARRAY.

Example:

[
  {
    "character_id":"CHAR001",
    "name":"Lord Shiva",
    "gender":"Male"
  },
  {
    "character_id":"CHAR002",
    "name":"Arjuna",
    "gender":"Male"
  }
]

Never return markdown.

Never return explanations.

Only return valid JSON.
"""

# ==========================================
# MAIN
# ==========================================

def extract_characters():

    print("=" * 60)
    print("🎭 CHARACTER EXTRACTOR")
    print("=" * 60)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        scene_plan = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT + "\n\nScene Plan:\n\n" + scene_plan
    )

    text = response.text.strip()

    # Remove markdown if Gemini returns it
    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    # Validate JSON
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        print("❌ Gemini did not return valid JSON.")
        print(text)
        return

    os.makedirs("outputs_v2", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(parsed, f, indent=4, ensure_ascii=False)

    print("\n✅ Characters Extracted Successfully!")
    print(f"📄 Saved: {OUTPUT_FILE}")

    print("\nCharacters Found:\n")

    for character in parsed:
        print(f"✓ {character.get('name', 'Unknown')} ({character.get('role', 'Unknown')})")


if __name__ == "__main__":
    extract_characters()