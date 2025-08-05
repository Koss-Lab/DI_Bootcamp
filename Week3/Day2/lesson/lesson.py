#lesson.py

from datetime import datetime, date
class Person:
    id_number = 1
    def __init__(self, name, last_name, birth_date):
        self.name = name
        self.last_name = last_name
        self.birth_date = Person.parse_birthdate(birth_date)
        self.id = Person.id_number
        Person.id_number += 1
    @staticmethod
    def parse_birthdate(date_str):
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    @staticmethod
    def format_name(name_str):
        return name_str.strip().capitalize()
    @staticmethod
    def format_full_name(name, last_name):
        return f"{Person.format_name(name)} {Person.format_name(last_name)}"
    @classmethod
    def from_age(cls, name, last_name, age):
        today = datetime.today()
        birth_year = today.year - age
        birth_date = f"01-01-{birth_year}"  # default to Jan 1st
        return cls(name, last_name, birth_date)
    def age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        return age
    def __str__(self):
        return f"/n name: {self.name} /n last_name: {self.last_name} /n age: {self.age}"
    def __repr__(self):
        return f'{self.__dict__}'
    def __lt__(self, other):
        return self.age() < other.age()
    def __eq__(self, other):
        return self.age() == other.age()



# :coche_blanche: Example usage
print(datetime.today())  # prints today's date and time
p1 = Person("John", "Snow", "21-08-1990")
p2 = Person("Jane", "Doe", "16-02-1999")
p3 = Person.from_age("Bruce", "Wayne", 30)  # creates a person from age
# :coche_blanche: Output checks
print(Person.id_number)     # Output: 4 (3 people created)
print(p1.birth_date)        # Output: 1990-08-21
print(p2.birth_date)        # Output: 1999-02-16
print(p3.birth_date)        # Output: 1995-01-01 (depends on year)
print(p3.name)              # Output: Bruce
print(p3.id)                # Output: 3
print(Person.format_full_name("miCHAel", "sCoTT"))  # Output: Michael Scott










