import os
import json
import requests
from pathlib import Path

from dotenv import load_dotenv
from runwayml import RunwayML


# ---------------------------------------------------
# Load Environment
# ---------------------------------------------------

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("RUNWAY_API_KEY")

if not API_KEY:
    raise ValueError("RUNWAY_API_KEY not found in .env")

client = RunwayML(api_key=API_KEY)


# ---------------------------------------------------
# Files
# ---------------------------------------------------

INPUT_FILE = "outputs_v2/image_prompts.json"
OUTPUT_DIR = "outputs_v2/images"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# Download Image
# ---------------------------------------------------

def download_image(url, save_path):

    response = requests.get(url, timeout=300)
    response.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(response.content)

    print(f"✅ Saved: {save_path}")


# ---------------------------------------------------
# Generate Image
# ---------------------------------------------------

def generate_image(scene):

    scene_id = scene["scene_id"]

    print(f"\n🎬 Generating Scene {scene_id}")

    try:

        # This matches image_prompt_generator.py
        prompt = scene["image_prompt"]

        # Runway prompt length limit
        if len(prompt) > 1000:
            prompt = prompt[:1000]

        task = client.text_to_image.create(
            model="gen4_image",
            prompt_text=prompt,
            ratio="1920:1080"
        ).wait_for_task_output()

        image_url = task.output[0]

        filename = os.path.join(
            OUTPUT_DIR,
            f"scene_{scene_id:03}.png"
        )

        download_image(image_url, filename)

        return True

    except Exception as e:

        print(f"❌ Scene {scene_id} Failed")
        print(e)

        return False


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        scenes = json.load(f)

    print("=" * 60)
    print("🎨 RUNWAY IMAGE GENERATOR")
    print("=" * 60)

    success = 0

    for scene in scenes:

        if generate_image(scene):
            success += 1

    print("\n" + "=" * 60)
    print(f"✅ Finished: {success}/{len(scenes)} images")
    print("=" * 60)


if __name__ == "__main__":
    main()