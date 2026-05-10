from functions.get_file_content import get_file_content

result = get_file_content("calculator", "main.py")
print(f"Result for main.py: \n{result}")

result = get_file_content("calculator", "pkg/calculator.py")
print(f"Result for 'pkg/calculator.py': \n{result}")

result = get_file_content("calculator", "/bin/cat")
print(f"Result for '/bin/cat': \n{result}")

result = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"Result for 'pkg/does_not_exist.py': \n{result}")

result = get_file_content("calculator", "lorem.txt")
truncated_result = result[9800:]
print(f"Result for 'lorem.txt': \n{truncated_result}")
