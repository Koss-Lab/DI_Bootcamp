import random

wordslist = ['correction', 'childish', 'beach', 'python', 'assertive', 'interference', 'complete', 'share', 'credit card', 'rush', 'south']
word = random.choice(wordslist)

word_length = len(word)
guessed_word = ['_'] * word_length
guessed_letters = set()
wrong_guesses = 0

gallows = [
    '''
     -----
     |   |
         |
         |
         |
         |
    ''',
    '''
     -----
     |   |
     O   |
         |
         |
         |
    ''',
    '''
     -----
     |   |
     O   |
     |   |
         |
         |
    ''',
    '''
     -----
     |   |
     O   |
    /|   |
         |
         |
    ''',
    '''
     -----
     |   |
     O   |
    /|\\  |
         |
         |
    ''',
    '''
     -----
     |   |
     O   |
    /|\\  |
    /    |
         |
    ''',
    '''
     -----
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    '''
]

def display_game():
    print(' '.join(guessed_word))
    print(gallows[wrong_guesses])

while wrong_guesses < 6 and '_' in guessed_word:
    display_game()
    guess = input("Guess a letter: ").lower()

    if guess in guessed_letters:
        print("You've already guessed that letter. Try again.")
        continue
    elif len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    guessed_letters.add(guess)

    if guess in word:
        for i in range(word_length):
            if word[i] == guess:
                guessed_word[i] = guess
        print(f"Good guess! '{guess}' is in the word.")
    else:
        wrong_guesses += 1
        print(f"Wrong guess! '{guess}' is not in the word.")

if wrong_guesses == 6:
    print("You lost! The word was:", word)
else:
    print("Congratulations! You guessed the word:", word)
