from openai import OpenAI
import os
import json

client = OpenAI()

system_prompt = """
You are a precise text analyst. 
Always respond only in valid JSON using this format:
{
  "summary": "one-sentence summary of the text",
  "tags": ["list", "of", "keywords"],
  "tone": "neutral / positive / negative"
}
"""

text = input("Enter a paragraph to analyze:\n")

def get_json_response(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt_text}
        ]
    )
    return response.choices[0].message.content.strip()

raw_output = get_json_response(f"Analyze this text:\n{text}")

for attempt in range(2):
    try:
        data = json.loads(raw_output)
        print("\nParsed JSON:")
        print(json.dumps(data, indent=4))
        break
    except json.JSONDecodeError:
        print(f"\nAttempt {attempt+1}: Failed to parse JSON, retrying...")
        raw_output = get_json_response(
            f"The previous output was invalid JSON. Please fix it and return only valid JSON:\n{raw_output}"
        )
else:
    print("\nFailed to produce valid JSON after retries.")
