# EXTREME: class definition inside nested except with decorators and properties
# Tests decompiler handling of class inside exception handler

try:
    __patch_match_subject_1 = '999' == '111'
    if __patch_match_subject_1 is True:
        raise MemoryError([True])
    elif __patch_match_subject_1 is False:
        _a = [[True], [False]]
    raise MemoryError([True])
except MemoryError as _e1:
    try:
        raise MemoryError([(lambda: True)()])
    except MemoryError as _e2:

        class ObfuscatedClass:
            _counter = 0

            def __init__(self, val):
                self._val = val
                ObfuscatedClass._counter += 1

            @property
            def value(self):
                return self._val

            @staticmethod
            def decode(x):
                return (lambda: (lambda _a: _a + 1)(x))()

            @classmethod
            def get_count(cls):
                return cls._counter

            def __repr__(self):
                return f"OC({self._val})"

        obj1 = ObfuscatedClass(10)
        obj2 = ObfuscatedClass(20)
        print(obj1)
        print(obj2.value)
        print(ObfuscatedClass.decode(5))
        print(ObfuscatedClass.get_count())
