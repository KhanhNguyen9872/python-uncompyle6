# Tests nested function with variable scope
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    def get():
        return count
    return increment, get

inc, get = make_counter()
inc()
inc()
inc()
print(get())
