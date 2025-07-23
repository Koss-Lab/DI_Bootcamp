#Daily_Challenge.py

#Exercise 1

number = int(input("Enter a number: "))
length = int(input("Enter the length: "))

multiples = []
for i in range(1, length + 1):
    multiples.append(number * i)

print(multiples)

#Exercise 2

word = input("Enter a word: ")

new_word = ""
for i in range(len(word)):
    if i == 0 or word[i] != word[i - 1]:
        new_word += word[i]

print(new_word)


