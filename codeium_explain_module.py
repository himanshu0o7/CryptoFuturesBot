import os
import openai
import argparse
from dotenv import load_dotenv

# ✅ Load .env explicitly from current script directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# ✅ Fetch API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or "your_real_key_here" in api_key:
    raise ValueError(f"❌ OPENAI_API_KEY is missing or invalid → {api_key}")

# ✅ Set API key for openai
openai.api_key = api_key


def extract_target_blocks(file_path):
    blocks = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    block = []
    mode = None

    for line in lines:
        if line.strip().startswith("# EXPLAIN:"):
            if block:
                blocks.append((mode, block))
            block = []
            mode = "EXPLAIN"
        elif line.strip().startswith("# FIX:"):
            if block:
                blocks.append((mode, block))
            block = []
            mode = "FIX"
        elif mode:
            block.append(line)
    if block:
        blocks.append((mode, block))

    return blocks


def explain_code(code, mode):
    prompt = (
        f"{'Explain' if mode == 'EXPLAIN' else 'Fix'} the following code:\n"
        + "".join(code)
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        suggestion = response.choices[0].message["content"]
        return suggestion.strip()
    except Exception as e:
        return f"❌ Error: {e}"


def process_file(file_path):
    blocks = extract_target_blocks(file_path)
    for i, (mode, block) in enumerate(blocks, 1):
        print(f"\n🔍 Block {i} ({mode}):")
        print("".join(block))
        suggestion = explain_code(block, mode)
        print(f"\n✅ Suggestion:\n{suggestion}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Code Explain/Fix Assistant")
    parser.add_argument("file", help="Path to the Python file to analyze")
    args = parser.parse_args()
    process_file(args.file)
