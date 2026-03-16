# EXTREME: function def inside nested except + try/except/else/finally + lambda args
# Mirrors functiondz with complex control flow inside

try:
    __patch_match_subject_1 = '816' == '14'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _1013 = [[True], [False]]
        str(['_216'])
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        __patch_match_subject_2 = (lambda: (lambda: 'abcd')())() == (lambda: (lambda: 'efgh')())()
        if __patch_match_subject_2 is True:
            raise MemoryError([(lambda: (lambda _x: _x + (lambda: 1)())(0) == 1)()])
        elif __patch_match_subject_2 is False:
            _96 = [[(lambda: (lambda _a: _a + 1)(0) == 1)()], [(lambda: (lambda _b: _b - 1)(0) == 1)()]]
            str([(lambda: (lambda: 'ijklm')())()])
        raise MemoryError([(lambda: (lambda _c: _c + 1)(0) == 1)()])
    except MemoryError as _e2:
        try:
            __patch_match_subject_3 = (lambda: (lambda: 'pqr')())() == (lambda: (lambda: 'stu')())()
            if __patch_match_subject_3 is True:
                raise MemoryError([(lambda: True)()])
            elif __patch_match_subject_3 is False:
                _619 = [[(lambda: True)()], [(lambda: False)()]]
                str([(lambda: (lambda: 'vwx')())()])
            raise MemoryError([(lambda: True)()])
        except MemoryError as _e3:
            tiendatcute = (lambda: 42)()

            def functiondz(x):
                try:
                    eval((lambda: (lambda: (lambda: "1+1")())())())
                    if (lambda: (lambda: (lambda: "abcdefgh")())())() == (lambda: (lambda: (lambda: "ijklmnop")())())():
                        (_a, _b, _c, _d) = (1, 2, 3, 4)
                    else:
                        pass
                except ZeroDivisionError:
                    try:
                        eval((lambda: (lambda: (lambda: "2+2")())())())
                    except ZeroDivisionError:
                        return (lambda: (lambda: (lambda: "deep_error_result")())())()
                    else:
                        pass
                    finally:
                        str((lambda: 100)())
                return "functiondz_ok"

            print(functiondz(1))
            print(tiendatcute)
