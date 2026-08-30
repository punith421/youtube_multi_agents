import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

# --------------------------------------------------
# Load Environment
# --------------------------------------------------

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# --------------------------------------------------
# Files
# --------------------------------------------------

INPUT_FILE = "outputs_v2/transcript.txt"
OUTPUT_DIR = "outputs_v2"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "speaker_segments.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Read Transcript
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    transcript = f.read()

# --------------------------------------------------
# Prompt
# --------------------------------------------------

PROMPT = f"""
You are an expert podcast analyzer.

Your task is:

1. Read the transcript.
2. Detect every speaker.
3. Label them logically.

Use labels like:

Host
Guest
Speaker 1
Speaker 2

Return ONLY valid JSON.

Format:

[
 {{
   "speaker":"Host",
   "text":"..."
 }},
 {{
   "speaker":"Guest",
   "text":"..."
 }}
]

Transcript:

{transcript}
"""

# --------------------------------------------------
# Gemini
# --------------------------------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=PROMPT
)

text = response.text.strip()

# Remove markdown if Gemini adds it
text = text.replace("```json", "")
text = text.replace("```", "")
text = text.strip()

# --------------------------------------------------
# Save JSON
# --------------------------------------------------

try:

    data = json.loads(text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("=" * 60)
    print("✅ Speaker Identification Complete")
    print("Saved:", OUTPUT_FILE)
    print("=" * 60)

except Exception as e:

    print("=" * 60)
    print("❌ Failed to parse Gemini response")
    print("=" * 60)

    print(text)

    raise e