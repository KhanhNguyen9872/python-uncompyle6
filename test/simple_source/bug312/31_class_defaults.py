# Tests class with default params in __init__
class Config:
    def __init__(self, name="default", value=0):
        self.name = name
        self.value = value

    def display(self):
        return self.name + ": " + str(self.value)

c = Config()
print(c.display())
c2 = Config("custom", 42)
print(c2.display())
