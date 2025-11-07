from openai import OpenAI
import os, json, glob

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- super-simple local "retriever" (no extra libs) ----
def load_corpus(folder="data"):
    docs = []
    for path in glob.glob(os.path.join(folder, "*.txt")):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        docs.append({"path": path, "text": text})
    return docs

CORPUS = load_corpus()

def search_notes(query, top_k=3):
    q = query.lower()
    scored = []
    for d in CORPUS:
        # naive score: count of query tokens appearing in text
        score = sum(t in d["text"].lower() for t in q.split())
        if score > 0:
            # return a short snippet to avoid overloading tokens
            snippet = d["text"][:800]
            scored.append((score, d["path"], snippet))
    scored.sort(key=lambda x: x[0], reverse=True)
    hits = [{"path": p, "snippet": s} for _, p, s in scored[:top_k]]
    return hits if hits else [{"path": None, "snippet": "No relevant notes found."}]

# ---- tool schema given to the model ----
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_notes",
            "description": "Search local knowledge base notes for relevant snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "minimum": 1, "maximum": 5}
                },
                "required": ["query"]
            }
        }
    }
]

def run():
    messages = [
        {"role": "system", "content": "You can call tools. If you need facts, use search_notes first, then answer citing file paths."}
    ]
    user = input("Ask something (RAG): ")
    messages.append({"role": "user", "content": user})

    # first call: model may request retrieval
    r1 = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
    a1 = r1.choices[0].message
    tool_calls = a1.tool_calls

    if tool_calls:
        messages.append(a1)
        for tc in tool_calls:
            if tc.function.name == "search_notes":
                args = json.loads(tc.function.arguments)
                result = search_notes(**args)
                messages.append({"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)})
        # second call: model composes final answer using retrieved snippets
        r2 = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
        print("\nAssistant:", r2.choices[0].message.content)
    else:
        print("\nAssistant:", a1.content)

if __name__ == "__main__":
    run()
