#Exercises_XP_NINJA.py

#Exercise 1

import math

C = 50
H = 30
user_input = input("Enter comma-separated numbers (D values): ")
D_values = user_input.split(',')
results = []

for D in D_values:
    Q = round(math.sqrt((2 * C * int(D)) / H))
    results.append(Q)

print("Results:", ",".join(map(str, results)))

#Exercise 2

import random

numbers = [3, 47, 99, -80, 22, 97, 54, -23, 5, 7]

print("Original list:", numbers)
print("Descending:", sorted(numbers, reverse=True))
print("Sum:", sum(numbers))
print("First & Last:", [numbers[0], numbers[-1]])
print("Greater than 50:", [n for n in numbers if n > 50])
print("Smaller than 10:", [n for n in numbers if n < 10])
print("Squared:", [n ** 2 for n in numbers])
print("Without duplicates:", list(set(numbers)), "| Count:", len(set(numbers)))
print("Average:", sum(numbers) / len(numbers))
print("Max:", max(numbers))
print("Min:", min(numbers))

sum_manual = 0
max_manual = numbers[0]
min_manual = numbers[0]

for n in numbers:
    sum_manual += n
    if n > max_manual:
        max_manual = n
    if n < min_manual:
        min_manual = n

avg_manual = sum_manual / len(numbers)

print("Manual Sum:", sum_manual)
print("Manual Average:", avg_manual)
print("Manual Max:", max_manual)
print("Manual Min:", min_manual)


user_numbers = []
for i in range(10):
    val = int(input(f"Enter number {i+1}, between -100 and 100: "))
    user_numbers.append(val)
print("User List:", user_numbers)

random_numbers = [random.randint(-100, 100) for _ in range(10)]
print("Random numbers:", random_numbers)


count = random.randint(50, 100)
many_randoms = [random.randint(-100, 100) for _ in range(count)]
print(f"{count} Random Numbers Generated:", many_randoms)

#Exercise 3

paragraph = """In the heart of the desert lies a secret monastery. 
Many have passed by without knowing its presence, hidden between the rocks and silence.
Pilgrims say the winds carry prayers to the stars."""
print("Paragraph:", paragraph)

sentences = paragraph.split(".")
words = paragraph.split()
unique_words = set(words)
non_ws_chars = len(paragraph.replace(" ", "").replace("\n", ""))
non_unique_count = len(words) - len(unique_words)

print("Number of characters:", len(paragraph))
print("number of sentences:", len([s for s in sentences if s.strip() != ""]))
print("Number of words:", len(words))
print("Number of unique Words:", len(unique_words))
print("Number of non-whitespace chars:", non_ws_chars)
print("Number of avg words/sentence:", round(len(words) / len([s for s in sentences if s.strip() != ""]), 2))
print("Number of non-unique words:", non_unique_count)

#Exercise 4

text = input("Enter a sentence: ")
words = text.split()
freq = {}

for word in words:
    if word not in freq:
        freq[word] = 1
    else:
        freq[word] += 1

for word, count in freq.items():
    print(f"{word}:{count}")

