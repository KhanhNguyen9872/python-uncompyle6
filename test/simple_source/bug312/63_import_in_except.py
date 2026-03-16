# Test: import statement inside nested except block
# From enjuly-A.pyc line 264: import time inside deeply nested except
try:
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        raise MemoryError([True])
    except MemoryError as _e2:
        try:
            raise MemoryError([True])
        except MemoryError as _e3:
            import time
            print(type(time))
