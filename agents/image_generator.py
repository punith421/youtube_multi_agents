import json
import os

os.makedirs("images", exist_ok=True)

with open("outputs/image_prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

count = 0

for i, scene in enumerate(prompts, start=1):

    prompt = scene.get("prompt", "")

    filename = f"images/scene_{i}.txt"

    with open(filename, "w", encoding="utf-8") as out:
        out.write(prompt)

    count += 1

print(f"✅ Saved {count} image prompts to images/")
