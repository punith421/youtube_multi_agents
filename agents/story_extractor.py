import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Get Gemini API Key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Read transcript
with open("outputs_v2/transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

# Prompt
prompt = f"""
You are an expert documentary writer.

Your task is to transform this interview transcript into a cinematic documentary script for an animated movie.

Rules:

- Read the ENTIRE transcript.
- Understand both the host's questions and the guest's answers.
- The host's questions are only context.
- The guest's answers contain the knowledge and must be preserved.
- Convert the conversation into a continuous documentary narration.
- Remove all Host/Guest dialogue.
- Do NOT output questions.
- Do NOT summarize.
- Do NOT invent facts.
- Preserve every important explanation from the guest.
- Improve only the language and flow.
- Make it sound like a professional historical documentary.
- Write scene by scene.

Output format:

Scene 1
Title:
Narration:

Scene 2
Title:
Narration:

Continue until the entire interview has been converted into a complete documentary.

Transcript:

{transcript}
"""

# Generate response
response = model.generate_content(prompt)

# Print output
print("\n========== EXTRACTED QUESTIONS ==========\n")
print(response.text)

# Create output directory if it doesn't exist
os.makedirs("outputs_v2", exist_ok=True)

# Save output
with open("outputs_v2/questions.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("\n✅ Questions extracted successfully!")
print("📄 Saved to: outputs_v2/questions.txt")