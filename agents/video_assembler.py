import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips

# ==========================================
# CONFIG
# ==========================================

IMAGES_DIR = "outputs_v2/images"
AUDIO_FILE = "outputs_v2/narration.wav"
OUTPUT_VIDEO = "outputs_v2/final_movie.mp4"

print("=" * 70)
print("🎬 VIDEO ASSEMBLER")
print("=" * 70)

# ==========================================
# LOAD IMAGES
# ==========================================

images = sorted([
    os.path.join(IMAGES_DIR, f)
    for f in os.listdir(IMAGES_DIR)
    if f.lower().endswith(".png")
])

if not images:
    raise Exception("❌ No images found in outputs_v2/images")

# ==========================================
# LOAD AUDIO
# ==========================================

if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError(f"❌ Audio file not found: {AUDIO_FILE}")

audio = AudioFileClip(AUDIO_FILE)

duration = audio.duration / len(images)

print(f"🎵 Audio Duration : {audio.duration:.2f} sec")
print(f"🖼️ Images         : {len(images)}")
print(f"⏱️ Time/Image     : {duration:.2f} sec")

# ==========================================
# CREATE VIDEO CLIPS
# ==========================================

clips = []

for img in images:

    clip = (
        ImageClip(img)
        .with_duration(duration)
        .resized(height=1080)
    )

    clips.append(clip)

# ==========================================
# COMBINE VIDEO
# ==========================================

video = concatenate_videoclips(clips, method="compose")
video = video.with_audio(audio)

os.makedirs("outputs_v2", exist_ok=True)

# ==========================================
# EXPORT FINAL VIDEO
# ==========================================

video.write_videofile(
    OUTPUT_VIDEO,
    codec="libx264",
    audio_codec="aac",
    fps=30
)

print("\n" + "=" * 70)
print("✅ FINAL MOVIE CREATED")
print(f"📄 Saved : {OUTPUT_VIDEO}")
print("=" * 70)