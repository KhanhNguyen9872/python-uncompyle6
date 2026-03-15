# Tests class with property-like methods
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return (self.x * self.x + self.y * self.y) ** 0.5

    def __repr__(self):
        return "Point(%d, %d)" % (self.x, self.y)

p = Point(3, 4)
print(p.distance())
