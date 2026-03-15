# Test closure / nested function in 3.12
def outer(x):
    def inner(y):
        return x + y
    return inner

add5 = outer(5)
print(add5(3))
