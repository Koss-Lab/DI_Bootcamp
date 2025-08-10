# anagrams.py

from anagram_checker import AnagramChecker

def main():
    checker = AnagramChecker("words.txt")  # Remplace par ton fichier de mots

    while True:
        print("\n--- ANAGRAM CHECKER ---")
        print("1. Input a word")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "2":
            print("Bye!")
            break

        elif choice == "1":
            word = input("Enter a single word: ").strip()

            # Validation: one word only
            if " " in word:
                print("❌ Error: Please enter only one word.")
                continue

            # Validation: only letters
            if not word.isalpha():
                print("❌ Error: Only alphabetic characters are allowed.")
                continue

            # Check if valid word
            if not checker.is_valid_word(word):
                print(f"❌ '{word}' is not a valid English word.")
                continue

            # Get anagrams
            anagrams = checker.get_anagrams(word)

            print(f"\nYOUR WORD: \"{word.upper()}\"")
            print("This is a valid English word.")
            if anagrams:
                print("Anagrams for your word:", ", ".join(anagrams))
            else:
                print("No anagrams found.")

        else:
            print("❌ Invalid option. Please choose 1 or 2.")

if __name__ == "__main__":
    main()
