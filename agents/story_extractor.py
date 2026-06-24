import google.generativeai as genai

API_KEY = "AQ.Ab8RN6LWIoAdZQlbC9-cpMC3j-HTyLO3ySIklBphVNilFQv7iA"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

with open("outputs/verified_transcript.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

prompt = f"""
Analyze this Mahabharata discussion and return:

1. Episode Title
2. Summary (5-10 lines)
3. People Mentioned
4. Mahabharata Characters Mentioned
5. Main Topics
6. Key Events Discussed
7. 10 Animation Scene Ideas

Format clearly with headings.

Transcript:

{transcript}
"""

response = model.generate_content(prompt)

with open("outputs/story.txt", "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ Story extracted!")
print("📄 outputs/story.txt")