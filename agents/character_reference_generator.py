import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json",
}

INPUT_FILE = "outputs/characters.json"
OUTPUT_DIR = "outputs/character_reference"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_image(prompt, output_path):

    payload = {
        "inputs": prompt
    }

    for attempt in range(5):

        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=300
        )

        if response.status_code == 200:

            with open(output_path, "wb") as f:
                f.write(response.content)

            return True

        print(f"Retry {attempt+1}/5")
        print(response.text)
        time.sleep(15)

    return False


def main():

    print("=" * 60)
    print("🎭 CHARACTER REFERENCE GENERATOR")
    print("=" * 60)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        characters = json.load(f)

    success = 0

    for character in characters:

        name = character["name"]
        prompt = character["image_prompt"]

        filename = os.path.join(
            OUTPUT_DIR,
            f'{character["character_id"]}.png'
        )

        print(f"\nGenerating {name}")

        ok = generate_image(prompt, filename)

        if ok:
            print("✅ Saved:", filename)
            success += 1
        else:
            print("❌ Failed")

    print("\n" + "=" * 60)
    print(f"Finished : {success}/{len(characters)} characters")
    print("=" * 60)


if __name__ == "__main__":
    main()