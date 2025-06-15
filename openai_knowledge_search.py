# openai_knowledge_search.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env and get API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY missing in .env")

# Initialize client
client = OpenAI(api_key=api_key)
print(f"🔑 Loaded Key: {api_key[:20]}...")

# Define the function tool GPT can call
functions = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Search for latest ChatGPT plugin usage tips",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"},
                    "options": {
                        "type": "object",
                        "properties": {
                            "num_results": {"type": "integer"},
                            "domain_filter": {"type": ["string", "null"]},
                            "sort_by": {"type": "string"}
                        },
                        "required": ["num_results", "sort_by"]
                    }
                },
                "required": ["query", "options"]
            }
        }
    }
]

# Create GPT chat request
response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "How to use ChatGPT plugins in 2025?"}
    ],
    tools=functions,
    tool_choice={"type": "function", "function": {"name": "search_knowledge_base"}},
)

# Extract and print tool call
tool_calls = response.choices[0].message.tool_calls
if tool_calls:
    for call in tool_calls:
        function_name = call.function.name
        arguments = call.function.arguments
        print(f"\n🛠️ GPT wants to call this function:")
        print(f"🔧 Function Name: {function_name}")
        print(f"📦 Arguments: {arguments}")
        print(f"🔍 Simulating: Searching for '{eval(arguments)['query']}'")
else:
    print("⚠️ No tool_calls in response.")

