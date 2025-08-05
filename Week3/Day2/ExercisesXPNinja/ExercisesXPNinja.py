#ExercisesXPNinja.py

import random

#Exercise 1

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        return (self.celsius * 9/5) + 32

    def to_kelvin(self):
        return self.celsius + 273.15

    def __repr__(self):
        return f"{self.celsius:.2f}°C"

class Fahrenheit(Temperature):
    def __init__(self, fahrenheit):
        self.fahrenheit = fahrenheit
        celsius = (fahrenheit - 32) * 5/9
        super().__init__(celsius)

    def __repr__(self):
        return f"{self.fahrenheit:.2f}°F"

class Kelvin(Temperature):
    def __init__(self, kelvin):
        self.kelvin = kelvin
        celsius = kelvin - 273.15
        super().__init__(celsius)

    def __repr__(self):
        return f"{self.kelvin:.2f}K"

t1 = Temperature(25)
print(t1.to_fahrenheit())
print(t1.to_kelvin())

t2 = Fahrenheit(98.6)
print(t2)
print(t2.to_kelvin())

t3 = Kelvin(0)
print(t3)
print(t3.to_fahrenheit())

#Exercise 2

class QuantumParticle:
    def __init__(self, x=None, p=None):
        self.x = x or random.randint(1, 10000)
        self.p = p or random.uniform(0, 1)
        self._spin = random.choice([0.5, -0.5])
        self.entangled_particle = None

    def __repr__(self):
        return f"<QuantumParticle x={self.x}, p={self.p:.4f}, spin={self._spin}>"

    def position(self):
        self._disturb()
        return self.x

    def momentum(self):
        self._disturb()
        return self.p

    def spin(self):
        self._disturb()
        return self._spin

    def _disturb(self):
        self.x = random.randint(1, 10000)
        self.p = random.uniform(0, 1)
        print("🌀 Quantum Interferences!!")

    def entangle(self, other):
        if not isinstance(other, QuantumParticle):
            print("❌ Can only entangle with another QuantumParticle.")
            return

        self.entangled_particle = other
        other.entangled_particle = self
        other._spin = -self._spin
        print("🔗 Spooky Action at a Distance !!")
        print(f"Particle {id(self)} is now entangled with Particle {id(other)}")


p1 = QuantumParticle(x=1, p=5.0)
p2 = QuantumParticle(x=2, p=5.0)
p1.entangle(p2)
print(p1.spin())
print(p2.spin())

