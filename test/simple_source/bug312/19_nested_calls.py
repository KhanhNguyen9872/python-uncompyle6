# Test nested function calls
def double(x):
    return x * 2

def add_one(x):
    return x + 1

result = double(add_one(double(3)))
print(result)
