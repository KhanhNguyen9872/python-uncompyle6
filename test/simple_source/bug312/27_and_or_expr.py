# Tests simple boolean expression
def check(a, b):
    if a and b:
        return True
    return False

print(check(True, True))
print(check(True, False))
