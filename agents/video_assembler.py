from moviepy import ImageClip, concatenate_videoclips
import os

clips = []

for i in range(1, 8):
    image_path = f"images/scene_{i}.png"

    if os.path.exists(image_path):
        clip = ImageClip(image_path).with_duration(3)
        clips.append(clip)

final_video = concatenate_videoclips(clips, method="compose")

final_video.write_videofile(
    "outputs/final_video.mp4",
    fps=24
)

print("✅ Video created!")