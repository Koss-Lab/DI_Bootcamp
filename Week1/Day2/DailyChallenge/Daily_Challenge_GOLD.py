#Daily_Challenge_GOLD.py

from datetime import datetime


birthdate_str = input("Please enter your birthdate (DD/MM/YYYY): ")
birthdate = datetime.strptime(birthdate_str, "%d/%m/%Y")

current_date = datetime.now()

age = current_date.year - birthdate.year - ((current_date.month, current_date.day) < (birthdate.month, birthdate.day))

last_digit_of_age = age % 10

is_leap_year = (birthdate.year % 4 == 0 and (birthdate.year % 100 != 0 or birthdate.year % 400 == 0))

def display_cake(candles):
    cake = f"""
       ___iiiii___
      |:H:a:p:p:y:|
    __|___________|__
   |^^^^^^^^^^^^^^^^^|
   |:B:i:r:t:h:d:a:y:|
   |{' ' * (17 - candles)}{'*' * candles}|
   ~~~~~~~~~~~~~~~~~~~
    """
    cake_with_candles = cake.replace("   |{' ' * 17}|", f"   |{'*' * candles}{' ' * (17 - candles)}|")
    print(cake_with_candles)

display_cake(last_digit_of_age)

if is_leap_year:
    print("\nSince you were born in a leap year, here is a second cake for you!")
    display_cake(last_digit_of_age)
