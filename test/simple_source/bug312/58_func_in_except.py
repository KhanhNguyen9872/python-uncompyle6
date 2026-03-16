# Test: function definition inside except block
# From enjuly-A.pyc: def functiondz(x) defined inside except MemoryError
try:
    raise MemoryError([True])
except MemoryError as _e:
    def handler(x):
        try:
            eval("1/0")
        except ZeroDivisionError:
            return "handled"
        else:
            pass

    print(handler(1))
