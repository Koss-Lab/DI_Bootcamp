#ExercisesXP.py

#Exercise 1

class Pets():
    def __init__(self, animals):
        self.animals = animals

    def walk(self):
        for animal in self.animals:
            print(animal.walk())


class Cat():
    is_lazy = True

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def walk(self):
        return f'{self.name} is just walking around'


class Bengal(Cat):
    def sing(self, sounds):
        return f'{sounds}'


class Chartreux(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 1: Siamese class
class Siamese(Cat):
    def sing(self, sounds):
        return f'{sounds}'


# Step 2: Create cat instances
bengal_cat = Bengal("Milo", 3)
chartreux_cat = Chartreux("Luna", 5)
siamese_cat = Siamese("Simba", 2)

all_cats = [bengal_cat, chartreux_cat, siamese_cat]

# Step 3: Create a Pets instance
sara_pets = Pets(all_cats)

# Step 4: Walk the cats
sara_pets.walk()

#Exercise 2

class Dog:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        return f"{self.name} is barking"

    def run_speed(self):
        return self.weight / self.age * 10

    def fight(self, other_dog):
        self_power = self.run_speed() * self.weight
        other_power = other_dog.run_speed() * other_dog.weight
        if self_power > other_power:
            return f"{self.name} won the fight!"
        elif self_power < other_power:
            return f"{other_dog.name} won the fight!"
        else:
            return "It's a draw!"


# Step 2: Dog instances
dog1 = Dog("Rex", 5, 20)
dog2 = Dog("Max", 3, 18)
dog3 = Dog("Buddy", 4, 25)

# Step 3: Test methods
print(dog1.bark())
print(dog2.run_speed())
print(dog1.fight(dog2))
print(dog2.fight(dog3))


#Exercise 3

import random

class PetDog(Dog):
    def __init__(self, name, age, weight):
        super().__init__(name, age, weight)
        self.trained = False

    def train(self):
        print(self.bark())
        self.trained = True

    def play(self, *args):
        dog_names = [self.name] + list(args)
        names_str = ", ".join(dog_names)
        print(f"{names_str} all play together")

    def do_a_trick(self):
        if self.trained:
            tricks = [
                "does a barrel roll",
                "stands on his back legs",
                "shakes your hand",
                "plays dead"
            ]
            print(f"{self.name} {random.choice(tricks)}")

my_dog = PetDog("Fido", 2, 10)
my_dog.train()
my_dog.play("Buddy", "Max")
my_dog.do_a_trick()

#Exercise 4

class Person:
    def __init__(self, first_name, age):
        self.first_name = first_name
        self.age = age
        self.last_name = ""

    def is_18(self):
        return self.age >= 18


class Family:
    def __init__(self, last_name):
        self.last_name = last_name
        self.members = []

    def born(self, first_name, age):
        new_member = Person(first_name, age)
        new_member.last_name = self.last_name
        self.members.append(new_member)

    def check_majority(self, first_name):
        for member in self.members:
            if member.first_name == first_name:
                if member.is_18():
                    print("You are over 18, your parents Jane and John accept that you will go out with your friends")
                else:
                    print("Sorry, you are not allowed to go out with your friends.")
                return
        print("Person not found.")

    def family_presentation(self):
        print(f"Family Name: {self.last_name}")
        for member in self.members:
            print(f"{member.first_name} - Age: {member.age}")

my_family = Family("Kossmann")
my_family.born("Ariel", 25)
my_family.born("Nathan", 15)

my_family.check_majority("Ariel")
my_family.check_majority("Nathan")
my_family.family_presentation()
