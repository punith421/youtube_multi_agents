from google import genai
from dotenv import load_dotenv
from pathlib import Path
import os
import time

# ==============================
# Load API Key
# ==============================

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

INPUT_FILE = "outputs/raw_transcript.txt"
OUTPUT_FILE = "outputs/verified_transcript.txt"

# ==============================
# Read transcript
# ==============================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    transcript = f.read()

print("📖 Transcript loaded.")

# ==============================
# Split into chunks
# ==============================

CHUNK_SIZE = 6000

chunks = [
    transcript[i:i + CHUNK_SIZE]
    for i in range(0, len(transcript), CHUNK_SIZE)
]

print(f"🧩 Total chunks: {len(chunks)}")

verified_chunks = []

# ==============================
# Process every chunk
# ==============================

for index, chunk in enumerate(chunks, start=1):

    print(f"\n🔹 Processing chunk {index}/{len(chunks)}")

    prompt = f"""
You are an expert editor, translator and Indian mythology scholar.

Your job:

1. Translate Kannada into natural English.
2. Preserve EVERY sentence.
3. Never summarize.
4. Never omit information.
5. Correct transcription mistakes.
6. Correct grammar and punctuation.
7. Remove repeated phrases caused by speech recognition.
8. Preserve interview format.
9. Keep Mahabharata names correct.

Examples:

Mahabharata
Vyasa
Krishna
Arjuna
Bhima
Nakula
Sahadeva
Draupadi
Kunti
Karna
Bhishma
Duryodhana
Dhritarashtra
Panchala
Kumaravyasa
Pampa Bharata

Return ONLY the corrected English transcript.

Transcript:

{chunk}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    verified_chunks.append(response.text.strip())

    time.sleep(1)

# ==============================
# Save
# ==============================

final_text = "\n\n".join(verified_chunks)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_text)

print("\n✅ Verification Complete!")
print(f"📄 Saved: {OUTPUT_FILE}")