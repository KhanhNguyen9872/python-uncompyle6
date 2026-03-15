# Tests fibonacci (no swap)
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    a = 0
    b = 1
    for i in range(2, n + 1):
        c = a + b
        a = b
        b = c
    return b

for i in range(10):
    print(fibonacci(i))
