#rock_paper_scissors.py

# rock-paper-scissors.py
from game import Game

def show_menu_once() -> str:
    """
    Show the 2-option menu once and return the raw choice.
    Valid returns: 'g' (play) or 'x' (show scores and exit).
    """
    print("\nMenu:")
    print("  (g) Play a new game")
    print("  (x) Show scores and exit")
    choice = input("  : ").strip().lower()
    return choice

def print_results(results: dict) -> None:
    """
    Print the results summary exactly like the screenshot.
    results: {'win': int, 'loss': int, 'draw': int}
    """
    print("\n  Game Results:")
    print(f"    You won {results.get('win', 0)} times")
    print(f"    You lost {results.get('loss', 0)} times")
    print(f"    You drew {results.get('draw', 0)} times\n")
    print("  Thank you for playing!\n")

def main():
    results = {"win": 0, "loss": 0, "draw": 0}
    while True:
        choice = show_menu_once()

        if choice == "g":
            game = Game()
            outcome = game.play()  # 'win' | 'loss' | 'draw'
            results[outcome] += 1

        elif choice == "x":
            print_results(results)
            break

        else:
            # If invalid, just re-loop (sample screenshot returns to menu after invalid input)
            print("❌ Invalid option. Choose 'g' to play or 'x' to exit.")

if __name__ == "__main__":
    main()
