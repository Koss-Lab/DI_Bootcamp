#ExercisesXP.py

#Exercise 1

keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

result_dict = dict(zip(keys, values))
print(result_dict)

#Exercise 2

family = {"rick": 43, 'beth': 13, 'morty': 5, 'summer': 8}

total_cost = 0

for member, age in family.items():
    if age < 3:
        ticket_price = 0
    elif 3 <= age <= 12:
        ticket_price = 10
    else:
        ticket_price = 15

    print(f"{member.title()} ticket price: ${ticket_price}")
    total_cost += ticket_price
print(f"Total cost: ${total_cost}")

#Exercise 3

brand = {'name': 'Zara',
'creation_date': 1975,
    'creator_name': 'Amancio Ortega Gaona',
    'type_of_clothes': ['men', 'women', 'children', 'home'],
    'international_competitors': ['Gap', 'H&M', 'Benetton'],
    'number_stores': 7000,
    'major_color': {
        'France': 'blue',
        'Spain': 'red',
        'US': 'pink, green'
    }
}
brand['number_stores'] = 2
print(f"Zara’s clients are interested in clothes for: {', '.join(brand['type_of_clothes'])}.")
brand['country_creation'] = 'Spain'

if 'international_competitors' in brand:
    brand['international_competitors'].append('Desigual')
del brand['creation_date']

print(f"Last competitor: {brand['international_competitors'][-1]}")
print(f"Major colors in the US: {brand['major_color']['US']}")
print(f"Number of keys: {len(brand)}")
print(f"Keys: {list(brand.keys())}")

more_on_zara = {'creation_date': 1975, 'number_stores': 7000}
brand.update(more_on_zara)
print(f"Updated brand dictionary: {brand}")

#Exercise 4

users = ["Mickey", "Minnie", "Donald", "Ariel", "Pluto"]

index_to_characters = {user: index for index, user in enumerate(users)}
print(index_to_characters)

character_to_index = {index: user for index, user in enumerate(users)}
print(character_to_index)

sorted_characters = {user: index for index, user in enumerate(sorted(users))}
print(sorted_characters)
