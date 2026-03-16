# Test: nested immediately-invoked lambda expressions
# From enjuly-A.pyc: (lambda: (lambda _210: _210 + (lambda: func(x))())(0) == 1)()
def f(x):
    return int(x - 30583)

result1 = (lambda: (lambda _210: _210 + (lambda: f(30584))())(0) == 1)()
print(result1)  # True

result2 = (lambda: (lambda _210: _210 + (lambda: f(30584))())(0))()
print(result2)  # 1

result3 = (lambda: (lambda: (lambda: 42)())())()
print(result3)  # 42
