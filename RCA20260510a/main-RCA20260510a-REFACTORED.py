import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from prompts import SYSTEM_PROMPT

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="NEDs AI Agent")
parser.add_argument("user_prompt", type=str, help="The prompt to send to the AI")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


# Define wrapper functions so the SDK can infer schemas and we can inject working_directory
def get_file_content_tool(file_path: str) -> str:
    """Returns the content of a file relative to the working directory."""
    if args.verbose:
        print(f" - Calling function: get_file_content(file_path='{file_path}')")
    return get_file_content(working_directory="./calculator", file_path=file_path)

def get_files_info_tool(directory: str) -> str:
    """Returns information about files in the specified directory."""
    if args.verbose:
        print(f" - Calling function: get_files_info(directory='{directory}')")
    return get_files_info(working_directory="./calculator", directory=directory)

def run_python_file_tool(file_path: str) -> str:
    """Executes a Python script from the working directory and returns its standard output and error."""
    if args.verbose:
        print(f" - Calling function: run_python_file(file_path='{file_path}')")
    return run_python_file(working_directory="./calculator", file_path=file_path)

def write_file_tool(file_path: str, content: str) -> str:
    """Writes the given content to a file in the working directory."""
    if args.verbose:
        print(f" - Calling function: write_file(file_path='{file_path}', ...)")
    return write_file(working_directory="./calculator", file_path=file_path, content=content)


def main():
    # Utilizing SDK chats component to manage the conversation history natively.
    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(
            tools=[get_file_content_tool, get_files_info_tool, run_python_file_tool, write_file_tool],
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    tool_map = {
        "get_file_content": get_file_content_tool,
        "get_files_info": get_files_info_tool,
        "run_python_file": run_python_file_tool,
        "write_file": write_file_tool,
    }

    message_to_send = args.user_prompt

    for _ in range(20):
        response = chat.send_message(message_to_send)

        if response.usage_metadata:
            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        else:
            if args.verbose:
                print("Warning: No usage metadata returned")

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_name = function_call.name
                func_args = dict(function_call.args) if function_call.args else {}
                
                if function_name in tool_map:
                    try:
                        res = tool_map[function_name](**func_args)
                        func_response = {"result": res}
                    except Exception as e:
                        func_response = {"error": str(e)}
                else:
                    func_response = {"error": f"Unknown function: {function_name}"}
                
                function_responses.append(types.Part(
                    function_response=types.FunctionResponse(
                        name=function_name,
                        id=function_call.id,
                        response=func_response
                    )
                ))
            message_to_send = function_responses
        else:
            print(f"\n{response.text}")
            break
    else:
        print("Error: Maximum number of iterations reached without a final response.")
        sys.exit(1)

if __name__ == "__main__":
    main()
