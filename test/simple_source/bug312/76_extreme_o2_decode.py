# EXTREME: full o2/h2o/_hex decode chain with always-true if-guards
# Exact reproduction of the Unicode decoder from enjuly-A.pyc

globals()['co2'] = str if False else str
globals()['feso4'] = bytes if False else bytes
globals()['h2so4'] = int if False else int
globals()['agno4'] = list if False else list
globals()['h3o'] = map if False else map

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

def _hex(j):
    h2so3 = ''
    for _hex in j:
        h2so3 += o2(_hex)
    return h2so3

def h2o(july, *k):
    if k:
        enjuly19 = '+'
    else:
        enjuly19 = ''
    globals()['july'] = july
    for globals()['enjuly19_'] in globals()['july']:
        enjuly19 += co2(enjuly19_)
    return enjuly19

# Decode "Hello" using the o2 function (H=72+16742655=16742727, etc.)
result = (lambda: (lambda: (lambda: h2o(agno4(h3o(o2, [16742727, 16742756, 16742763, 16742763, 16742766]))))())())()
print(result)  # Hello
