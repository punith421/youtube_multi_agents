import os
import subprocess

INPUT_AUDIO = "data/audio.webm"
OUTPUT_AUDIO = "data/clean_audio.wav"

os.makedirs("data", exist_ok=True)

print("=" * 60)
print("🎧 AUDIO PREPROCESSOR")
print("=" * 60)

if not os.path.exists(INPUT_AUDIO):
    print(f"❌ Input file not found: {INPUT_AUDIO}")
    exit()

print("🔄 Converting audio...")

command = [
    "ffmpeg",
    "-y",
    "-i", INPUT_AUDIO,

    # Mono audio
    "-ac", "1",

    # Whisper works best with 16kHz
    "-ar", "16000",

    # Normalize loudness
    "-af", "loudnorm",

    OUTPUT_AUDIO
]

result = subprocess.run(command)

if result.returncode == 0:
    print("✅ Audio preprocessing complete!")
    print(f"📁 Saved: {OUTPUT_AUDIO}")
else:
    print("❌ FFmpeg failed.")