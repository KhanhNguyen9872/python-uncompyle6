# Test for-each patterns
# for with list
items = [1, 2, 3, 4, 5]
total = 0
for item in items:
    total = total + item
print(total)

# for with enumerate
for i, val in enumerate(items):
    print(i, val)

# for with dict
d = {"a": 1, "b": 2}
for key in d:
    print(key)

# for-else
for x in range(10):
    if x == 5:
        break
else:
    print("no break")
