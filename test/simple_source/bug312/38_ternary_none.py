# Tests conditional assignment with None check
def safe_divide(a, b):
    result = a / b if b != 0 else None
    return result

print(safe_divide(10, 2))
print(safe_divide(10, 0))
