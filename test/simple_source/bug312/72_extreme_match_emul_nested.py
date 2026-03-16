# EXTREME: 5-level nested match emulation with lambda subjects, function defs, and imports
# Combines all enjuly-A patterns: __patch_match_subject, MemoryError, lambdas, def in except, import

def converter(x):
    return chr(x + 48)

try:
    __patch_match_subject_1 = '312' == '15'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _21 = [[True], [False]]
        str(['_118'])
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        __patch_match_subject_2 = (lambda: (lambda: ''.join(list(map(converter, [1, 2]))))())() == (lambda: (lambda: ''.join(list(map(converter, [3, 4]))))())()
        if __patch_match_subject_2 is True:
            raise MemoryError([(lambda: (lambda _x: _x + (lambda: 1)())(0) == 1)()])
        elif __patch_match_subject_2 is False:
            _54 = [[(lambda: (lambda _a: _a + 1)(0) == 1)()], [(lambda: (lambda _b: _b - 1)(0) == 1)()]]
            str([(lambda: ''.join(list(map(converter, [5, 6]))))()])
        raise MemoryError([(lambda: (lambda _x: _x + 1)(0) == 1)()])
    except MemoryError as _e2:
        try:
            __patch_match_subject_3 = (lambda: ''.join(list(map(converter, [7, 8]))))() == (lambda: ''.join(list(map(converter, [0, 9]))))()
            if __patch_match_subject_3 is True:
                raise MemoryError([(lambda: True)()])
            elif __patch_match_subject_3 is False:
                _x = [[(lambda: True)()], [(lambda: False)()]]
            raise MemoryError([(lambda: True)()])
        except MemoryError as _e3:
            try:
                __patch_match_subject_4 = (lambda: (lambda: (lambda: ''.join(list(map(converter, [1, 0, 5]))))())())() == (lambda: (lambda: (lambda: ''.join(list(map(converter, [2, 0, 5]))))())())()
                if __patch_match_subject_4 is True:
                    raise MemoryError([(lambda: (lambda _c: _c + (lambda: 1)())(0) == 1)()])
                elif __patch_match_subject_4 is False:
                    _y = [[(lambda: True)()], [(lambda: False)()]]
                    str([(lambda: (lambda: (lambda: ''.join(list(map(converter, [3, 0, 5]))))())())()])
                raise MemoryError([(lambda: (lambda _d: _d + 1)(0) == 1)()])
            except MemoryError as _e4:
                try:
                    __patch_match_subject_5 = (lambda: (lambda: (lambda: ''.join(list(map(converter, [4, 0]))))())())() == (lambda: (lambda: (lambda: ''.join(list(map(converter, [5, 0]))))())())()
                    if __patch_match_subject_5 is True:
                        raise MemoryError([(lambda: True)()])
                    elif __patch_match_subject_5 is False:
                        _z = [[(lambda: True)()], [(lambda: False)()]]
                    raise MemoryError([(lambda: True)()])
                except MemoryError as _e5:
                    def deep_handler(val):
                        try:
                            eval("1/0")
                        except ZeroDivisionError:
                            return "handled_" + str(val)
                        else:
                            pass
                        finally:
                            str(42)

                    import time
                    print(deep_handler(5))
