# Test: lambda expression as argument to raise
# From enjuly-A.pyc: raise MemoryError([(lambda: expr)()])
try:
    raise MemoryError([(lambda: (lambda _x: _x + 1)(0) == 1)()])
except MemoryError as e:
    print(e.args)

try:
    raise MemoryError([(lambda: (lambda _y: _y - 1)(0) == 1)()])
except MemoryError as e:
    print(e.args)
