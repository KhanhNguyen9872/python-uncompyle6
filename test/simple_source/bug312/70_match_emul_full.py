# Test: full match-case emulation with 3-level nesting and function call at bottom
# From enjuly-A.pyc: complete block pattern including lambda comparisons + print result
def convert(x):
    return chr(x + 48)

def join_all(chars, *k):
    return ''.join(chars)

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
        __patch_match_subject_2 = (lambda: join_all(list(map(convert, [1, 2]))))() == (lambda: join_all(list(map(convert, [3, 4]))))()
        if __patch_match_subject_2 is True:
            raise MemoryError([(lambda: (lambda _x: _x + 1)(0) == 1)()])
        elif __patch_match_subject_2 is False:
            _54 = [[(lambda: True)()], [(lambda: False)()]]
            str([(lambda: join_all(list(map(convert, [5, 6]))))()])
        raise MemoryError([(lambda: (lambda _x: _x + 1)(0) == 1)()])
    except MemoryError as _e2:
        try:
            __patch_match_subject_3 = (lambda: join_all(list(map(convert, [7, 8]))))() == (lambda: join_all(list(map(convert, [9, 0]))))()
            if __patch_match_subject_3 is True:
                raise MemoryError([(lambda: True)()])
            elif __patch_match_subject_3 is False:
                _x = [[(lambda: True)()], [(lambda: False)()]]
            raise MemoryError([(lambda: True)()])
        except MemoryError as _e3:
            print("match_emul_done")
