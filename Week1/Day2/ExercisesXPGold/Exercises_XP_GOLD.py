#Exercises_XP_GOLD.py

#Exercise 1

list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list2 = [7, 8, 9, 10, 11, 12, 13, 14, 15]

list1.extend(list2)
print(list1)

#Exercise 2

for number in range(1500, 2501):
    if number % 5 == 0 and number % 7 == 0:
        print(number)

#Exercise 3

names = ['Samus', 'Cortana', 'V', 'Link', 'Mario', 'Cortana', 'Samus']
user_name = input('Enter your name: ')

if user_name in names:
    print(f"{user_name} found at index: {names.index(user_name)}")
else:
    print(f"{user_name} not found in the list.")

#Exercise 4

number1 = int(input('Enter a first number: '))
number2 = int(input('Enter a second number: '))
number3 = int(input('Enter a third number: '))

print("The greatest number is:", max(number1, number2, number3))

#Exercise 5

import string
vowels = 'aeiou'
for letter in string.ascii_lowercase:
    if letter in vowels:
        print(f"{letter} is a vowel")
    else:
        print(f"{letter} is a consonant")

#Exercise 6

words = []
for i in range(7):
    word = input(f"Enter word {i + 1}: ")
    words.append(word)
letter = input("Enter a single character: ")
for word in words:
    if letter in word:
        print(f"'{letter}' found at index {word.index(letter)} in word '{word}'")
    else:
        print(f"'{letter}' not found in word '{word}'")

#Exercise 7

numbers = list(range(1, 1000001))
print("Min:", min(numbers))
print("Max:", max(numbers))
print("Sum:", sum(numbers))

#Exercise 8

input_str = input("Enter comma-separated numbers: ")
numbers_list = input_str.split(",")
numbers_tuple = tuple(numbers_list)
print("List:", numbers_list)
print("Tuple:", numbers_tuple)

#Exercise 9

print("\nExercise 9:")
import random
wins = 0
losses = 0
while True:
    guess = input("Guess a number from 1 to 9 (or type 'q' to quit): ")
    if guess.lower() == 'q':
        break
    if not guess.isdigit() or not (1 <= int(guess) <= 9):
        print("Invalid input. Try again.")
        continue
    guess = int(guess)
    rand_num = random.randint(1, 9)
    if guess == rand_num:
        print("Winner!")
        wins += 1
    else:
        print(f"Better luck next time. (The number was {rand_num})")
        losses += 1

print(f"\nGames Won: {wins} | Games Lost: {losses}")