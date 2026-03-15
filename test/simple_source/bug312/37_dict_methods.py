# Tests dictionary get and setdefault
d = {"a": 1, "b": 2}
print(d.get("a"))
print(d.get("c", 0))
d.setdefault("c", 3)
print(d)
