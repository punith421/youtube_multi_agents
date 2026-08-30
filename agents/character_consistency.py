import json
import os

INPUT_FILE = "outputs/characters.json"
OUTPUT_FILE = "outputs/character_reference.json"


def build_reference():

    print("=" * 60)
    print("🎭 CHARACTER CONSISTENCY AGENT")
    print("=" * 60)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        characters = json.load(f)

    references = {}

    for character in characters:

        references[character["name"]] = {
            "character_id": character.get("character_id", ""),
            "gender": character.get("gender", ""),
            "age": character.get("approximate_age", ""),
            "role": character.get("role", ""),
            "skin_tone": character.get("skin_tone", ""),
            "face": character.get("face", ""),
            "eyes": character.get("eyes", ""),
            "hair": character.get("hair", ""),
            "beard": character.get("beard", ""),
            "body": character.get("body", ""),
            "height": character.get("height", ""),
            "dress": character.get("dress", ""),
            "jewelry": character.get("jewelry", ""),
            "weapon": character.get("weapon", ""),
            "accessories": character.get("accessories", ""),
            "personality": character.get("personality", ""),
            "expression": character.get("expression", ""),
            "walking_style": character.get("walking_style", ""),
            "voice": character.get("voice", ""),
            "master_prompt": character.get("image_prompt", "")
        }

    os.makedirs("outputs", exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(references, f, indent=4, ensure_ascii=False)

    print("\n✅ Character reference library created")
    print(f"📄 Saved: {OUTPUT_FILE}")

    print("\nCharacters:")
    for name in references:
        print("✓", name)


if __name__ == "__main__":
    build_reference()