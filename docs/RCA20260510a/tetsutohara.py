from google import genai
from google.genai import types


def get_current_directory_files() -> list[str]:
    print("\n[Tool Executed] get_current_directory_files called")
    return ["main.py", "README.md", "requirements.txt"]


client = genai.Client(api_key="YOUR_API_KEY")


def test_gemini_31_function_calling():
    print("--- Gemini 3.1 Function Calling Test Start ---")

    try:
        chat = client.chats.create(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                tools=[get_current_directory_files],
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=False
                ),
            ),
        )

        print("Sending prompt...")
        response = chat.send_message(
            "What kind of files are there in the current directory?"
        )

        print("\n[Success] Response from model:")
        print(response.text)

        print("Sending prompt...")
        response = chat.send_message(
            "What are the purposes of the files in the current directory?"
        )
        print("\n[Success] Response from model:")
        print(response.text)

    except Exception as e:
        print("\n[REPRODUCED ERROR] 400 error detected:")
        print(e)


if __name__ == "__main__":
    test_gemini_31_function_calling()
