from faster_whisper import WhisperModel
import os

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("⏳ Loading model...")

# Best balance of speed + accuracy on M3 Air
model = WhisperModel(
    "medium",
    device="cpu",
    compute_type="int8"
)

print("✅ Model loaded!")
print("🎙️ Transcribing Kannada audio...")

segments, info = model.transcribe(
    "data/audio.webm",
    language="kn",
    task="transcribe",
    beam_size=5
)

transcript_lines = []

for segment in segments:
    print(segment.text)
    transcript_lines.append(segment.text)

transcript_text = "\n".join(transcript_lines)

# Save raw transcript
with open("outputs/raw_transcript.txt", "w", encoding="utf-8") as f:
    f.write(transcript_text)

print("\n✅ Transcription Complete!")
print("📄 Saved: outputs/raw_transcript.txt")