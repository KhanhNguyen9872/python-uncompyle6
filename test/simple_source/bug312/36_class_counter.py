# Tests class with class attribute
class Counter:
    count = 0

    def __init__(self):
        self.value = 1

    def get_value(self):
        return self.value

c1 = Counter()
print(c1.get_value())
print(Counter.count)
