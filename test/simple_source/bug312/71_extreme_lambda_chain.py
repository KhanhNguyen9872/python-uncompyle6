# EXTREME: deeply nested lambda chains with closures, default args, and immediate invocation
# Combines: nested lambdas, closure capture, ternary, comparison chains

f1 = (lambda: (lambda _a: (lambda _b: (lambda _c: _a + _b + _c)(3))(2))(1))()
print(f1)  # 6

f2 = (lambda: (lambda x=10: (lambda y=20: (lambda z=30: x + y + z)())())())()
print(f2)  # 60

f3 = (lambda: (lambda: (lambda: (lambda: (lambda: (lambda: 99)())())())())())()
print(f3)  # 99

# Lambda returning lambda returning lambda
gen = (lambda: (lambda: (lambda x: (lambda y: x + y))))()()
print(gen(3)(4))  # 7

# Nested lambda with ternary and comparison
f4 = (lambda: (lambda _x: _x + 1 if _x > 0 else _x - 1)(
    (lambda: (lambda _y: _y * 2)(
        (lambda: 5)()
    ))()
))()
print(f4)  # 11

# Lambda chain with boolean result used in ternary
f5 = (lambda: "yes" if (lambda: (lambda _z: _z + (lambda: 1)())(0) == 1)() else "no")()
print(f5)  # yes
