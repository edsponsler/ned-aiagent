from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

types.Part.model_config['extra'] = 'allow'
types.Part.model_rebuild(force=True)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    from functions.call_function import available_functions
    
    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(tools=[available_functions])
    )
    
    response = chat.send_message("Explain how the calculator renders the result to the console.")
    
    if response.function_calls:
        print("Model extra of candidate:", response.candidates[0].content.parts[0].model_extra)

if __name__ == "__main__":
    main()
