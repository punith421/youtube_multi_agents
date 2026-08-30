import json
import os
import urllib.parse
import requests

# Create images folder
os.makedirs("images", exist_ok=True)

# Load prompts
with open("outputs/image_prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

print(f"🎬 Found {len(prompts)} scenes")

for i, scene in enumerate(prompts, start=1):

    prompt = scene["prompt"]

    print(f"\n🎨 Generating Scene {i}...")
    print(prompt[:80] + "...")

    # Encode prompt
    encoded = urllib.parse.quote(prompt)

    # Pollinations AI
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        "?width=1280"
        "&height=720"
        "&model=flux"
        f"&seed={i}"
    )

    response = requests.get(url, timeout=300)

    if response.status_code == 200:

        filename = f"images/scene_{i}.png"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✅ Saved {filename}")

    else:

        print("❌ Failed")
        print(response.text)

print("\n🎉 All scenes generated successfully!")