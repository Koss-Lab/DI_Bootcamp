#Loops.py

fruits = ["apple", "banana", "kiwi", 'pear']

for fruit in fruits :
    print(fruit)

for char in 'Harry':
    print(char)

languages = ('PT', 'ES', 'IT')
for lang in languages:
    print(lang)

for i in range(1, 11):
    print('Hello', i)

for i, fruit in enumerate(fruits):
    if fruit == 'apple':
        fruits[i] = 'Mac is better'

    print(f'Fruit {i} is {fruit}')

print(fruits)
