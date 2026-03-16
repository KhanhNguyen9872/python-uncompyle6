# Test: deeply nested try/except with raise MemoryError pattern
# From enjuly-A.pyc: 3-level nested try/except MemoryError blocks
try:
    x = '312' == '15'
    if x is True:
        raise MemoryError([True])
    elif x is False:
        _a = [[True], [False]]
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        y = 'ab' == 'cd'
        if y is True:
            raise MemoryError([True])
        elif y is False:
            _b = [[True], [False]]
        raise MemoryError([True])
    except MemoryError as _e2:
        try:
            z = 'ef' == 'gh'
            if z is True:
                raise MemoryError([True])
            elif z is False:
                _c = [[True], [False]]
            raise MemoryError([True])
        except MemoryError as _e3:
            print("deep nested")
