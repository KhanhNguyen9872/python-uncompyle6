# Adapted from bug37/02_if_not_or.py
# Tests "if not predicate or" inside for loop
def getmembers(names, obj, predicate):
    for key in names:
        if not predicate or obj:
            obj = 2
        obj += 1
    return obj

print(getmembers([1], 0, False))
print(getmembers([1], 1, True))
