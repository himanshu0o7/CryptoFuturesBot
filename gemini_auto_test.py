import google.generativeai as genai
import subprocess
import os

genai.configure(api_key="YOUR_GEMINI_API_KEY")


def run_script(script_name):
    result = subprocess.run(["python", script_name], capture_output=True, text=True)
    return result.stderr if result.stderr else result.stdout


def gemini_autofix(file_name, error_output):
    with open(file_name, "r") as f:
        code = f.read()

    prompt = f"""
    Fix the following error in {file_name}:
    
    {error_output}
    
    Here is the existing code:
    {code}
    
    Provide corrected Python code only.
    """

    response = genai.GenerativeModel("gemini-1.5-pro").generate_content(prompt)
    return response.text


script_to_test = "main.py"
error_log = run_script(script_to_test)

if "Traceback" in error_log:
    print("🔴 Error detected:\n", error_log)
    fix = gemini_autofix(script_to_test, error_log)
    print("✅ Gemini Suggested Fix:\n", fix)
else:
    print("🟢 Test Passed:\n", error_log)
