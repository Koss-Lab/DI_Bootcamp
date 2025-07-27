#Functions.py

# functions are used to automate some code, if we have a function doing a certain thing,
# we can call it anytime to execute its code without to rewrite everything

# print()
# len()

#syntax

def func_name():
    '''prints out the function name'''
    print('I am a function')


#call
func_name()

#Exercise

def hello():
    '''prints out the hello message'''
    print('Hello there!')

hello()

# Passing ARGUMENTS to the function

def greetings(language = 'EN', name = 'Ariel')-> str:
    '''prints out the greeting to name, depending on the language'''
    if language == 'PT':
        print(f'Ola {name}, tudo bem ?')
    elif language == 'ES':
        print(f'Holab{name}, que tal ?')
    elif language == 'EN':
        print(f'Hi {name}, how are you ?')
    else:
        print('unknown langage')

#greetings('PT')
#greetings('ES')
#greetings('JP')

#Key word arguments

greetings('PT', 'Ariel')
greetings(name = 'Ariel', language = 'PT')
greetings()

#returning a value from a function

def calculation (num1, num2)-> int:
    '''sum of two numbers'''
    result = num1 + num2
    return result
print(calculation(3, 4))

def multiply(calc)-> int:

    result = calc * 3
    return result
calc = calculation(3, 4)
print(multiply(3))


#Exercise 2
def info(country, capital):
    print(f'The capital of {country} is {capital}')

def country_info(country='Naboo') -> str:
    if country == 'Israel':
        capital = 'Jerusalem'
        info(country, capital)
    elif country == 'Naboo':
        capital = 'Theed'
        info(country, capital)
    elif country == 'China':
        capital = 'Beijing'
        info(country, capital)
    elif country == 'Belgium':
        capital = 'Brussels'
        info(country, capital)
    else:
        print('Unknown country')

country_info('Belgium')

#Exercise 3

age = 26

def current_age():
    print(age)
    my_age = 27
    my_age += 1

current_age()

#Exercise 4

students = ['Harry', 'Ron', 'Hermione', 'Luna']

#create a function called welcome() that says 'Name, welcome to Hogwards !' for each one of the given list

def welcome(*args):
    if args:
        for name in args:
            print(f'{name}, Welcome to Hogwards !')
    else:
        print("you didn't pass names")

welcome()

def get_house(students_list):
    for i, name in enumerate(students_list):
        students_list[i] = f'{name} - Hogwarts'
        print(students_list[i])
get_house(students)


#Args and kwargs
# args = list, sets, tuples,

welcome('Camila', 'Niv', 'Michal', 'David', 'Flavia')
def user_info(**kwargs):
    print(kwargs)
    for value in kwargs.values():
        print(value)

user_info(name='Michael', age=27, email='<EMAIL>', is_online=True)

numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(numbers[0][2])
