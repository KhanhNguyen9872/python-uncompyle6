# Test: bytearray with arithmetic decoding
# From enjuly-A.pyc c2h6 function: bytearray slicing + arithmetic
def decode(e):
    br = bytearray(e[len(b'prefix/'):])
    r = 0
    for b in br:
        r = r * 256 + b
    return r

print(decode(b'prefix/\x00\x01'))  # 1
print(decode(b'prefix/\x01\x00'))  # 256
print(decode(b'prefix/A'))        # 65
