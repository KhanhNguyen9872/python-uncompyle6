# Tests nested class
class Outer:
    value = 10
    class Inner:
        value = 20
        def get(self):
            return self.value

o = Outer()
i = Outer.Inner()
print(o.value)
print(i.get())
