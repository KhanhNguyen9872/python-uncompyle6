# Test: if-guarded code blocks with always-true conditions
# From enjuly-A.pyc: if 1 < 2:, if 2 > 1:, if 2 == 2:
def encode(x):
    result = 0
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    if 1 < 2:
        b1 = 192 | x >> 6
    b2 = 128 | x & 63
    if 2 > 1:
        b3 = b1 + b2
    if 2 == 2:
        b4 = b3 * 2
    if 1 < 3:
        result = b4
    return result

print(encode(200))
