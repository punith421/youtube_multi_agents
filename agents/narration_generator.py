import os
from dotenv import load_dotenv
from google import genai

# ==========================================
# LOAD GEMINI
# ==========================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

INPUT_FILE = "outputs/final_transcript.txt"
OUTPUT_FILE = "outputs/narration.txt"

print("=" * 60)
print("🎙️ NARRATION GENERATOR")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    transcript = f.read()

PROMPT = f"""
You are a professional Netflix documentary writer.

Transform the following transcript into a cinematic documentary narration.

Requirements:

- Natural spoken English
- Emotionally engaging
- Dramatic storytelling
- Historical accuracy
- Keep the original meaning
- Smooth transitions
- No bullet points
- No scene numbers
- No speaker names
- Suitable for AI voice generation
- Around 2–3 minutes long

Transcript:

{transcript}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=PROMPT
)

narration = response.text.strip()

os.makedirs("outputs", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(narration)

print("\n✅ Narration generated!")
print(f"📄 Saved: {OUTPUT_FILE}")