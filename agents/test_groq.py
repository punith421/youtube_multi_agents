from groq import Groq

client = Groq(
    api_key="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"
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)