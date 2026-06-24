with open("outputs/english.txt", "r", encoding="utf-8") as f:
    text = f.read()

words = text.split()

print("\n=== Transcript Quality Report ===")
print(f"Total Words: {len(words)}")

repeated = []

for i in range(len(words)-1):
    if words[i].lower() == words[i+1].lower():
        repeated.append(words[i])

print(f"Repeated Words Found: {len(repeated)}")

if repeated:
    print("Examples:", repeated[:20])

print("\nManual Check Needed:")
print("- Character names")
print("- Mahabharata terms")
print("- Repeated phrases")
print("- Wrong translations")