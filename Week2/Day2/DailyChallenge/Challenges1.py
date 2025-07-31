#Challenges1.py

#Exercise 1

def insert_item(lst, index, item):
    lst.insert(index, item)
    print(lst)

insert_item([1, 2, 3, 4], 2, 'new_item')


#Exercise 2

def count_spaces(s):
    count = s.count(' ')
    print(f"Number of spaces: {count}")

count_spaces("This is a test string.")

#Exercise 3

def count_case(s):
    upper = sum(1 for c in s if c.isupper())
    lower = sum(1 for c in s if c.islower())
    print(f"Uppercase: {upper}, Lowercase: {lower}")

count_case("Hello World!")

#Exercise 4

def my_sum(arr):
    total = 0
    for num in arr:
        total += num
    print(f"Sum: {total}")

my_sum([1, 5, 4, 2])

#Exercise 5

def find_max(arr):
    max_num = arr[0]
    for num in arr:
        if num > max_num:
            max_num = num
    print(f"Max number: {max_num}")

find_max([0, 1, 3, 50])


#Exercise 6

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    print(f"Factorial: {result}")

factorial(4)

#Exercise 7

def list_count(lst, element):
    count = 0
    for item in lst:
        if item == element:
            count += 1
    print(f"Count of '{element}': {count}")

list_count(['a', 'a', 't', 'o'], 'a')

#Exercise 8

import math

def norm(lst):
    sum_squares = sum(x ** 2 for x in lst)
    result = math.sqrt(sum_squares)
    print(f"L2-norm: {result}")

norm([1, 2, 2])

#Exercise 9

def is_mono(arr):
    if all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)) or all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1)):
        print("True")
    else:
        print("False")

is_mono([7, 6, 5, 5, 2, 0])
is_mono([2, 3, 3, 3])
is_mono([1, 2, 0, 4])

#Exercise 10

def longest_word(lst):
    longest = max(lst, key=len)
    print(f"Longest word: {longest}")

longest_word(["apple", "banana", "kiwi", "grapefruit"])

#Exercise 11

def separate_lists(lst):
    integers = [item for item in lst if isinstance(item, int)]
    strings = [item for item in lst if isinstance(item, str)]
    print(f"Integers: {integers}, Strings: {strings}")

separate_lists([1, "apple", 2, "banana", 3, "cherry"])

#Exercise 12

def is_palindrome(s):
    if s == s[::-1]:
        print("True")
    else:
        print("False")

is_palindrome('radar')
is_palindrome('john')

#Exercise 13

def sum_over_k(sentence, k):
    words = sentence.split()
    count = sum(1 for word in words if len(word) > k)
    print(f"Words with length > {k}: {count}")

# Example
sentence = 'Do or do not there is no try'
k = 2
sum_over_k(sentence, k)



#Exercise 14

def dict_avg(d):
    average = sum(d.values()) / len(d)
    print(f"Average: {average}")

dict_avg({'a': 1, 'b': 2, 'c': 8, 'd': 1})

#Exercise 15

def common_div(n1, n2):
    divisors = [i for i in range(1, min(n1, n2) + 1) if n1 % i == 0 and n2 % i == 0]
    print(f"Common divisors: {divisors}")

common_div(10, 20)

#Exercise 16

def is_prime(n):
    if n <= 1:
        print("False")
        return
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            print("False")
            return
    print("True")

is_prime(11)
is_prime(15)

#Exercise 17

def weird_print(lst):
    result = [lst[i] for i in range(len(lst)) if i % 2 == 0 and lst[i] % 2 == 0]
    print(result)

weird_print([1, 2, 2, 3, 4, 5])

#Exercise 18

def type_count(**kwargs):
    type_counts = {}
    for value in kwargs.values():
        t = type(value)
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, count in type_counts.items():
        print(f"{t.__name__}: {count}")

type_count(a=1, b="string", c=1.0, d=True, e=False)

#Exercise 19

def my_split(s, delimiter=' '):
    result = []
    word = ''
    for char in s:
        if char == delimiter:
            if word:
                result.append(word)
                word = ''
        else:
            word += char
    if word:
        result.append(word)
    print(result)

my_split("Hello world, how are you?", ',')
my_split("Hello world how are you?")

#Exercise 20

def to_password(s):
    return '*' * len(s)

input_string = input("Enter a string to convert to password format: ")
print("Password format:", to_password(input_string))

