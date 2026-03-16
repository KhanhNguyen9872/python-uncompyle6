# EXTREME: the ultimate stress test - combines EVERYTHING from enjuly-A.pyc
# globals aliasing + ternary chains + match emulation + nested lambdas + bytearray decode
# + for loop over globals + function def in except + try/else/finally + chr/join
# + import in except + always-true if-guards + class in except + comprehensions

# Phase 1: globals aliasing with complex ternary (enjuly-A lines 1-13)
globals()['mol'] = bool if bool(bool(bool(bool))) < bool(type(int(110) > int(121) < int(156) > int(1418))) and bool(str(str(102) > int(912) < int(128) > int(1914))) > 2 else bool
globals()['co2'] = str if bool(bool(bool(str))) < bool(type(int(142) > int(94) < int(1119) > int(917))) and bool(str(str(72) > int(97) < int(175) > int(112))) > 2 else str
globals()['h2so4'] = int if False else int
globals()['feso4'] = bytes if False else bytes
globals()['agno4'] = list if False else list
globals()['h3o'] = map if False else map
globals()['h2o3'] = eval if False else eval
globals()['h2'] = callable if False else callable

# Phase 2: decoder functions (enjuly-A h2o, c2h6, o2)
def h2o(july, *k):
    if k:
        enjuly19 = '+'
    else:
        enjuly19 = ''
    globals()['_173'] = (lambda: (lambda _210: _210 + (lambda: h2so4(30584 - 30583))())(0) == 1)()
    globals()['july'] = july
    for globals()['enjuly19_'] in globals()['july']:
        if not _173:
            globals()['enjuly19_'] += (lambda: '')()
        enjuly19 += co2(enjuly19_)
    return enjuly19

def c2h6(e):
    br = bytearray(e[len(b'enjuly19/'):])
    r = 0
    for b in br:
        r = r * 256 + b
    return r

def o2(h2so3):
    h2so3 = h2so3 - 16742655
    if h2so3 <= 127:
        return co2(feso4([h2so3]), 'utf8')
    elif h2so3 <= 2047:
        if 1 < 2:
            b1 = 192 | h2so3 >> 6
        b2 = 128 | h2so3 & 63
        return co2(feso4([b1, b2]), 'utf8')
    elif h2so3 <= 65535:
        b1 = 224 | h2so3 >> 12
        if 2 > 1:
            b2 = 128 | h2so3 >> 6 & 63
        b3 = 128 | h2so3 & 63
        return co2(feso4([b1, b2, b3]), 'utf8')
    else:
        b1 = 240 | h2so3 >> 18
        if 2 == 2:
            b2 = 128 | h2so3 >> 12 & 63
        if 1 < 2 < 3:
            b3 = 128 | h2so3 >> 6 & 63
        b4 = 128 | h2so3 & 63
        return co2(feso4([b1, b2, b3, b4]), 'utf8')

# Phase 3: match emulation block 1 (enjuly-A pattern)
try:
    __patch_match_subject_1 = '312' == '15'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _21 = [[True], [False]]
        co2(['_118'])
    raise MemoryError([True])
except MemoryError as _1714:
    try:
        __patch_match_subject_2 = (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [16742704, 16742705]))))())())() == (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [16742708, 16742704, 16742712]))))())())()
        if __patch_match_subject_2 is True:
            raise MemoryError([(lambda: (lambda _184: _184 + (lambda: h2so4(30584 - 30583))())(0) == 1)()])
        elif __patch_match_subject_2 is False:
            _54 = [[(lambda: (lambda _1510: _1510 + (lambda: h2so4(1))())(0) == 1)()], [(lambda: (lambda _1417: _1417 - (lambda: h2so4(1))())(0) == 1)()]]
            co2([(lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [16742750, 16742704, 16742709]))))())())()])
        raise MemoryError([(lambda: (lambda _1615: _1615 + (lambda: h2so4(1))())(0) == 1)()])
    except MemoryError as _141:
        try:
            __patch_match_subject_3 = (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [(lambda: c2h6(b'enjuly19/\xffy4'))(), (lambda: c2h6(b'enjuly19/\xffy0'))(), (lambda: c2h6(b'enjuly19/\xffy1'))()]))))())())() == (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [(lambda: c2h6(b'enjuly19/\xffy0'))(), (lambda: c2h6(b'enjuly19/\xffy/'))(), (lambda: c2h6(b'enjuly19/\xffy0'))(), (lambda: c2h6(b'enjuly19/\xffy3'))()]))))())())()
            if __patch_match_subject_3 is True:
                raise MemoryError([(lambda: True)()])
            elif __patch_match_subject_3 is False:
                _1319 = [[(lambda: True)()], [(lambda: False)()]]
            raise MemoryError([(lambda: True)()])
        except MemoryError as _176:
            print("block1")

# Phase 4: match emulation block 2 with function def
try:
    __patch_match_subject_4 = '816' == '14'
    if __patch_match_subject_4 is True:
        raise MemoryError([True])
    elif __patch_match_subject_4 is False:
        _1013 = [[True], [False]]
        co2(['_216'])
    raise MemoryError([True])
except MemoryError as _193:
    try:
        __patch_match_subject_5 = (lambda: 'test1')() == (lambda: 'test2')()
        if __patch_match_subject_5 is True:
            raise MemoryError([(lambda: True)()])
        elif __patch_match_subject_5 is False:
            _96 = [[(lambda: True)()], [(lambda: False)()]]
        raise MemoryError([(lambda: True)()])
    except MemoryError as _916:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _148:
            tiendatcute = (lambda: c2h6(b'enjuly19/{'))()

            # Function def inside except (enjuly-A functiondz)
            def functiondz(x):
                try:
                    h2o3("1+1")
                    if "abcdefgh" == "cdefghab":
                        (_126, _1115, _617, _1215) = (1, 2, 3, 4)
                    else:
                        pass
                except ZeroDivisionError:
                    try:
                        h2o3("2+2")
                    except ZeroDivisionError:
                        return "hello_from_decompiler"
                    else:
                        pass
                    finally:
                        co2(100)
                return "functiondz_ok"

# Phase 5: more blocks with import and string building
try:
    __patch_match_subject_7 = '114' == '1014'
    if __patch_match_subject_7 is True:
        raise MemoryError([True])
    elif __patch_match_subject_7 is False:
        _93 = [[True], [False]]
    raise MemoryError([True])
except MemoryError as _69:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _515:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _82:
            print(tiendatcute)

try:
    raise MemoryError([True])
except MemoryError as _169:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _219:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _79:
            import time

try:
    raise MemoryError([True])
except MemoryError as _87:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _179:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _59:
            s = ''.join((chr(x) for x in [(lambda: c2h6(b'enjuly19/H'))(), (lambda: c2h6(b'enjuly19/e'))(), (lambda: c2h6(b'enjuly19/l'))(), (lambda: c2h6(b'enjuly19/l'))(), (lambda: c2h6(b'enjuly19/o'))()]))

try:
    raise MemoryError([True])
except MemoryError as _139:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _111:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _1915:
            print(s)

try:
    raise MemoryError([True])
except MemoryError as _314:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _1519:
        try:
            raise MemoryError([(lambda: True)()])
        except MemoryError as _12:
            print(functiondz(1))

print('done')
