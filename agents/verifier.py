import re

def verify_transcript(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Remove repeated words
    text = re.sub(r'\b(\w+)( \1\b)+', r'\1', text)

    # Fix common names
    corrections = {
        "Gaurishak": "Gaurish Akki",
        "Jagdhishwaram": "Jagadish Sharma",
        "Mahabarata": "Mahabharata",
        "Mahabaratha": "Mahabharata",
        "Krushna": "Krishna",
        "Arjun": "Arjuna",
        "Bheeshma": "Bhishma",
    }

    for wrong, correct in corrections.items():
        text = text.replace(wrong, correct)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Verified transcript saved!")

if __name__ == "__main__":
    verify_transcript(
        "outputs/english.txt",
        "outputs/verified_transcript.txt"
    )