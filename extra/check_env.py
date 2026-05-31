import subprocess
result = subprocess.run(
    ["venv\\Scripts\\python.exe", "-c", "import textual; print(textual.__version__)"],
    cwd="C:\\Users\\xkr\\Desktop\\lockbox",
    capture_output=True, text=True
)
print("textual version:", result.stdout.strip(), result.stderr.strip())

result2 = subprocess.run(
    ["venv\\Scripts\\python.exe", "-c", "import lockbox; print('lockbox ok')"],
    cwd="C:\\Users\\xkr\\Desktop\\lockbox",
    capture_output=True, text=True
)
print("lockbox import:", result2.stdout.strip(), result2.stderr.strip())
