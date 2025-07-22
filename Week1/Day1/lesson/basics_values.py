#basics_values.py

#greetings = 'Hello World !'  (string)
#print(greetings.capitalize())
#print(greetings.title())
#print(greetings.upper())
#print(greetings.lower())
#print(greetings[1:5])
#print(greetings[3])
#numbers, integers(no decimal), floats(decimal), complex numbers (num + letters)


#Exercise 1

description = "strings are..."
print(description.upper())

print(description.replace("are", 'is'))
#description = "string is ..."
print(description[0:6])

#Exercise 2

my_age = 26
my_future_age = my_age + 123879
print(f'I will be {my_future_age} in 123879 years')

#Exercise 3

bank_balance = '33000'
phone_number = 532287514

if isinstance(bank_balance, str):
    bank_balance = int(bank_balance)
else:
    bank_balance = str(bank_balance)

if isinstance(phone_number, int):
    phone_number = str(phone_number)
else:
    phone_number = int(phone_number)

print(f"bank_balance: {bank_balance} ({type(bank_balance)})")
print(f"phone_number: {phone_number} ({type(phone_number)})")

#Exercise 4

first_name = "Ariel"
last_name = "Kossmann"
full_name = f"{first_name} {last_name}"
print(full_name)

#Exercise 5

x = 5
y = 10
z = 0
word1 = "hello"
word2 = "world"

if x < y and y > z:
    print("x is less than y and y is greater than z")
elif x > y and y > z:
    print("x is greater than y and y is greater than z")
else:
    print("x is less than y and y is less than z")

if word1 != word2:
    print("word1 and word2 are not equal")
else:
    print("word1 and word2 are equal")
print(bool(z))
print(bool(word1))
