import os
import requests
import json
from dotenv import load_dotenv

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": "What files are in the current directory?"}]}],
        "tools": [{"functionDeclarations": [{"name": "get_files_info", "description": "foo", "parameters": {"type": "OBJECT", "properties": {"directory": {"type": "STRING"}}}}]}]
    }
    r = requests.post(url, json=payload)
    print("Response JSON:")
    print(json.dumps(r.json(), indent=2))

if __name__ == "__main__":
    main()
