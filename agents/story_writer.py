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

# Updated paths
INPUT_FILE = "outputs_v2/transcript.txt"
OUTPUT_FILE = "outputs_v2/story.txt"

print("=" * 60)
print("📖 STORY WRITER")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    transcript = f.read()

PROMPT = f"""
You are one of the world's best documentary writers.

Your documentaries feel like Netflix, BBC, Discovery and National Geographic.

Your task is to convert this interview transcript into a cinematic documentary script for an animated movie.

STRICT RULES

1. Read the COMPLETE transcript.
2. Understand both the host's questions and the guest's answers.
3. Preserve every important explanation from the guest.
4. Do NOT invent facts.
5. Remove filler words and repetitions.
6. Remove the interview format completely.
7. Do NOT write Host or Guest.
8. Convert everything into one smooth documentary narration.
9. Build suspense naturally.
10. Keep the historical timeline correct.
11. Use simple spoken English.
12. Write emotionally and cinematically.
13. Make every paragraph naturally lead into the next.
14. Help the audience visualize every moment.
15. This script will later become an animated movie.

Output ONLY the documentary script.

Transcript:

{transcript}
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=PROMPT
)

story = response.text.strip()

os.makedirs("outputs_v2", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(story)

print("\n✅ Story created!")
print("📄 Saved:", OUTPUT_FILE)