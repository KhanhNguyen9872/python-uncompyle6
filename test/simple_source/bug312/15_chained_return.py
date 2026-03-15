# Test range check (no chained compare)
def is_valid(x):
    if x >= 0 and x <= 10:
        return True
    return False

print(is_valid(5))
print(is_valid(-1))
