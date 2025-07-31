#oop_intro.py

#Classes and object
#how to create a class


class Dog:

    #The consturctor

    def __init__(self, name, color, age, is_trained = False):
        self.name = name
        self.color = color
        self.age = age
        self.is_trained = is_trained

    def bark(self):
        print(f'{self.name} is barking')

    def run(self):
        if self.age <= 5:
            print(f'{self.name}  runs really fast !')
        elif self.age <= 9 and self.age >= 6:
            print(f'{self.name}  is running !')
        else:
            print(f"{self.name}  don't want to run")

    def walk(self, meters):
        print(f'{self.name} is walking {meters} meters')

    def rename(self, new_name):
        self.name = new_name
        return self


dog1 = Dog('Rex', 'Brown', 10)
print(dog1.name)
print(dog1.color)
print(dog1.age)

print(dog1.__dict__)

dog1.breed = 'Puddle'
print(dog1.breed)

#Second project of dog

dog2 = Dog('Max', 'Gold', 3)
dog2.breed = 'Golden Retriever'
print(dog2.name)
print(dog2.color)
print(dog2.age)
print(dog2.breed)

#Create a new attribute to the dog class called "its_trained" , the value is boolean and the default is False
#then run the code again, what happen ?

#Dog.is_trained = False
print(dog2.is_trained)

#Dog 3

dog3 = Dog('Fluffy', 'White', 7, True)
print(dog3.__dict__)
print(dog3.age)
print(dog3.is_trained)
print(type(dog3))

dog1.bark()

dog1.run()
dog2.run()
dog3.run()

dog1.walk(500)

dog1.rename('Gal Leshem')
print(dog1.name)
