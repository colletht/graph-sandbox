from math import sqrt

#Represents a point in 2 dimensional space
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y
        )

    def scalar(self, other):
        return Point(
            self.x*other,
            self.y*other
        )

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    def getUnitVector(self):
        return Point(
            self.x/self.magnitude(),
            self.y/self.magnitude()
        )