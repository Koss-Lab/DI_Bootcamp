#ExercisesXPGold.py

import datetime
import holidays
import random
import string

#Exercise 1

def upcoming_holiday(country_code='US'):
    today = datetime.date.today()
    year = today.year

    country_holidays = holidays.CountryHoliday(country_code, years=[year, year + 1])

    for date, name in sorted(country_holidays.items()):
        if date > today:
            days_left = (date - today).days
            print(f"📅 Today is {today}")
            print(f"🎉 The next holiday is {name} in {days_left} days (on {date})")
            return

upcoming_holiday('US')
upcoming_holiday('UK')
upcoming_holiday('IL')
upcoming_holiday('BE')
upcoming_holiday('FR')

#Exercise 2

def age_on_planets(seconds):
    earth_year = 31557600
    planets = {
        'Mercury': 0.2408467,
        'Venus': 0.61519726,
        'Earth': 1.0,
        'Mars': 1.8808158,
        'Jupiter': 11.862615,
        'Saturn': 29.447498,
        'Uranus': 84.016846,
        'Neptune': 164.79132
    }

    for planet, ratio in planets.items():
        age = seconds / (earth_year * ratio)
        print(f"On {planet}, you are {age:.2f} years old.")

age_on_planets(1_000_000_000)

#Exercise 3

import re

def return_numbers(s):
    digits = re.findall(r'\d', s)
    return ''.join(digits)

print(return_numbers('k5k3q2g5z6x9bn'))

#Exercise 4

import re

def validate_full_name(name):
    pattern = r'^[A-Z][a-z]+ [A-Z][a-z]+$'
    if re.match(pattern, name):
        print("✅ Valid full name.")
    else:
        print("❌ Invalid name. Make sure it's properly capitalized and has only one space.")

name = input("Enter your full name (Ex: John Doe): ")
validate_full_name(name)

#Exercise 5

def generate_password(length):
    if length < 6 or length > 30:
        raise ValueError("Password length must be between 6 and 30")

    chars = string.ascii_letters + string.digits + string.punctuation

    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in string.punctuation for c in password)):
            return password

def password_generator_cli():
    while True:
        try:
            length = int(input("Enter password length (6-30): "))
            if 6 <= length <= 30:
                break
            else:
                print("❌ Invalid range. Try again.")
        except:
            print("❌ Please enter a valid number.")

    password = generate_password(length)
    print(f"🔐 Your new password is: {password}")
    print("💡 Keep it in a safe place!")

password_generator_cli()

def test_password_generator():
    for i in range(100):
        length = random.randint(6, 30)
        password = generate_password(length)
        assert any(c.islower() for c in password), "No lowercase letter"
        assert any(c.isupper() for c in password), "No uppercase letter"
        assert any(c.isdigit() for c in password), "No digit"
        assert any(c in string.punctuation for c in password), "No special character"
        assert len(password) == length, "Wrong length"
        print(f"{i + 1:02d}. {password}")
    print("✅ All 100 passwords passed the test.")

test_password_generator()
