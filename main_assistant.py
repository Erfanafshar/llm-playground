from openai import OpenAI
import os, json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Tool functions -----
def search_notes(query, top_k=3):
    pass

def get_web_data(topic):
    pass

# --- Tools regsigery -------
tools = [
    "type: function",
    "function": {
        "name": "get rag"
        "description": "get file info"
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "the city is big"
                },
                "required": ["city"]
            }
        }
    }
]

def run():
    print("AI assistant ready, (type 'exit' to quit)\n")
    messages = [
        {"role": "system", "content": "You are a helpful assistant that can use tools to find or fetch facts."}
    ]

    while True:
        user = input("You: ")
        if user.lower() == "exit":
            print("Assistant: Bye!")
            break
        
        messages.append(
            {"role": "user", "content": user}
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = messages,
            tools = tools,
            temperature = 0.5
        )

        messages.append("role": "assistant", "content": response)

        print(f"Assistant: {response.choices[0].message.content}")

if __name__ == "__main__":
    run()
