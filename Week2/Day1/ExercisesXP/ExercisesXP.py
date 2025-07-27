#ExercisesXP.py

import random

#Exercise 1

def display_message():
    print( 'I am learning about functions in Python.')
display_message()

#Exercise 2

def favorite_book(title):
    print(f'One of my favorite books is {title}.')
favorite_book('Tartuffe - Molière')

#Exercise 3

def describe_city(city, country = 'Unknown'):
    print(f'{city} is in {country}')

describe_city('Brussels', 'Belgium')
describe_city('Bordeaux', 'France')
describe_city('Jerusalem', 'Israel')
describe_city('Reykjavik', 'Iceland')
describe_city('Paris')

#Exercise 4

def guess_number(your_number):
    random_number = random.randint(1, 100)
    if your_number == random_number:
        print("Success!")
    else:
        print(f"Fail! Your number: {your_number}, Random number: {random_number}")

guess_number(23)
guess_number(42)
guess_number(13)

#Exercise 5

def make_shirt(size = 'Large', text = 'I love Python !'):
    print(f"The size of the shirt is {size} and the text is {text}.")

make_shirt()
make_shirt("medium")
make_shirt("small", "Kossmagic")
make_shirt("small", "Custom message")
make_shirt(text="Hello!", size="small")
make_shirt('XL', "Ze'ev")

#Exercise 6

magician_names = ['Harry Houdini', 'David Blaine', 'Criss Angel', 'Kossmagic', 'Maxime Mandrake']
def show_magicians(magician_names):
    for magician in magician_names:
        print(magician)

def make_great(magician_names):
    for magician in magician_names:
        print(f'{magician} the Great')

make_great(magician_names)
show_magicians(magician_names)

#Exercise 7

def get_random_temp():
    return random.randint(-10, 40) #or random.uniform(-10, 40) (float numbers)

def main():
    temp = get_random_temp()
    print(f'The temperature is now {temp} degrees Celsius.')
    if temp < 0:
        print("Brrr, that's freezing! Wear some extra layers today.")
    elif 0 <= temp < 16:
        print("Quite chilly! Don’t forget your coat.")
    elif 16 <= temp < 23:
        print("Nice weather.")
    elif 23 <= temp < 32:
        print("A bit warm, stay hydrated.")
    else:
        print("It’s really hot! Stay cool.")

main()
