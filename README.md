# AI Agent

**⚠️ Disclaimer: For Learning Purposes Only ⚠️**

This application is designed and built purely for educational and learning purposes. It is **not** intended for "real world" production use.

## Overview

This project is a basic Python-based AI agent that leverages the Gemini SDK to assist users with file operations and script execution. It serves as an exploration into giving an LLM the tools necessary to interact directly with a local filesystem and Python interpreter.

## Security Warning

**Running this application carries significant inherent security risks.** 

The AI agent has the ability to read files, write files, and execute arbitrary Python scripts directly on your host machine. While there are basic application-level guardrails in place (such as a working directory constraint), these do not provide secure isolation. A malicious or hallucinating agent could potentially impact the functioning of the host operating system.

For a detailed breakdown of the vulnerabilities and current guardrails, please read the full [Security Audit](docs/security_audit.md).

## Architecture

To understand how the application is structured, how the Gemini SDK integrates with the local tool wrappers, and how the core logic is separated from the tool implementations, please see the [Architecture Overview](docs/architecture.md).

## Future Next Steps

To move this project from an educational experiment towards a more robust tool, the following next steps are planned:

- **System Isolation (Docker):** Implement a Docker container to securely sandbox the execution of Python scripts, completely mitigating the risk of arbitrary code execution impacting the host machine.
- **Enhanced Guardrails:** Enforce stricter bounds on file I/O operations and potentially restrict standard library imports in the agent's execution environment.
- **Human-in-the-Loop:** Add a confirmation prompt that requires explicit user approval before the agent is allowed to execute any script or permanently modify any files.
- **Advanced Context Management:** Improve the agent's ability to maintain context over longer coding sessions and multi-file projects.

## Credits

The original idea and foundational inspiration for this project come from the [boot.dev](https://boot.dev/) course **"Building an AI Agent"**.
