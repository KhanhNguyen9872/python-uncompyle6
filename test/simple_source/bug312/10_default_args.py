# Test default args in 3.12
def greet(name, greeting="Hello"):
    return greeting + ", " + name

print(greet("World"))
print(greet("World", "Hi"))
