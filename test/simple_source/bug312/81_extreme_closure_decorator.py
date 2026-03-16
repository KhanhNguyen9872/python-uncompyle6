# EXTREME: recursive closures + nonlocal + decorator chains + functools
# Maximum closure/function complexity

import functools

# Decorator that wraps with lambda
def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

# Decorator with arguments
def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(n):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

# Triple-decorated function
@trace
@repeat(3)
@trace
def compute(x):
    return (lambda: (lambda _a: _a ** 2)(x))()

print(compute(5))  # [25, 25, 25]

# Recursive closure with nonlocal
def make_counter(start=0):
    count = start
    def increment(n=1):
        nonlocal count
        count += n
        return count
    def decrement(n=1):
        nonlocal count
        count -= n
        return count
    def get():
        return count
    return increment, decrement, get

inc, dec, get = make_counter(10)
print(inc())    # 11
print(inc(5))   # 16
print(dec(3))   # 13
print(get())    # 13

# Closure returning closure returning closure
def level1(a):
    def level2(b):
        def level3(c):
            def level4(d):
                return a + b + c + d
            return level4
        return level3
    return level2

print(level1(1)(2)(3)(4))  # 10

# Lambda closure chain
fn = (lambda a: (lambda b: (lambda c: (lambda d: a * b + c * d))))(2)(3)(4)(5)
print(fn)  # 26

# Recursive function with memoization via closure
def make_fib():
    cache = {}
    def fib(n):
        if n in cache:
            return cache[n]
        if n <= 1:
            result = n
        else:
            result = fib(n - 1) + fib(n - 2)
        cache[n] = result
        return result
    return fib

fib = make_fib()
print([fib(i) for i in range(10)])
