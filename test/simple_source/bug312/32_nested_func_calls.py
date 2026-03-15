# Tests nested function calls with multiple args
def add(a, b):
    return a + b

def mul(a, b):
    return a * b

result = add(mul(2, 3), mul(4, 5))
print(result)
print(add(1, add(2, add(3, 4))))
