import re

CHARACTERS = [
    "Krishna",
    "Arjuna",
    "Karna",
    "Bhishma",
    "Drona",
    "Duryodhana",
    "Yudhishthira",
    "Nakula",
    "Sahadeva",
    "Draupadi",
    "Kunti",
    "Gandhari",
    "Dhritarashtra",
    "Vyasa",
    "Shakuni",
    "Pandava",
    "Kaurava"
]

with open("outputs/verified_transcript.txt", "r", encoding="utf-8") as f:
    text = f.read()

found = []

for character in CHARACTERS:
    if re.search(character, text, re.IGNORECASE):
        found.append(character)

with open("outputs/characters.txt", "w", encoding="utf-8") as f:
    for character in found:
        f.write(character + "\n")

print("\nCharacters Found:")
for character in found:
    print("✓", character)

print("\nSaved: outputs/characters.txt")