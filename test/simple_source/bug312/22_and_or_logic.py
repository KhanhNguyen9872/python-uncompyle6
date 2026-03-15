# Test and/or in if
def check(a, b, c):
    if a and b:
        return 1
    if a or c:
        return 2
    return 3

print(check(True, True, False))
print(check(True, False, True))
print(check(False, False, False))
