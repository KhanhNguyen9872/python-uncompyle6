# Adapted from bug30/03_pop_top.py
# Tests while + inline if/else
def bisect_left(a, x, lo=0, hi=10):
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo

print(bisect_left([1, 3, 5, 7, 9], 4))
print(bisect_left([1, 3, 5, 7, 9], 1))
