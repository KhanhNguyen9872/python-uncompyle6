# Tests for 3.12 classes
class Dog:

    def __init__(self, name):
        self.name = name

    def bark(self):
        return self.name + " says woof!"


d = Dog("Rex")
print(d.bark())
