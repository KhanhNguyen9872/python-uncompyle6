# EXTREME: generator + comprehension + lambda inside try/except match emulation
# Combines generators, list/dict/set comprehensions with obfuscation patterns

try:
    __patch_match_subject_1 = '123' == '456'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _x = [[True], [False]]
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _e2:
        # List comprehension with lambda filter
        result1 = [(lambda x: x * 2)(i) for i in range(10) if (lambda x: x % 2 == 0)(i)]
        print(result1)

        # Dict comprehension with ternary
        result2 = {(lambda k: k)(i): (lambda v: "even" if v % 2 == 0 else "odd")(i) for i in range(5)}
        print(result2)

        # Set comprehension
        result3 = {(lambda x: x ** 2)(i) for i in range(-3, 4)}
        print(sorted(result3))

        # Nested list comprehension
        result4 = [[(lambda x, y: x + y)(i, j) for j in range(3)] for i in range(3)]
        print(result4)

        # Generator with lambda inside join
        result5 = ''.join((chr((lambda x: x + 65)(i)) for i in range(5)))
        print(result5)

        # Chained generators
        def gen1():
            for i in range(5):
                yield (lambda x: x * 3)(i)

        def gen2(g):
            for val in g:
                if (lambda x: x > 5)(val):
                    yield val

        print(list(gen2(gen1())))
