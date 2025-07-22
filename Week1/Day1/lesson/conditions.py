#conditions.py

# ==
# !=
# <=
# >=
# +=
# -=

if 5 > 3:
    print("hello world")
else :
    print("not hello world")


user_age = int(input("Enter your age: ")) #int = integer, quand on a besoin d'une integer dans l'input
if user_age < 18:
    print("sorry you can't watch the movie")
elif user_age == 21:
    print("you got a free popcorn")
else:
    print("you can watch the movie")

#Exercise 1

user_name = input("Enter your name: ")

if len(user_name) < 5:
    print('You have a short name')
else:
    print('you have a long name')

#Exercise 2

number = int(input("Enter a number between 1 and 100: "))
if number > 100 or number < 1:
    print('this number is not between 1 and 100')
else:
    if number % 3 == 0 and number % 5 == 0:
        print('FizzBuzz')
    elif number % 5 == 0:
        print('Buzz')
    elif number % 3 == 0:
        print('Fizz')
    else:
        print(f'your number({number}) is not divisible by 5 or 3')

