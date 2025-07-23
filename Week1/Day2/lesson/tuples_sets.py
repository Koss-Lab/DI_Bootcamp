#tuples_sets.py

#tuples
my_id = (1347)
my_tuple = ()
print(type(my_tuple))

nums = [1, 2, 3, 4, 5]
num_tuple = tuple(nums)
print(num_tuple)

cities = ['NY', 'BO', 'SP', 'RJ', 'NY']
print(cities.count('NY'))

#sets
print(cities[1])
print(cities.index('SP'))
cities[1] = 'RJ'

#Unpacking
languages = ('EN', 'RU', 'JA', 'HE')
lang1, lang2, lang3, lang4 = languages
print(lang1)
print(lang2)
print(lang3)
print(lang4)


#Sets

some_set = set()
other_set = [1, 2, 6]

countries = {'Israel', 'US', 'Brazil'}
names = {'Shimon', 'Israel', 'David'}

set3 = countries.intersection(names)
print(set3)
merged_set = countries.union(names)
print(merged_set)

dif_set = countries.difference(names)
print(dif_set)