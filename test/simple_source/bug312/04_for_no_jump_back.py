# Test function with for and return in 3.12
def find_first(items):
    for item in items:
        return item
    return None

print(find_first([1, 2, 3]))
print(find_first([]))
