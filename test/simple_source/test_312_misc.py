# Test miscellaneous Python 3.12 constructs

# Ternary expression
x = 10
result = "big" if x > 5 else "small"
print(result)

# Multiple assignment
a, b, c = 1, 2, 3
print(a, b, c)

# Augmented assignment
total = 0
total += 10
total -= 3
total *= 2
print(total)

# String formatting
name = "World"
msg = f"Hello, {name}!"
print(msg)

# Assert
assert 1 + 1 == 2
assert len("abc") == 3, "length should be 3"

# Global/nonlocal
counter = 0
def increment():
    global counter
    counter = counter + 1

increment()
print(counter)

# Walrus operator
if (n := 10) > 5:
    print(n)

# Chained comparison
x = 5
if 1 < x < 10:
    print("in range")
