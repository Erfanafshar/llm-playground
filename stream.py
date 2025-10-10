from openai import OpenAI
import os
import sys

client = OpenAI()

def stream_chat(prompt, temperature=0.7):
    response_stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        stream=True
    )

    print("\nModel output:\n")
    for event in response_stream:
        if event.choices and event.choices[0].delta.get("content"):
            text = event.choices[0].delta["content"]
            sys.stdout.write(text)
            sys.stdout.flush()
    print("\n\n--- stream finished ---\n")

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    try:
        temperature = float(input("Enter temperature (0–1, default 0.7): ") or 0.7)
    except ValueError:
        temperature = 0.7
    stream_chat(prompt, temperature)
