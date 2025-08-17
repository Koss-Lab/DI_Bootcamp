#decorators.py

class Circle:
    def __init__(self, radius: float, diameter: float):
        self.radius = radius
        self.diameter = diameter

    @classmethod
    def from_diameter (cls, diameter):
        diameter = diameter
        radius = diameter / 2
        return cls(radius, diameter)
    @staticmethod
    def area_from_radius (radius):
        return math.pi * (radius ** 2)

    @property
    def color(self):
        return self

    @property.setter
    def color(self, color):
        self.color = color
        return self


circle1 = Circle(5, 10)
print(circle1.radius)
print(circle1.diameter)

circle2 = Circle('', 10)
print(circle2.radius)
print(circle2.diameter)