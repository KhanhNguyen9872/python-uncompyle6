# Test: match-case emulated via try/except/raise MemoryError pattern
# From enjuly-A.pyc: __patch_match_subject_N = expr; if True: raise; elif False: ...; raise
try:
    __patch_match_subject_1 = '312' == '15'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _21 = [[True], [False]]
        str(['_118'])
    raise MemoryError([True])
except MemoryError as _e:
    print("caught")
