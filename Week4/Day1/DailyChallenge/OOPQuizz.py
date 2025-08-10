#OOPQuizz.py

#Part 1 – OOP Quiz Answers (English)
#1. What is a class?
#A class is a blueprint or template for creating objects in object-oriented programming (OOP). It defines attributes (data) and methods (behavior) that the objects created from it will have.

#2. What is an instance?
#An instance is a specific object created from a class. Each instance has its own data stored in its attributes, while sharing the same methods defined in the class.

#3. What is encapsulation?
#Encapsulation is the OOP principle of bundling data (attributes) and methods (behavior) inside a single unit (class) and controlling access to them using access modifiers (e.g., public, protected, private).

#4. What is abstraction?
#Abstraction is the process of hiding complex implementation details and showing only the essential features of an object. This allows the user to interact with the object without knowing its internal workings.

#5. What is inheritance?
#Inheritance is the mechanism that allows one class (child/subclass) to acquire the properties and methods of another class (parent/superclass). It promotes code reuse and hierarchical relationships.

#6. What is multiple inheritance?
#Multiple inheritance is when a class can inherit attributes and methods from more than one parent class. This can increase flexibility but may introduce complexity in method resolution.

#7. What is polymorphism?
#Polymorphism is the ability of different objects to respond to the same method name in different ways. It allows for a unified interface with different underlying implementations.

#8. What is method resolution order (MRO)?
#MRO is the order in which Python searches for a method in a hierarchy of classes when multiple inheritance is used. It determines the sequence of classes to be checked when executing a method. In Python, you can check the MRO with ClassName.mro()


#Exercise : Deck of Cards

import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        """Create a standard 52-card deck."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards = [Card(suit, value) for suit in suits for value in values]

    def shuffle(self):
        """Shuffle the deck randomly."""
        if len(self.cards) != 52:
            self.build()
        random.shuffle(self.cards)

    def deal(self):
        """Deal a single card from the deck."""
        if len(self.cards) == 0:
            return None
        return self.cards.pop()


# Example usage
if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    print(f"Dealt card: {deck.deal()}")
    print(f"Remaining cards in deck: {len(deck.cards)}")
