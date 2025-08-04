#OOP.py

# OOP = Object Oriented Programing

# Class = a blueprint for creating objects,
# within the Class, we can define the attributes of the objects of that class

#Attributes = the main characteristic of an object

#Inheritance: Parent and Child class

class Parent:
    def speak(self):
        print(f"Parent speaking")

class Child(Parent):
    def speak(self):
        print("Child speaking")

class Grandchild(Child):
    pass

obj1 = Child()
obj1.speak()

obj2 = Grandchild()
obj2.speak()

class Animal:
    def __init__(self, name, family, legs):
        self.name = name
        self.family = family
        self.legs = legs

    def sleep(self):
        return f"{self.name} is sleeping - from Animal"


class Dog(Animal):
    def __init__(self, name, family, legs, trained, age):
        super().__init__(name, family, legs)
        self.trained = trained
        self.age = age

    def bark(self):
        return f"{self.name} is barking"


class Cat(Animal):
    def __init__(self, name, family, legs, friendly, age, nickname):
        super().__init__(name, family, legs)
        self.friendly = friendly
        self.age = age
        self.nickname = nickname

    def get_crazy(self):
        if self.friendly:
            return f"{self.name} doesn't get crazy"
        else:
            return f"{self.name} is running at full power"


class Alien:
    def __init__(self, name, planet):
        self.name = name
        self.planet = planet

    def bark(self):
        return f"{self.name} goes Ulululu"


class AlienDog(Alien, Dog):
    def __init__(self, name, family, legs, trained, age, planet):
        Alien.__init__(self, name, planet)
        Dog.__init__(self, name, family, legs, trained, age)


class AlienCat(Alien, Cat):
    def __init__(self, name, family, legs, friendly, age, nickname, planet):
        Alien.__init__(self, name, planet)
        Cat.__init__(self, name, family, legs, friendly, age, nickname)

    def fly_away(self):
        return f"{self.get_crazy()} as an alien cat"

dog1 = Dog("Rex", "Canine", 4, True, 5)
print(dog1.bark())

alien_dog1 = AlienDog("Buba", "Canine", 6, True, 135, "Jupiter")
print(alien_dog1.bark())
print(Dog.bark(alien_dog1))

alien_cat1 = AlienCat("Bob", "Feline", 8, False, 999, "Bobby", "Catopia")
print(alien_cat1.fly_away())
