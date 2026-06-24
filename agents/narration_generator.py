import google.generativeai as genai

API_KEY = "AQ.Ab8RN6LWIoAdZQlbC9-cpMC3j-HTyLO3ySIklBphVNilFQv7iA"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

with open("outputs/story.txt", "r", encoding="utf-8") as f:
    story = f.read()

prompt = f"""
You are a professional documentary writer.

Convert the following story analysis into a cinematic narration.

Rules:
- Sound like a Netflix documentary.
- Be dramatic and engaging.
- Keep historical and philosophical meaning.
- Write 2-3 minutes of narration.
- Do not use bullet points.

Story:

{story}
"""

response = model.generate_content(prompt)

with open("outputs/narration.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ Narration generated!")
print("📄 outputs/narration.txt")