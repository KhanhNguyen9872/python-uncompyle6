# Test with statement
import tempfile
import os

# Simple with open
path = tempfile.mktemp()
with open(path, "w") as f:
    f.write("hello")

# Read back
with open(path, "r") as f:
    data = f.read()
    print(data)

os.remove(path)
