import os
import numpy as np
import soundfile as sf
from kokoro import KPipeline

# ==========================================
# CONFIG
# ==========================================

INPUT_FILE = "outputs_v2/story.txt"
OUTPUT_FILE = "outputs_v2/narration.wav"

VOICE = "am_adam"

SAMPLE_RATE = 24000

# ==========================================
# START
# ==========================================

print("=" * 70)
print("🎙️ AI VOICE GENERATOR")
print("=" * 70)

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found!")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read().strip()

print("📖 Story loaded")

print("🧠 Loading Kokoro model...")
pipeline = KPipeline(lang_code="a")

print("✅ Model Loaded")
print("🎤 Generating voice...\n")

audio_chunks = []

for _, _, audio in pipeline(
    text,
    voice=VOICE
):
    audio_chunks.append(audio)

if not audio_chunks:
    raise RuntimeError("Voice generation failed.")

final_audio = np.concatenate(audio_chunks)

os.makedirs("outputs_v2", exist_ok=True)

sf.write(
    OUTPUT_FILE,
    final_audio,
    SAMPLE_RATE
)

print("\n" + "=" * 70)
print("✅ Voice Generated Successfully")
print(f"🎧 Voice : {VOICE}")
print(f"📄 Saved : {OUTPUT_FILE}")
print("=" * 70)