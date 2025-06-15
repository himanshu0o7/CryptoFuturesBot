import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in the environment variables.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def run_search_tool(query="ChatGPT plugin usage", num_results=3):
    tools = [{
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Retrieve info on a technical topic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "options": {
                        "type": "object",
                        "properties": {
                            "num_results": {"type": "number"},
                            "domain_filter": {"type": ["string", "null"]},
                            "sort_by": {
                                "type": ["string", "null"],
                                "enum": ["relevance", "date", "popularity", "alphabetical"]
                            }
                        },
                        "required": ["num_results", "domain_filter", "sort_by"]
                    }
                },
                "required": ["query", "options"]
            }
        }
    }]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Updated to a valid model
            messages=[{"role": "user", "content": f"Please search the knowledge base for {query}"}],
            tools=tools,
            tool_choice={"type": "function", "function": {"name": "search_knowledge_base"}}
        )

        tool_calls = getattr(response.choices[0].message, "tool_calls", None)
        if not tool_calls:
            print("⚠️ No tool_calls in response.")
            return

        for call in tool_calls:
            try:
                args = json.loads(call.function.arguments)
                if "query" not in args or "options" not in args:
                    print("⚠️ Missing required arguments.")
                    continue
                options = args["options"]
                if not all(key in options for key in ["num_results", "domain_filter", "sort_by"]):
                    print("⚠️ Missing required options.")
                    continue
                print(f"\n🔍 Searching: {args['query']}")
                print(f"📊 Options: {options}")
                # Dummy simulation
                print("📚 Top Results (Simulated):")
                print("1. Plugin API Guide – https://platform.openai.com/docs/plugins")
                print("2. Plugin Development – https://openai.com/blog/chatgpt-plugins")
                print("3. Plugin Directory – https://openai.com/plugins")
            except json.JSONDecodeError as e:
                print(f"❌ JSON Decode Error: {e}")
    except Exception as e:
        print(f"❌ API Request Failed: {e}")

# Example usage
if __name__ == "__main__":
    run_search_tool()

