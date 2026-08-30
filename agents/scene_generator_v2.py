import google.generativeai as genai


def generate_scenes():
    with open("outputs/narration.txt", "r", encoding="utf-8") as f:
        narration = f.read()

    prompt = f"""
You are a professional film director and storyboard artist.

Convert the narration into a sequence of cinematic scenes.

For each scene provide:

- scene_number
- duration_seconds
- visual_description
- camera_movement
- characters
- voiceover

Return ONLY valid JSON.

Narration:

{narration}
"""

    print("🎬 Generating scenes...")

    response = model.generate_content(prompt)

    scene_text = response.text

    # Remove markdown if Gemini adds it
    scene_text = scene_text.replace("```json", "").replace("```", "").strip()

    with open("outputs/scenes.json", "w", encoding="utf-8") as f:
        f.write(scene_text)

    print("✅ Scenes generated!")
    print("📄 outputs/scenes.json")

    return "outputs/scenes.json"