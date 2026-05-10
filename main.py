import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions import wrappers
from prompts import SYSTEM_PROMPT

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="NEDs AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Configure the wrappers module
wrappers.VERBOSE = args.verbose
wrappers.WORKING_DIRECTORY = "./calculator"


def main():
    # Utilizing SDK chats component to manage the conversation history natively.
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=wrappers.tools_list,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False, maximum_remote_calls=20),
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    response = chat.send_message(args.user_prompt)

    if response.usage_metadata:
        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        if args.verbose:
            print("Warning: No usage metadata returned")

    print(f"\n{response.text}")


if __name__ == "__main__":
    main()
