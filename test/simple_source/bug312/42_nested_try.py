# Hard: try/except at module level
try:
    x = int("42")
    print(x)
except:
    print("error")

try:
    y = int("bad")
except:
    y = -1
print(y)
