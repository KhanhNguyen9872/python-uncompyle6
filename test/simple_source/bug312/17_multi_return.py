# Test multiple return values
def minmax(items):
    lo = items[0]
    hi = items[0]
    for x in items:
        if x < lo:
            lo = x
        if x > hi:
            hi = x
    return lo, hi

low, high = minmax([3, 1, 4, 1, 5, 9])
print(low, high)
