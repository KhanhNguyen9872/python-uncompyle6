# Test conditional with and/or
def foo(n):
    zero_stride = True if n >= 95 and n & 1 else False
    return zero_stride

print(foo(95))
print(foo(94))
