# Tests multiple return paths
def classify(x, y):
    if x > 0:
        if y > 0:
            return "both positive"
        return "x positive only"
    if y > 0:
        return "y positive only"
    return "neither positive"

print(classify(1, 1))
print(classify(1, -1))
print(classify(-1, 1))
print(classify(-1, -1))
