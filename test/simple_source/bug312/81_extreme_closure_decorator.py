# EXTREME: recursive closures + nonlocal + decorator chains
# Maximum closure/function complexity

# Simple decorator (fixed args, not *args/**kwargs)  
def trace(func):
    def wrapper(x):
        result = func(x)
        return result
    return wrapper

# Decorator with arguments (fixed args)
def repeat(n):
    def decorator(func):
        def wrapper(x):
            results = []
            for _ in range(n):
                results.append(func(x))
            return results
        return wrapper
    return decorator

# Triple-decorated function
@trace
@repeat(3)
@trace
def compute(x):
    return x ** 2

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

# Simple recursive function
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(10))  # 3628800

# Closure with list accumulation
def make_accumulator():
    items = []
    def add(x):
        items.append(x)
        return len(items)
    def get_all():
        return list(items)
    return add, get_all

add, get_all = make_accumulator()
print(add(1), add(2), add(3))
print(get_all())
