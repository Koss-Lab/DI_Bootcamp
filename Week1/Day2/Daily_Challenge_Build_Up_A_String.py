#Daily_Challenge_Build_Up_A_String.py

import random

#Exercise 1

string = input("Enter EXACTLY 10 characters: ")

#Exercise 2

if len(string) < 10:
    print('String not long enough.')
elif len(string) > 10:
    print('String too long.')
elif len(string) == 10:
    print('Perfect string.')

#Exercise 3

    print("First character:", string[0])
    print("Last character:", string[-1])

#Exercise 4

print("\nBuilding string:")
for i in range(1, len(string) + 1):
    print(string[:i])

#Exercise 5

chars = list(string)
random.shuffle(chars)
shuffled_string = ''.join(chars)
print("\n🔀 Shuffled string:", shuffled_string)