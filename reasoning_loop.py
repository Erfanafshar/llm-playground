from openai import OpenAI
import os, json
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- tools (real implementations) ---
def add_numbers(a, b): return a + b
def get_weather(city): return f"Mock weather for {city}: 23°C and sunny."
TOOLS = {
    "add_numbers": add_numbers,
    "get_weather": get_weather,
}

# --- tool declarations (schema shown to the model) ---
tool_specs = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
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
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    }
]

SYSTEM = "You can call tools. Think step-by-step. If finished, answer the user without calling more tools."

def call_model(messages, with_tools=True):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tool_specs if with_tools else None
    ).choices[0].message

def run():
    messages = [{"role": "system", "content": SYSTEM}]
    user = input("Ask something: ")
    messages.append({"role": "user", "content": user})

    # simple reasoning loop: attempt up to 3 tool rounds
    for _ in range(3):
        msg = call_model(messages, with_tools=True)
        if not msg.tool_calls:
            print("\nAssistant:", msg.content)
            return
        messages.append(msg)
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            fn = TOOLS.get(name)
            result = "Unknown tool" if fn is None else fn(**args)
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": str(result)})

    # final answer after last tool round
    final = call_model(messages, with_tools=False)
    print("\nAssistant:", final.content)

if __name__ == "__main__":
    run()
