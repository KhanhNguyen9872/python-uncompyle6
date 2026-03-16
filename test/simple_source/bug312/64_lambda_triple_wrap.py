# Test: triple-wrapped lambda with list(map(...)) pattern
# From enjuly-A.pyc: (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [...]))))())())()
def decode_char(x):
    return chr(x - 100)

def join_chars(chars, *k):
    return ''.join(chars)

result = (lambda: (lambda: (lambda: join_chars(list(map(decode_char, [172, 169, 176]))))())())()
print(result)
