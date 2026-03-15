# Hard: class inheritance with method override
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

animals = [Dog("Rex"), Cat("Whiskers"), Animal("Bird")]
for a in animals:
    print(a.speak())
