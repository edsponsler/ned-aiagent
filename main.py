import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="NEDs AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access 'args.user_prompt'

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

def generate_content(client, messages):
    return client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=messages
    )

def main():
    response = generate_content(client, messages)
    if response.usage_metadata:
        if args.verbose:
            print(f"User prompt: {messages}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("No usage metadata returned")

    print(f"\n{response.text}")

if __name__ == "__main__":
    main()
