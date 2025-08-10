#game.py

import random

class Game:
    VALID_ITEMS = ("rock", "paper", "scissors")
    SHORTMAP = {"r": "rock", "p": "paper", "s": "scissors"}
    REVMAP = {"rock": "r", "paper": "p", "scissors": "s"}

    def get_user_item(self) -> str:
        """
        Ask the user for (r/p/s). Accepts full words too.
        Returns the long form: 'rock' | 'paper' | 'scissors'.
        """
        while True:
            choice = input("Select (r)ock, (p)aper, or (s)cissors: ").strip().lower()
            if choice in self.SHORTMAP:
                return self.SHORTMAP[choice]
            if choice in self.VALID_ITEMS:
                return choice
            print("❌ Invalid choice. Type r, p, or s.")

    def get_computer_item(self) -> str:
        """Return a random long-form item."""
        return random.choice(self.VALID_ITEMS)

    def get_game_result(self, user_item: str, computer_item: str) -> str:
        """
        Compare user vs computer and return: 'win' | 'draw' | 'loss'.
        """
        if user_item == computer_item:
            return "draw"
        wins_against = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
        return "win" if wins_against[user_item] == computer_item else "loss"

    def play(self) -> str:
        """
        Play one round, print outcome like the screenshot, and return the result.
        """
        user_item = self.get_user_item()
        computer_item = self.get_computer_item()
        result = self.get_game_result(user_item, computer_item)

        # Print in short-letter style to match the sample output
        print(
            f"You chose: {self.REVMAP[user_item]}. "
            f"The computer chose: {self.REVMAP[computer_item]}. "
            f"Result: {result}"
        )
        return result
