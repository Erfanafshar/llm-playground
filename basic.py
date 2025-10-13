import os
from openai import OpenAI

# Works with OpenAI cloud or local vLLM
client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are funny and brief"},
        {"role": "user", "content": "Where is your banana?"}
    ],
    temperature=0.5
)

print(response.choices[0].message.content)