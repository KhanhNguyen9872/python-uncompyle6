# Tests nested ternary
def sign(x):
    return "positive" if x > 0 else ("negative" if x < 0 else "zero")

print(sign(5))
print(sign(-3))
print(sign(0))
