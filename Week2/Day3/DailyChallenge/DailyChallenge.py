#DailyChallenge.py


class Farm:
    def __init__(self, farm_name):
        self.name = farm_name
        self.animals = {}

    def add_animal(self, animal_type, count=1):
        if animal_type in self.animals:
            self.animals[animal_type] += count
        else:
            self.animals[animal_type] = count

    def get_info(self):
        farm_info = f"{self.name}'s farm\n"
        for animal, count in sorted(self.animals.items()):
            farm_info += f"\n{animal} : {count}"
        farm_info += "\n\n    E-I-E-I-0!"
        return farm_info

    def get_animal_types(self):
        return sorted(self.animals.keys())

    def get_short_info(self):
        animal_types = self.get_animal_types()
        animal_info = ", ".join([f"{animal}s" if self.animals[animal] > 1 else animal for animal in animal_types])
        return f"{self.name}'s farm has {animal_info}."


macdonald = Farm("McDonald")
macdonald.add_animal('cow', 5)
macdonald.add_animal('sheep')
macdonald.add_animal('sheep')
macdonald.add_animal('goat', 12)
print(macdonald.get_info())
print(macdonald.get_animal_types())
print(macdonald.get_short_info())
