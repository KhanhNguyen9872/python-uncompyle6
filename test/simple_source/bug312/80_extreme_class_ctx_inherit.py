# EXTREME: async-like patterns, multiple inheritance, metaclass, context managers
# Everything inside nested try/except for maximum complexity

try:
    __patch_match_subject_1 = '0' == '1'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _z = [[True], [False]]
    raise MemoryError([True])
except MemoryError as _e:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError:

        # Context manager class
        class ManagedResource:
            def __init__(self, name):
                self.name = name
                self.entered = False

            def __enter__(self):
                self.entered = True
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.entered = False
                return False

        # Multiple inheritance with super()
        class Base1:
            def method(self):
                return "base1"

        class Base2:
            def method(self):
                return "base2"

        class Child(Base1, Base2):
            def method(self):
                return super().method() + "_child"

        # Class with __slots__ and __eq__
        class Point:
            __slots__ = ('x', 'y')

            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __eq__(self, other):
                return self.x == other.x and self.y == other.y

            def __hash__(self):
                return hash((self.x, self.y))

            def __add__(self, other):
                return Point(self.x + other.x, self.y + other.y)

            def __repr__(self):
                return f"P({self.x},{self.y})"

        # Use everything
        with ManagedResource("test") as res:
            print(res.entered)  # True
            c = Child()
            print(c.method())  # base1_child
            p1 = Point(1, 2)
            p2 = Point(3, 4)
            p3 = p1 + p2
            print(p3)  # P(4,6)
            print(p1 == Point(1, 2))  # True

        # Nested with + try inside
        with ManagedResource("outer") as r1:
            with ManagedResource("inner") as r2:
                try:
                    raise ValueError("test")
                except ValueError as ve:
                    print(str(ve))
                finally:
                    print(r1.name, r2.name)
