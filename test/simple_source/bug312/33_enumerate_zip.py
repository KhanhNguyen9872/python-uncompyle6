# Tests enumerate and zip
names = ["a", "b", "c"]
for i, name in enumerate(names):
    print(i, name)

xs = [1, 2, 3]
ys = [4, 5, 6]
for x, y in zip(xs, ys):
    print(x + y)
