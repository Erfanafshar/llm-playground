import json, os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_web_data(topic):
    """Fake external API – reads from local JSON instead of internet."""
    data = {
        "weather": "Today is sunny, 22°C with light wind.",
        "bitcoin": "Bitcoin is trading around $68,000.",
        "ai": "AI research is rapidly advancing, especially in multimodal models like GPT-4o."
    }
    # basic lookup
    for k, v in data.items():
        if k in topic.lower():
            return v
    return "Sorry, no live data found for that topic."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_web_data",
            "description": "Fetch external (mock) data like weather, bitcoin price, or AI news.",
            "parameters": {
                "type": "object",
                "properties": {"topic": {"type": "string"}},
                "required": ["topic"]
            }
        }
    }
]

def run():
    messages = [{"role": "system", "content": "You can call get_web_data for real-time info."}]
    user = input("Ask about weather, bitcoin, or AI: ")
    messages.append({"role": "user", "content": user})

    r1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
    a1 = r1.choices[0].message
    tool_calls = a1.tool_calls

    if tool_calls:
        messages.append(a1)
        for tc in tool_calls:
            if tc.function.name == "get_web_data":
                args = json.loads(tc.function.arguments)
                result = get_web_data(**args)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
        r2 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        print("\nAssistant:", r2.choices[0].message.content)
    else:
        print("\nAssistant:", a1.content)

if __name__ == "__main__":
    run()
