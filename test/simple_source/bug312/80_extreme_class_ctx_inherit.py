# EXTREME: context managers, multiple inheritance inside exception handler
# Tests class definitions in except blocks, context managers, super()

try:
    raise MemoryError([True])
except MemoryError:

    # Context manager class
    class ManagedResource:
        def __init__(self, name):
            self.name = name

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            return False

    # Multiple inheritance with super()
    class Base1:
        def method(self):
            return "base1"

    class Child(Base1):
        def method(self):
            return super().method() + "_child"

    # Class with operator overloading
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __add__(self, other):
            return Point(self.x + other.x, self.y + other.y)

    # Use context manager
    with ManagedResource("test") as res:
        print(res.name)

    # Use inheritance
    c = Child()
    print(c.method())

    # Use operator overloading
    p1 = Point(1, 2)
    p2 = Point(3, 4)
    p3 = p1 + p2
