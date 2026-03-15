# Tests map and filter builtins
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)
