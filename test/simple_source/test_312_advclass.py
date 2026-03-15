# Test advanced class features

# Inheritance
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return self.name + " makes a sound"

class Dog(Animal):
    def speak(self):
        return self.name + " barks"

class Cat(Animal):
    def speak(self):
        return self.name + " meows"

# Class with class method and static method
class Counter:
    count = 0

    def __init__(self):
        Counter.count = Counter.count + 1

    @classmethod
    def get_count(cls):
        return cls.count

    @staticmethod
    def description():
        return "A simple counter"

# Usage
dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())
print(cat.speak())

c1 = Counter()
c2 = Counter()
print(Counter.get_count())
print(Counter.description())
