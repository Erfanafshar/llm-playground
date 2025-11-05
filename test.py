import json 

raw = '{"city": "Toronto"}'
args = json.loads(raw)

def get_weather(city):
    print(f"The weather in {city} is 23C and sunny.")

get_weather(**args)