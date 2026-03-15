# Test global and nonlocal
count = 0

def increment():
    global count
    count += 1

increment()
increment()
print(count)

def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
        return x
    return inner()

print(outer())
