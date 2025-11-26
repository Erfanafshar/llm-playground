from openai import OpenAI
import os

client = OpenAI(os.getenv("OPEN_AI_API_KEY"))

def get_weather(city):
    return f"the weather in {city} is 25 degree and sunny."

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "this function return weather of city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "the city to get the weather for"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

messagess = [
    {"role": "system", "content": "You are helpful and you can call function if needed"},
    {"role": "user", "content": "How is the weather today"}
}]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages = messages,
    tools = tools,
    temperature=0.5
)

message = response.choices[0].message.content
tool_calls = message.tool_calls

if tool_calls:
    call = tool_calls[0]
    fn_name = call.function.name
    args = json.loads(call.function.arguments)
    print(f"model called {fn_name}" with args {args})

    if fn_name == "get_weather":
        result = get_weather(**args)
    else:
        print("wrong function call")

    messages.append({"role": "function", "content": result})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = messages,
        tools = tools,
    )

    print(response.choices[0].message.content)

else:
    print(message.content)