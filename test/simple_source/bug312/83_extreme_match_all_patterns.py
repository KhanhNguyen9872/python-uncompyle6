# EXTREME: comprehensive match/case with all pattern types
# Pushes decompiler to handle every match pattern variant

class Point:
    __match_args__ = ("x", "y")
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    __match_args__ = ("center", "radius")
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

def classify(obj):
    match obj:
        # Literal patterns
        case 0:
            return "zero"
        case True:
            return "true_literal"
        case "hello":
            return "greeting"
        case None:
            return "none"
        # OR pattern
        case 1 | 2 | 3:
            return "small_int"
        # Capture pattern with guard
        case int(n) if n > 100:
            return f"big_int_{n}"
        case int(n) if n < 0:
            return f"neg_int_{n}"
        # Sequence patterns
        case []:
            return "empty_list"
        case [x]:
            return f"single_{x}"
        case [x, y]:
            return f"pair_{x}_{y}"
        case [x, *rest]:
            return f"head_{x}_rest_{len(rest)}"
        # Mapping patterns
        case {"action": "move", "x": x, "y": y}:
            return f"move_{x}_{y}"
        case {"action": "stop", **rest}:
            return f"stop_extra_{len(rest)}"
        # Class patterns
        case Point(x=0, y=0):
            return "origin"
        case Point(x, y) if x == y:
            return f"diagonal_{x}"
        case Point(x, y):
            return f"point_{x}_{y}"
        case Circle(Point(x, y), r) if r > 0:
            return f"circle_at_{x}_{y}_r_{r}"
        # Nested match
        case {"data": [first, *_]}:
            return f"data_first_{first}"
        # Wildcard
        case _:
            return "unknown"

tests = [
    0, "hello", None, 2, 150, -5,
    [], [42], [1, 2], [1, 2, 3, 4],
    {"action": "move", "x": 10, "y": 20},
    {"action": "stop", "reason": "done"},
    Point(0, 0), Point(5, 5), Point(3, 7),
    Circle(Point(1, 2), 10),
    {"data": [99, 100, 101]},
    "other"
]

for t in tests:
    print(classify(t))

# Nested match inside try/except
try:
    match (lambda: [1, 2, 3])():
        case [a, b, c] if (lambda x: x > 0)(a):
            raise MemoryError([(lambda: a + b + c)()])
        case _:
            raise MemoryError([0])
except MemoryError as e:
    print(f"sum={e.args[0][0]}")
