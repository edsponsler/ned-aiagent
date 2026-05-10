# Bug Report: `google-genai` Python SDK Strips `thought_signature` in Gemini 3.1 Function Calling

**To:** Google Gemini 3.1 Product Engineering & SDK Maintainers  
**Issue:** `400 INVALID_ARGUMENT` during multi-turn function calling with Gemini 3.1 models due to missing `thought_signature`.  
**Impact:** Critical blocking issue for Gemini 3.1 agent workflows. Forces developers to downgrade to Gemini 2.5.  

## Overview
When utilizing `gemini-3.1-flash` or `gemini-3.1-flash-lite` with the `google-genai` Python SDK, multi-turn function calling (both manual and via `AutomaticFunctionCallingConfig`) fails. The API rejects the subsequent tool response request with the following error:
`400 INVALID_ARGUMENT: Function call is missing a thought_signature in functionCall parts. This is required for tools to work correctly...`

## Root Cause Analysis: Core Serialization Layer
The Gemini 3.1 model family introduces an opaque `thought_signature` payload inside `functionCall` parts to preserve the model's internal reasoning state across tool execution boundaries. 

However, the `google-genai` Python SDK parses incoming API responses into strict Pydantic models. Because the Pydantic schema defining the `Part` or `FunctionCall` objects does not explicitly recognize the `thoughtSignature` field (and drops undefined extra fields), the SDK silently strips the signature during deserialization.

When the SDK's internal `chats` loop (via `AutomaticFunctionCallingConfig(disable=False)`) constructs the conversation history to submit the tool execution results back to the model, the required signature is permanently lost. The API consequently rejects the payload and terminates the session.

## Impact on Developers
This serialization bug entirely breaks the "happy path" for agent workflows using Gemini 3.1. Developers attempting to leverage the advanced reasoning and multi-tool orchestration capabilities of the 3.1 models are met with immediate API crashes. 

Currently, the only viable workaround is to completely abandon Gemini 3.1 and downgrade agent architectures to `gemini-2.5-flash`, which does not strictly enforce the signature requirement. This severely limits developer adoption of the newest models.

## Steps to Reproduce
A minimal reproduction of this issue is available in the following public repository:
**Repository:** `git@github.com:edsponsler/ned-aiagent.git`

1. Clone the repository and configure your `.env` file with a valid `GEMINI_API_KEY`.
2. Inspect `main.py` and ensure the `chats.create` config is set to use:
   - `model="gemini-3.1-flash-lite"`
   - `automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)`
3. Run the agent with a prompt requiring a multi-turn tool call, for example:
   `uv run main.py "What files are in the current directory?"`
4. Observe the `ClientError: 400 INVALID_ARGUMENT` crash immediately after the tool is executed and the SDK attempts to return the result to the model.

## Request
We kindly request that the SDK engineering team prioritize a patch to explicitly accept and round-trip the `thoughtSignature` field within the Pydantic models used by the `google-genai` SDK. Resolving this data loss issue in the serialization layer will immediately unblock the developer ecosystem from adopting the powerful capabilities of the Gemini 3.1 family.
