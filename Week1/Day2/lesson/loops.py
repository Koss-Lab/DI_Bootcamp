fruits = ['apple', 'banana', 'kiwi', 'pear']

for fruit in fruits:
  print(fruit)

#sequences that we can loop throught
# strings

for char in 'Harry':
  print(char)

#list: example above

#tuples and sets

languages = ('PT', 'ES', 'IT')
for lang in languages:
  print(lang)

#range()

for i in range(0,11,2):
  print('hello', i)

# for i in 10:
#   print(i)

for i, fruit in enumerate(fruits):
  if fruit == 'apple':
    fruits[i] = 'Windows is better'
  else:
    print(f'Fruit {i} is {fruit}')

print(fruits)