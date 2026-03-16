# EXTREME: walrus operator + match/case + lambda + for/else + while/else
# Combines multiple Python 3.10+ features with obfuscation patterns

# Walrus in while loop
values = [5, 3, 8, 0, 2, 7]
idx = 0
total = 0
while (val := values[idx]) != 0:
    total += val
    idx += 1
print(total)  # 16

# Walrus in list comprehension
result = [y for x in range(10) if (y := (lambda v: v * v)(x)) > 20]
print(result)  # [25, 36, 49, 64, 81]

# match/case with complex patterns
data = {"type": "point", "x": 10, "y": 20}
match data:
    case {"type": "point", "x": int(x), "y": int(y)} if x > 0:
        result_match = (lambda a, b: a + b)(x, y)
    case {"type": "line"}:
        result_match = -1
    case _:
        result_match = 0
print(result_match)  # 30

# for/else with lambda
for i in range(5):
    if (lambda x: x > 10)(i):
        print("found")
        break
else:
    print("not_found")

# while/else
counter = 3
while counter > 0:
    counter -= 1
    if (lambda x: x < -5)(counter):
        break
else:
    print("while_complete")

# Nested match inside try/except
try:
    val = (lambda: 42)()
    match val:
        case 42:
            raise MemoryError([(lambda: True)()])
        case _:
            raise MemoryError([(lambda: False)()])
except MemoryError as e:
    print(e.args[0][0])
