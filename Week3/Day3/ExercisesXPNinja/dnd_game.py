import random
import json

class Character:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.attributes = self.generate_attributes()

    def generate_attributes(self):
        """
        Rolls 4d6 and keeps the highest 3, six times.
        """
        stats = {}
        abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        for ability in abilities:
            rolls = [random.randint(1, 6) for _ in range(4)]
            rolls.sort(reverse=True)
            score = sum(rolls[:3])
            stats[ability] = score
        return stats

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "attributes": self.attributes
        }

    def to_text(self):
        """
        Returns a nicely formatted character sheet as string.
        """
        lines = [f"Name: {self.name}", f"Age: {self.age}", "Stats:"]
        for key, value in self.attributes.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)

class Game:
    def __init__(self):
        self.characters = []

    def start(self):
        print("🎲 Welcome to Dungeons & Dragons Character Creator!")
        num_players = input("How many players? ")

        try:
            num_players = int(num_players)
        except ValueError:
            print("Invalid input. Must be a number.")
            return

        for i in range(num_players):
            print(f"\nCreating character #{i+1}")
            name = input("Enter character name: ")
            age = input("Enter character age: ")
            self.characters.append(Character(name, age))

        self.export_to_json()
        self.export_to_txt()
        print("\n✅ Characters saved to 'characters.json' and 'characters.txt'")

    def export_to_json(self):
        data = [char.to_dict() for char in self.characters]
        with open("characters.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def export_to_txt(self):
        with open("characters.txt", "w", encoding="utf-8") as f:
            for char in self.characters:
                f.write(char.to_text())
                f.write("\n\n")

if __name__ == "__main__":
    game = Game()
    game.start()
