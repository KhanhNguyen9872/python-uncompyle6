# Test decorator (use simple call-based decorator pattern)
def my_decorator(func):
    def wrapper(name):
        print("before")
        result = func(name)
        print("after")
        return result
    return wrapper

def say_hello(name):
    return "Hello, " + name

decorated = my_decorator(say_hello)
print(decorated("World"))
