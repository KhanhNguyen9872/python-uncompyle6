# Test: string built from chr() in a generator + join
# From enjuly-A.pyc line 292: s = ''.join(chr(x) for x in [...])
def decode(x):
    return x

s = ''.join((chr(x) for x in [decode(72), decode(101), decode(108), decode(108), decode(111)]))
print(s)
