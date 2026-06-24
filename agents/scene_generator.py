with open("outputs/verified_transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

scenes = []

paragraphs = text.split(".")

for i, paragraph in enumerate(paragraphs[:10]):
    paragraph = paragraph.strip()

    if paragraph:
        scenes.append(f"Scene {i+1}: {paragraph}")

with open("outputs/scenes.txt", "w", encoding="utf-8") as f:
    for scene in scenes:
        f.write(scene + "\n\n")

print("✅ Scenes generated!")
print("Saved: outputs/scenes.txt")