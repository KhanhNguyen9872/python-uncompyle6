# Test: if-guarded code blocks with always-true conditions
# From enjuly-A.pyc: if 1 < 2:, if 2 > 1:, if 2 == 2:, if 1 < 2 < 3:
def encode(x):
    result = 0
    if 1 < 2:
        b1 = 192 | x >> 6
    b2 = 128 | x & 63
    if 2 > 1:
        b3 = b1 + b2
    if 2 == 2:
        b4 = b3 * 2
    if 1 < 2 < 3:
        result = b4
    return result

print(encode(200))
