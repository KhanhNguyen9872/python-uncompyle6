# Hard: key-value class
class Store:
    def __init__(self):
        self.data = {}

    def put(self, key, value):
        self.data[key] = value

    def fetch(self, key):
        return self.data.get(key)

s = Store()
s.put("x", 10)
s.put("y", 20)
print(s.fetch("x"))
print(s.fetch("z"))
