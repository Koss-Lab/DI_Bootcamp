#Loops.py

#Exercise 1

user_number = int(input("Enter a number: "))

for i in range(1, 11):
    print(f"{user_number} x {i} = {user_number * i}")

#Exercise 2

number = 1

while number <= 10:
    print(number)
    number += 1