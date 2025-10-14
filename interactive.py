from openai import OpenAI
import os

# Create client
client = OpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# System message defines tone and rules
messages = [
    {"role": "system", "content": "be helpful and concise"}
]

print("Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Bye!")
        break

    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Send full conversation so far
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=1.0,
    )

    # Extract model reply
    reply = response.choices[0].message.content
    print("Assistant:", reply, "\n")

    # Add assistant reply back into history
    messages.append({"role": "assistant", "content": reply})
