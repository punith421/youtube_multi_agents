import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

os.makedirs("images", exist_ok=True)

with open("outputs/image_prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

for i, scene in enumerate(prompts, start=1):

    prompt = scene["prompt"]

    print(f"🎨 Generating Scene {i}...")

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=300
    )

    if response.status_code == 200:

        image_path = f"images/scene_{i}.png"

        with open(image_path, "wb") as img:
            img.write(response.content)

        print(f"✅ Saved {image_path}")

    else:
        print(f"❌ Scene {i} failed")
        print(response.text)

print("🎉 Image generation complete!")