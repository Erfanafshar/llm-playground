from openai import OpenAI
import json

client = OpenAI()

def get_weather(city):
    return f"The weather in {city} is 23°C and sunny."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city to get weather for"}
                },
                "required": ["city"]
            }
        }
    }
]

messages = [
    {"role": "system", "content": "You can call functions if needed."},
    {"role": "user", "content": "What is the weather in Toronto?"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# Step 1: See if model wants to call a function
tool_calls = response.choices[0].message.get("tool_calls")
if tool_calls:
    fn_name = tool_calls[0]["function"]["name"]
    args = json.loads(tool_calls[0]["function"]["arguments"])
    print(f"Model called: {fn_name} with args: {args}")

    # Step 2: Execute the function
    if fn_name == "get_weather":
        result = get_weather(**args)

    # Step 3: Send function result back to model
    messages.append(response.choices[0].message)
    messages.append({"role": "tool", "tool_call_id": tool_calls[0]["id"], "content": result})

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print("\nFinal answer from model:")
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
