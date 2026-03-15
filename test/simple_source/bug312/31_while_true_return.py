# Tests while True with single return
def find_divisor(n):
    d = 2
    while d * d <= n:
        if n % d == 0:
            return d
        d += 1
    return n

print(find_divisor(15))
print(find_divisor(7))
