import os

from google import genai
from google.genai import types


# Define simple mock tools
def get_files_info(directory: str = ".") -> str:
    """Lists files in a specified directory.

    Args:
        directory: Directory path to list files from.
    """
    print(f" -> Executing tool: get_files_info(directory='{directory}')")
    return "file1.txt, main.py"


def get_file_content(file_path: str) -> str:
    """Returns the content of a file.

    Args:
        file_path: Path to the file to read.
    """
    print(f" -> Executing tool: get_file_content(file_path='{file_path}')")
    return "print('Hello world')"


def main():
    from dotenv import load_dotenv

    # Requires GEMINI_API_KEY environment variable. Loading from ../../.env
    load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

    SYSTEM_PROMPT = """
    You are a helpful AI coding agent.
    Your goal is to assist the user by performing file operations.
    CRITICAL RULE: You must always list the files in the directory first before reading the content of any specific file. Do not call tools in parallel.
    """

    print("Initializing chat session with gemini-3.1-flash-lite and AFC enabled...")
    chat = client.chats.create(
        # gemini 3.1 crashs with 400 error; gemini 2.5 does not
        # model="gemini-2.5-flash",
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(
            tools=[get_files_info, get_file_content],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=False, maximum_remote_calls=20
            ),
            system_instruction=SYSTEM_PROMPT,
            temperature=0.0,
        ),
    )

    prompt = "Please look at the files in the current directory, and then tell me what is inside the python file."
    print(f"\nUser Prompt: '{prompt}'\n")

    try:
        response = chat.send_message(prompt)
        print("\n--- SUCCESS ---")
        print("Final Response:")
        print(response.text)
    except Exception:
        print("\n--- CRASH DETECTED ---")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
