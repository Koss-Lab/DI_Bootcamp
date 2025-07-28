#ExercisesXPNinja.py

#Exercise 1

def get_full_name(first_name, last_name, middle_name=None):
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    if middle_name:
        middle_name = middle_name.capitalize()
        return f"{first_name} {middle_name} {last_name}"
    else:
        return f"{first_name} {last_name}"

print(get_full_name(first_name="john", middle_name="hooker", last_name="lee"))
print(get_full_name(first_name="bruce", last_name="lee"))

#Exercise 2

MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.'
}

def english_to_morse(text):
    text = text.upper()
    morse = []
    for word in text.split(' '):
        coded = ' '.join(MORSE_CODE_DICT.get(char, '') for char in word)
        morse.append(coded)
    return ' / '.join(morse)

def morse_to_english(morse):
    reverse_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
    words = morse.split(' / ')
    decoded_words = []
    for word in words:
        letters = word.split()
        decoded = ''.join(reverse_dict.get(l, '') for l in letters)
        decoded_words.append(decoded)
    return ' '.join(decoded_words)

print(english_to_morse("Hello World"))
print(morse_to_english(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."))

#Exercise 3

def box_printer(*args):
    max_length = max(len(word) for word in args)
    border = '*' * (max_length + 4)
    print(border)
    for word in args:
        print(f"* {word}{' ' * (max_length - len(word))} *")
    print(border)

box_printer("Hello", "World", "in", "reallylongword", "a", "frame")

#Exercise 4

def insertion_sort(alist):
    # Start from the second element (index 1) and iterate to the end
    for index in range(1, len(alist)):
        currentvalue = alist[index]      # Store the current value to be inserted
        position = index                 # Remember the current index

        # Shift elements of the sorted part of the list that are greater than currentvalue
        while position > 0 and alist[position - 1] > currentvalue:
            alist[position] = alist[position - 1]  # Move the larger element to the right
            position = position - 1                # Move to the next position on the left

        # Insert the current value in its correct position
        alist[position] = currentvalue

alist = [54, 26, 93, 17, 77, 31, 44, 55, 20]
insertion_sort(alist)
print(alist)  # Output: [17, 20, 26, 31, 44, 54, 55, 77, 93]

