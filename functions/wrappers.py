from typing import Callable, Dict, List, Optional

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# Global configuration that can be updated by main.py
VERBOSE = False
WORKING_DIRECTORY = "./calculator"


def get_file_content_tool(file_path: str) -> str:
    """Returns the content of a file relative to the working directory.
    
    Args:
        file_path: Path to the file to read, relative to the working directory.
    """
    if VERBOSE:
        print(f"Calling function: get_file_content(file_path='{file_path}')")
    else:
        print(" - Calling function: get_file_content")
    return get_file_content(working_directory=WORKING_DIRECTORY, file_path=file_path)


def get_files_info_tool(directory: str = ".") -> str:
    """Lists files in a specified directory relative to the working directory, providing file size and directory status.
    
    Args:
        directory: Directory path to list files from, relative to the working directory (default is the working directory itself).
    """
    if VERBOSE:
        print(f"Calling function: get_files_info(directory='{directory}')")
    else:
        print(" - Calling function: get_files_info")
    return get_files_info(working_directory=WORKING_DIRECTORY, directory=directory)


def run_python_file_tool(file_path: str, args: Optional[List[str]] = None) -> str:
    """Executes a python file and returns the output.
    
    Args:
        file_path: Path to the python file to execute, relative to the working directory.
        args: Optional list of arguments to pass to the python file.
    """
    if VERBOSE:
        print(f"Calling function: run_python_file(file_path='{file_path}')")
    else:
        print(" - Calling function: run_python_file")
    return run_python_file(working_directory=WORKING_DIRECTORY, file_path=file_path, args=args)


def write_file_tool(file_path: str, content: str) -> str:
    """Writes the given content to the specified file. This function can be used to create new files or overwrite existing files within the working directory.
    
    Args:
        file_path: File path to write the content to, relative to the working directory.
        content: Content to write to the file.
    """
    if VERBOSE:
        print(f"Calling function: write_file(file_path='{file_path}', ...)")
    else:
        print(" - Calling function: write_file")
    return write_file(working_directory=WORKING_DIRECTORY, file_path=file_path, content=content)


# Export the tools list for the SDK to infer schemas from
tools_list: List[Callable] = [
    get_file_content_tool,
    get_files_info_tool,
    run_python_file_tool,
    write_file_tool,
]

# Export the tool map for manual dispatching
tool_map: Dict[str, Callable] = {
    "get_file_content": get_file_content_tool,
    "get_files_info": get_files_info_tool,
    "run_python_file": run_python_file_tool,
    "write_file": write_file_tool,
}
