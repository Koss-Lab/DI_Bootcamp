#DailyChallenge2.py

#Exercise 1

def sort_words():
    words = input("Enter words separated by commas: ")
    word_list = words.split(',')
    word_list.sort()
    sorted_words = ','.join(word_list)
    print(f"Sorted words: {sorted_words}")

sort_words()

#Exercise 2

def longest_word(sentence):
    words = sentence.split()
    longest = ""
    for word in words:
        if len(word) > len(longest):
            longest = word
    return longest

print(longest_word("Margaret's toy is a pretty doll."))
print(longest_word("A thing of beauty is a joy forever."))
print(longest_word("Forgetfulness is by all means powerless!"))

