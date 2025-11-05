from openai import OpenAI
import os
import json
from datetime import datetime

# Client (default OpenAI endpoint)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Python functions (the actual tools) ----
def add_numbers(a, b):
    return a + b

def get_weather(city):
    return f"Mock weather for {city}: 23°C and sunny."

def get_time(timezone):
    # Simple demo: not real TZ handling, just show current time with the label
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"Current time (approx) in {timezone}: {now}"

# ---- Tool declarations (what the model can call) ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather by city (mock).",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time label for a given timezone (demo).",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "description": "IANA zone like America/Toronto"}
                },
                "required": ["timezone"]
            }
        }
    }
]

def run():
    messages = [
        {"role": "system", "content": "You can call tools if needed. Be concise."}
    ]

    user_prompt = input("Ask something (e.g., 'What is 7 + 13?' or 'Time in America/Toronto'): ")
    messages.append({"role": "user", "content": user_prompt})

    # First call: model decides whether to call one or more tools
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools
    )

    assistant_msg = response.choices[0].message
    tool_calls = assistant_msg.tool_calls

    if tool_calls:
        # Handle one or multiple tool calls
        messages.append(assistant_msg)
        for call in tool_calls:
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"[DEBUG] Tool request: {fn_name}({args})")

            if fn_name == "add_numbers":
                result = add_numbers(**args)
            elif fn_name == "get_weather":
                result = get_weather(**args)
            elif fn_name == "get_time":
                result = get_time(**args)
            else:
                result = "Unknown tool."

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": str(result)
            })

        # Second call: model now has tool outputs and produces the final answer
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        print("\nAssistant:", final.choices[0].message.content)
    else:
        # No tools needed; answer directly
        print("\nAssistant:", assistant_msg.content)

if __name__ == "__main__":
    run()