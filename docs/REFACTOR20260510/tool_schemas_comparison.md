# Architectural Comparison: Tool Schemas in Gemini Agents

This document provides an architectural comparison of two approaches for defining Tool Schemas in your agent, considering code organization and the evolution of the Gemini models.

---

## Approach 1: Manual `types.FunctionDeclaration` (Previous Approach)

In the previous approach, each tool file (e.g., `get_file_content.py`) explicitly defined a `types.FunctionDeclaration`, which were then grouped into a single `types.Tool` array in `call_function.py`.

### Pros:
*   **Explicit Contract Control:** You have 100% fine-grained control over the exact JSON schema sent to the API. This is useful if you have extremely complex nested objects that Python type hints struggle to express.
*   **Strict Decoupling:** The Python implementation is completely divorced from the LLM-facing interface. A developer can refactor the Python code without worrying that they accidentally changed the LLM's prompt.

### Cons:
*   **High Boilerplate:** It requires writing dense, deeply-nested Pydantic/OpenAPI-style schemas.
*   **Silent Drift:** This is the biggest danger. If a developer adds a new parameter to `get_file_content(working_directory, file_path, new_flag)` but forgets to update `schema_get_file_content`, the code will silently fail at runtime because the LLM won't know the new argument exists.
*   **Clutter:** Half of your file becomes schema definitions rather than business logic.

---

## Approach 2: Automatic Inference via SDK (Current Refactored Approach)

In the refactored approach, the `google-genai` SDK dynamically inspects the Python callables (e.g., `get_file_content_tool`) directly, parsing the function signature, type hints, and docstrings to generate the schema on the fly.

### Pros:
*   **Single Source of Truth (DRY):** The code *is* the schema. By defining `def write_file_tool(file_path: str, content: str)`, you guarantee that the LLM and the Python interpreter are operating on the exact same contract. 
*   **Highly Maintainable:** Adding a new tool is as simple as writing a standard Python function with type hints and passing it to the `tools` array. There are no secondary mapping files or schema declarations to update.
*   **Cleaner Architecture:** Your core function files inside the `functions` directory can be entirely stripped of Google GenAI SDK imports, leaving pure, standard Python logic.

### Cons:
*   **Prompt/Code Coupling:** Your Python docstrings are no longer just for developers; they are literal prompts for the LLM. You have to write docstrings with prompt-engineering in mind.
*   **Type Hint Limitations:** You are restricted by what the SDK's parser understands from Python `typing` primitives.

---

## Which is the Best Practice?

**Automatic Inference is the definitive best practice for modern agent development.** 

The transition from `gemini-2.5` to `gemini-3.1` strongly reinforces this. Here is why:

1. **Alignment with SDK "Happy Paths":** Manually constructing API payloads and bypassing the SDK's high-level abstractions is extremely brittle (as evidenced by issues like the `thought_signature` parsing bug). The `google-genai` SDK is aggressively moving towards "Pythonic" interfaces. By leveraging automatic inference and `client.chats`, you ride the rails of the SDK's intended architecture, ensuring you get features like automatic `thought_signature` preservation and transparent schema validation for free.
2. **Gemini 3.1's Advanced Tool Use:** `gemini-3.1` has massively improved reasoning and tool-adherence capabilities over `2.5`. It is much better at inferring intent from natural language constraints. This means you no longer need rigid, overly-engineered JSON schemas to force the model into compliance. A simple, well-written Python docstring is more than enough for Gemini 3.1 to perfectly understand how and when to use a tool.
3. **Engineering Velocity:** For product engineers, maintaining manual schemas acts as a heavy tax on velocity. Automatic inference allows developers to write pure Python functions, wrap them, and instantly hand them to the agent, eliminating the risk of drift entirely.
