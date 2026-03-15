# Test generators and iterators

# Generator function
def count_up(n):
    i = 0
    while i < n:
        yield i
        i = i + 1

for val in count_up(5):
    print(val)

# Generator expression
squares = list(x * x for x in range(5))
print(squares)

# Dict comprehension
square_map = {x: x * x for x in range(5)}
print(square_map)
