#ExercisesXPGold.py

import random

#Exercise 1

CURRENT_YEAR = 2025
CURRENT_MONTH = 7

def get_age(year, month, day):
    age = CURRENT_YEAR - year
    if CURRENT_MONTH < month:
        age -= 1
    return age

def can_retire(gender, date_of_birth):
    # date_of_birth : "yyyy/mm/dd"
    year, month, day = map(int, date_of_birth.split('/'))
    age = get_age(year, month, day)
    if gender == 'm':
        return age >= 67
    elif gender == 'f':
        return age >= 62
    else:
        return False

gender = input("What is your gender? (m/f): ").lower()
dob = input("Enter your date of birth (yyyy/mm/dd): ")
if can_retire(gender, dob):
    print("You can retire! 🎉")
else:
    print("You can't retire yet.")

#Exercise 2

def crazy_sum(x):
    return int(str(x)) + int(str(x)*2) + int(str(x)*3) + int(str(x)*4)
print(crazy_sum(3))

#Exercise 3

def throw_dice():
    return random.randint(1, 6)

def throw_until_doubles():
    throws = []
    while True:
        d1, d2 = throw_dice(), throw_dice()
        throws.append((d1, d2))
        if d1 == d2:
            break
    return throws

def main():
    all_throws = []
    for _ in range(100):
        run = throw_until_doubles()
        print(run)  # Affiche la séquence de couples pour ce run
        all_throws.append(len(run))
    total_throws = sum(all_throws)
    avg_throws = round(total_throws / len(all_throws), 2)
    print(f"Total throws: {total_throws}")
    print(f"Average throws to reach doubles: {avg_throws}")

main()

