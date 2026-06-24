from PIL import Image, ImageDraw

import json
import os

os.makedirs("images", exist_ok=True)

with open("outputs/scenes.json", "r", encoding="utf-8") as f:
    scenes = json.load(f)

for scene in scenes:

    num = scene["scene_number"]

    img = Image.new("RGB", (1280, 720), color=(40, 80, 180))

    draw = ImageDraw.Draw(img)

    text = f"SCENE {num}"

    draw.text(
        (450, 320),
        text,
        fill=(255, 255, 255)
    )

    img.save(f"images/scene_{num}.png")

print("✅ New placeholder images created!")