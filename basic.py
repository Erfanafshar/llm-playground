from openai import OpenAI

# Works with OpenAI cloud or local vLLM
client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key="your_api_key_here"
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Retrieval-Augmented Generation in one line."}
    ],
    temperature=0.3
)

print(response.choices[0].message.content)