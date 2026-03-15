# Test range comparison (no chained, simplified)
def check_range(x):
    if x >= 0 and x <= 10:
        return True
    return False

print(check_range(5))
print(check_range(-1))
