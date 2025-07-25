# exercises_xp_gold.py

#Exercise 1 and 2

birthdays = {
    "Alice": "1990/05/22",
    "Bob": "1985/09/12",
    "Charlie": "2000/01/30",
    "Dana": "1993/03/17",
    "Eli": "1988/11/05"
}

print("🎉 Welcome to the Birthday Dictionary!")
print("You can look up the birthdays of the people in the list :\n")

for person in birthdays:
    print("-", person)

name = input("Enter a name to look up: ")

if name in birthdays:
    print(f"{name}'s birthday is on {birthdays[name]}")
else:
    print("Sorry, this name is not in the birthday dictionary.")


#Exercise 3

new_name = input("\nAdd a new birthday – Enter the name: ")
new_birthday = input(f"Enter {new_name}'s birthday (YYYY/MM/DD): ")
birthdays[new_name] = new_birthday

print("\nUpdated birthday list:")
for person in birthdays:
    print("-", person)

final_lookup = input("\nWhose birthday do you want to look up? ")

if final_lookup in birthdays:
    print(f"{final_lookup}'s birthday is on {birthdays[final_lookup]}")
else:
    print(f"Sorry, we don’t have the birthday information for {final_lookup}.")


#Exercise 4

print("\n🛒 Welcome to the Fruit Shop!")

simple_items = {
    "banana": 4,
    "apple": 2,
    "orange": 1.5,
    "pear": 3
}

print("\nFruit prices:")
for fruit, price in simple_items.items():
    print(f"The price of one {fruit} is ${price}")

stock_items = {
    "banana": {"price": 4, "stock": 10},
    "apple": {"price": 2, "stock": 5},
    "orange": {"price": 1.5, "stock": 24},
    "pear": {"price": 3, "stock": 1}
}

total_cost = 0

print("\nInventory value per fruit:")
for fruit, data in stock_items.items():
    cost = data["price"] * data["stock"]
    print(f"{fruit.capitalize()}: {data['stock']} in stock at ${data['price']} — Total: ${cost}")
    total_cost += cost

print(f"\n💰 Total cost to buy everything in stock: ${total_cost}")
