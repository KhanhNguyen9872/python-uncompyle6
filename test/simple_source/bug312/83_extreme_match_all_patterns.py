# EXTREME: comprehensive pattern classification using if/elif/else
# Tests complex conditional logic with type checks

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

def classify_int(n):
    if n == 0:
        return "zero"
    elif n > 100:
        return "big_int_" + str(n)
    elif n < 0:
        return "neg_int_" + str(n)
    elif n == 1 or n == 2 or n == 3:
        return "small_int"
    return "other_int"

def classify_list(lst):
    n = len(lst)
    if n == 0:
        return "empty_list"
    elif n == 1:
        return "single_" + str(lst[0])
    elif n == 2:
        return "pair_" + str(lst[0]) + "_" + str(lst[1])
    else:
        return "head_" + str(lst[0]) + "_rest_" + str(n - 1)

def classify_dict(d):
    action = d.get("action")
    if action == "move" and "x" in d and "y" in d:
        return "move_" + str(d["x"]) + "_" + str(d["y"])
    elif action == "stop":
        count = len(d) - 1
        return "stop_extra_" + str(count)
    elif "data" in d:
        data = d["data"]
        if len(data) > 0:
            return "data_first_" + str(data[0])
    return "unknown_dict"

def classify_point(p):
    if p.x == 0 and p.y == 0:
        return "origin"
    elif p.x == p.y:
        return "diagonal_" + str(p.x)
    else:
        return "point_" + str(p.x) + "_" + str(p.y)

def classify(obj):
    # Use type(obj) is X checks (not isinstance or is None)
    if type(obj) is type(None):
        return "none"
    elif obj is True:
        return "true_literal"
    elif type(obj) is str:
        if obj == "hello":
            return "greeting"
        return "unknown"
    elif type(obj) is int:
        return classify_int(obj)
    elif type(obj) is list:
        return classify_list(obj)
    elif type(obj) is dict:
        return classify_dict(obj)
    elif type(obj) is Circle:
        c = obj.center
        r = obj.radius
        if r > 0:
            return "circle_at_" + str(c.x) + "_" + str(c.y) + "_r_" + str(r)
        return "circle_invalid"
    elif type(obj) is Point:
        return classify_point(obj)
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

# Nested try/except
try:
    _vals = [1, 2, 3]
    _sum = 0
    for _v in _vals:
        _sum += _v
    if _sum > 0:
        raise MemoryError([_sum])
    else:
        raise MemoryError([0])
except MemoryError as e:
    print("sum=" + str(e.args[0][0]))
