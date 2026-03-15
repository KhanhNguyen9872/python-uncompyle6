# Test advanced function features

# Default arguments
def greet(name, greeting="Hello"):
    return greeting + ", " + name

print(greet("World"))
print(greet("World", "Hi"))

# *args and **kwargs
def varargs(*args, **kwargs):
    print(args)
    print(kwargs)

varargs(1, 2, 3, a=4, b=5)

# Nested function / closure
def outer(x):
    def inner(y):
        return x + y
    return inner

add5 = outer(5)
print(add5(3))

# Decorator
def decorator(func):
    def wrapper(*args):
        print("before")
        result = func(*args)
        print("after")
        return result
    return wrapper

@decorator
def say_hello(name):
    print("hello " + name)

say_hello("world")
