#DailyChallenge.py

import math
import matplotlib.pyplot as plt


class Circle:
    def __init__(self, radius=None, diameter=None):
        if radius is not None:
            self.radius = radius
        elif diameter is not None:
            self.radius = diameter / 2
        else:
            raise ValueError("You must provide either a radius or a diameter")

    @property
    def diameter(self):
        return self.radius * 2

    @property
    def area(self):
        return math.pi * self.radius ** 2

    def __str__(self):
        return f"Circle with radius: {self.radius:.2f}, diameter: {self.diameter:.2f}, area: {self.area:.2f}"

    def __add__(self, other):
        if isinstance(other, Circle):
            return Circle(radius=self.radius + other.radius)
        raise TypeError("You can only add another Circle")

    def __eq__(self, other):
        return isinstance(other, Circle) and self.radius == other.radius

    def __lt__(self, other):
        return isinstance(other, Circle) and self.radius < other.radius

    def __le__(self, other):
        return isinstance(other, Circle) and self.radius <= other.radius

    def __gt__(self, other):
        return isinstance(other, Circle) and self.radius > other.radius

    def __ge__(self, other):
        return isinstance(other, Circle) and self.radius >= other.radius

    def __repr__(self):
        return f"Circle({self.radius:.2f})"

c1 = Circle(radius=5)
c2 = Circle(diameter=10)
c3 = Circle(radius=3)

print(c1)
print(c2 == c1)
print(c3 < c1)
print(c1 + c3)
print(sorted([c1, c2, c3]))

def draw_circles_with_matplotlib(circles):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    x_offset = 0
    for circle in circles:
        draw = plt.Circle((x_offset + circle.radius, circle.radius), circle.radius, fill=False)
        ax.add_patch(draw)
        x_offset += circle.diameter + 10

    ax.set_xlim(0, x_offset)
    ax.set_ylim(0, max(c.radius for c in circles) * 2 + 10)
    plt.title("Sorted Circles")
    plt.show()

draw_circles_with_matplotlib(sorted([c1, c2, c3]))