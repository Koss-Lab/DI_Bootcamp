#ExercisesXP.py

from func import add_and_print
from datetime import date
from faker import Faker
import string
import random

#Exercise 1

class Currency:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount

    def __str__(self):
        return f"{self.amount} {self.currency}s"

    def __repr__(self):
        return self.__str__()

    def __int__(self):
        return self.amount

    def __add__(self, other):
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(f"Cannot add between Currency type <{self.currency}> and <{other.currency}>")
            return self.amount + other.amount
        elif isinstance(other, int):
            return self.amount + other
        else:
            raise TypeError("Unsupported type for addition")

    def __iadd__(self, other):
        if isinstance(other, Currency):
            if self.currency != other.currency:
                raise TypeError(f"Cannot add between Currency type <{self.currency}> and <{other.currency}>")
            self.amount += other.amount
        elif isinstance(other, int):
            self.amount += other
        else:
            raise TypeError("Unsupported type for addition")
        return self

c1 = Currency('dollar', 5)
c2 = Currency('dollar', 10)
c3 = Currency('shekel', 1)
c4 = Currency('shekel', 10)

str(c1)

int(c1)

repr(c1)

print(c1 + 5)

print(c1 + c2)

print(c1)

c1 += 5
print(c1)

c1 += c2
print(c1)

#print(c1 + c3)

#Exercise 2

add_and_print(10, 5)

#Exercise 3

letters = string.ascii_letters
random_string = ''.join(random.choice(letters) for _ in range(5))
print(random_string)

#Exercise 4

def show_today_date():
    today = date.today()
    print("Today's date is:", today)

show_today_date()

#Exercise 5

from datetime import datetime

def time_until_new_year():
    now = datetime.now()
    next_year = datetime(year=now.year + 1, month=1, day=1)
    diff = next_year - now
    print("Time until Jan 1st:", diff)

time_until_new_year()

#Exercises 6

def minutes_lived(birthdate_str):
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")  # format: YYYY-MM-DD
    now = datetime.now()
    diff = now - birthdate
    minutes = int(diff.total_seconds() // 60)
    print(f"You have lived for {minutes} minutes.")

minutes_lived("1998-09-23")

#Exercise 7

fake = Faker()
users = []

def generate_users(n):
    for _ in range(n):
        user = {
            "name": fake.name(),
            "address": fake.address(),
            "language_code": fake.language_code()
        }
        users.append(user)

generate_users(5)
for user in users:
    print(user)