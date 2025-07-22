#Exercises_XP.py

#Exercise 1

my_fav_numbers = {1, 2, 3, 4, 7, 8, 12, 18, 16, 23, 30, 32, 42, 69, 420}
my_fav_numbers.add(9)
my_fav_numbers.add(13)
my_fav_numbers.pop()
print(my_fav_numbers)
friend_fav_numbers = (8, 7, 36, 42, 64, 128)
our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)
print(f'our fav numbers: {our_fav_numbers}')

#Exercise 2

my_tuple = (10, 20, 30)
my_tuple = my_tuple + (40, 50)
print(my_tuple)

#Exercise 3

basket = ["Banana", "Apples", "Oranges", "Blueberries"]
basket.remove("Banana")
basket.pop()
basket.append("Kiwi")
basket.insert(0, "Apples")
apples_count = basket.count("Apples")
print(f'apples count: {apples_count}')
basket.clear()
print("Final basket:", basket)

#Exercise 4

#Float = 3.14, 12.4 (decimals numbers)
#Integer = 1, 2, 3, 4 (full numbers)

float_numbers = []
for i in range(3, 11):
    float_numbers.append(i * 0.5)
print(float_numbers)

#Exercise 5

for i in range(1, 21):
    print(i)
for i in range(1, 21):
    if i % 2 == 0:
        print(i)

#Exercise 6

name =""

while name != "Ariel":
    name = input('Enter your name: ')

#Exercise 7

favorites_fruits = input('Enter one or more of your favorites fruits : ')
user_fruits = input('Enter any fruit : ')
if user_fruits.lower() in favorites_fruits.lower():
    print("You chose one of your favorite fruits! Enjoy!")
else:
    print("You chose a new fruit. I hope you enjoy it!")

#Exercise 8

toppings = []
while True:
    topping = input("Enter the toppings for you pizza (or tap 'quit' when done) : ")
    if topping == "quit":
        break
    else:
        toppings.append(topping)
        print(f"Adding {topping} to your pizza.")

total_cost = 10 + len(toppings) * 2.5
print(f"Your pizza with those toppings : {toppings} , will cost {total_cost} $.")

#Exercise 9

total_cost = 0
while True:
    age = int(input("Enter the age of a person: "))

    if age < 3:
        cost = 0
    elif 3 <= age <= 12:
        cost = 10
    else:
        cost = 15

    total_cost += cost
    more = input("Do you want to enter another person's age? (yes/no): ")
    if more.lower() != "yes":
        break

print(f"Total ticket cost: ${total_cost}")

#Bonus

allowed = []
not_allowed = []

while True:
    name = input("Enter the name of the person: ")
    age = int(input("Enter the age of the person: "))

    if age >= 18:
        allowed.append(name)
    else:
        not_allowed.append(name)

    more = input("Do you want to add another person? (yes/no): ")
    if more.lower() != "yes":
        break

print(f"People who can watch the movie: {allowed}")
print(f"People who cannot watch the movie: {not_allowed}")

#Exercise 10

sandwich_orders = ["Tuna", "Pastrami", "Avocado", "Pastrami", "Egg", "Chicken", "Pastrami"]
finished_sandwiches = []

while "Pastrami" in sandwich_orders:
    sandwich_orders.remove("Pastrami")

for sandwich in sandwich_orders:
    finished_sandwiches.append(sandwich)
    print(f"I made your {sandwich} sandwich.")

print(f"All finished sandwiches: {finished_sandwiches}")

