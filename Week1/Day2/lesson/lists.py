# List: sequence of ordered elements that can be changed (mutable)

user_name = 'juliana'
email = 'juliana@gmail.com'
user_age = 35
is_online = True

user_info = [user_name, email,user_age,is_online]
print(len(user_info))

some_list = list('item 1') #create a list with the function
other_list = ['item 1', 'item 2']

print(some_list)
print(other_list)

empty_list = []

#ordered means can be accessed by index
print(user_info[2])

# fruits = ['orange', 'kiwi', 'aple', 'lime']
# #slice 
# print(fruits[-2:])

# fruits[1] = 'pineaple'
# print(fruits)

# my_name = 'Juliana'
# my_name[3] = 'e' #typeError: not possible to change an item on a string: strings are imutable

#list methods
fruits = ['orange', 'kiwi', 'aple', 'lime']
fruits.insert(1, 'mango')
print(fruits)

fruits.remove('kiwi') #removes the first apperance 
print(fruits)

fruits.append('wattermelon')
print(fruits)

fruits.pop(1) #with no argument it deletes the last element
print(fruits)

vegs = ['tomate', 'potato', 'carrot']
colors = ['red', 'blue', 'green']

fruits.extend(vegs)
print(fruits)


#sorted() and .sort()
fruits_sorted = sorted(fruits)
print(fruits)
print(fruits_sorted)

fruits.sort()
print(fruits)

#exercise 1

list1 = [5, 10, 15, 20, 25, 50, 20]

if 20 in list1:
    index_20 = list1.index(20)
    list1[index_20] = 200
print(list1)
