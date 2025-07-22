#Exercises_XP.py

#Exercise 1

print("Hello world\nHello world\nHello world\nHello world")

#Exercise 2

calculation = (99^3)*8
print(f'the result of (99^3)*8 is {calculation}')

#Exercise 3

# 5 < 3 # False
# 3 == 3  # True
# 3 == "3" # False
# "3" > 3  # Error (cannot compare string and int)
# "Hello" == "hello" # False

#Exercise 4

computer_brand = 'Kossmagic'
print(f'I have a {computer_brand} computer.')

#Exercise 5

name = 'Ariel'
age = 26
shoe_size = 43
info = f"My name is {name}, I am {age} years old, and I wear size {shoe_size} shoes."
print(info)

#Exercise 6

a = 18
b = 42

if a > b:
    print('Hello World')
else:
    print('Not Hello World')

#Exercise 7

number = int(input('Enter a number: '))
if number % 2 == 0:
    print("Even")
else:
    print("Odd")

#Exercise 8

user_name = input('Enter your name: ')
if user_name == 'Ariel':
    print("That's my bro right here, we got the same name !")
else:
    print(f"{user_name} , This is the name i gave to my dog")

#Exercise 9

height = int(input('Enter your height in centimeters: '))
if height > 145:
    print('Congrats ! You can ride that roller coaster')
else:
    print(f'Sorry ! You are too small, grow {146-height} centimeters more, and come back to enjoy !')

