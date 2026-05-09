import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Arguments to pass to the python file",
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_dir = (
        os.path.commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
    )

    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python3", absolute_file_path]

    if args:
        command.extend(args)

    try:
        output_string = ""
        completed_process = subprocess.run(
            command, cwd=working_dir_abs, timeout=30, text=True, capture_output=True
        )

        if completed_process.returncode != 0:
            output_string += (
                f"Process exited with code {completed_process.returncode}\n"
            )

        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced.\n"

        if completed_process.stdout:
            output_string += f"STDOUT: {completed_process.stdout}\n"

        if completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}\n"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"
