from openai import OpenAI
import json
import os

# Create client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                    "city": {
                        "type": "string",
                        "description": "The city to get weather for"
                    }
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

message = response.choices[0].message
tool_calls = message.tool_calls  # direct access (no .get)

if tool_calls:
    call = tool_calls[0]
    fn_name = call.function.name
    args = json.loads(call.function.arguments)
    print(f"Model called: {fn_name} with args: {args}")

    # Run your function
    if fn_name == "get_weather":
        result = get_weather(**args)
    else:
        result = "Unknown tool"

    # Return the tool result to the model
    messages.append(message)
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": result
    })

    final_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    print("\nFinal answer from model:")
    print(final_response.choices[0].message.content)
else:
    print(message.content)
