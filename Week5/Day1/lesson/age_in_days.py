#age_in_days.py

from datetime import date

# Edit these with your DOB
birth_year = 1998
birth_month = 9
birth_day = 23

today = date.today()
birthday = date(birth_year, birth_month, birth_day)
age_days = (today - birthday).days
print(f"Age in days: {age_days}")
