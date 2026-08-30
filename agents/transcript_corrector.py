import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise Exception("❌ GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================
# SPLIT TRANSCRIPT
# ==========================================

def split_text(text, max_chars=4000):
    chunks = []
    current = ""

    for line in text.split("\n"):
        if len(current) + len(line) < max_chars:
            current += line + "\n"
        else:
            chunks.append(current)
            current = line + "\n"

    if current:
        chunks.append(current)

    return chunks


# ==========================================
# PROMPT
# ==========================================

PROMPT = """
You are an expert Kannada language editor.

Your task is to correct the transcript.

Rules:

1. Keep 100% meaning.
2. Do NOT summarize.
3. Do NOT remove sentences.
4. Correct Kannada spelling.
5. Correct punctuation.
6. Correct Sanskrit names.
7. Remove OCR/transcription mistakes.
8. Keep paragraph order.
9. Return ONLY corrected Kannada.

Transcript:

"""


# ==========================================
# MAIN FUNCTION
# ==========================================

def correct_transcript(input_file):

    print("=" * 60)
    print("🧠 GEMINI TRANSCRIPT CORRECTOR")
    print("=" * 60)

    with open(input_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    chunks = split_text(transcript)

    corrected = []

    total = len(chunks)

    for i, chunk in enumerate(chunks):

        print(f"Chunk {i+1}/{total}")

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=PROMPT + chunk
        )

        corrected.append(response.text)

    final_text = "\n\n".join(corrected)

    output_file = Path(OUTPUT_DIR) / "final_transcript.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_text)

    print("\n✅ Transcript corrected")
    print(f"📄 Saved: {output_file}")

    return str(output_file)


if __name__ == "__main__":
    correct_transcript("outputs/transcript.txt")