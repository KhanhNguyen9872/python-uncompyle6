# Tests global variable access from nested scope
counter = 0

def increment():
    global counter
    counter += 1

def get_count():
    return counter

increment()
increment()
increment()
print(get_count())
