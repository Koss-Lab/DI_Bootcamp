# DATA STRUCTURES: SEQUENCES

# TUPLES
my_id = (1347)

my_tuple = ()
print(type(my_tuple))

nums = [1,2,34,5,67]
nums_tuple = tuple(nums)
print(nums_tuple)

#tuple methods
cities = ('NY', 'BO', 'SP', 'RJ', 'NY')

print(cities.count('NY'))

#we can use index
print(cities[1])
print(cities.index('SP'))

# cities[1] = "RJ" #not possible!!!

#Unpacking
languages = ('EN','RU','JA','HE')

lang1, lang2, lang3, lang4 = languages
print(lang1)
print(lang2)
print(lang3)
print(lang4)

# SETS

some_set = set()
other_set = {1,2,6}

#set methods
countries = {"Israel", "US", "Brazil"}
names = {"Shimon", "Israel", "David"}

set_3 = countries.intersection(names)
print(set_3)

merged_set = countries.union(names)
print(merged_set)

dif_set = names.difference(countries)
print(dif_set)