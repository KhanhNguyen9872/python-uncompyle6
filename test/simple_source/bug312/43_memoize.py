# Hard: memoize (list-based cache)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

# Call and measure
for i in range(12):
    print(fib(i))
