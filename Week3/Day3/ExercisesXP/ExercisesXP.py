#ExercisesXP.py

import os
import json
import random

#Exercise 1

def get_words_from_file(file_path):
    """
    Reads words from a text file and returns them as a list.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            word_list = content.split()
            return word_list
    except FileNotFoundError:
        print("Error: words.txt not found.")
        return []


def get_random_sentence(length):
    """
    Generates a random sentence with a given number of words.
    """
    words = get_words_from_file('words.txt')
    if not words:
        return "No words available."

    sentence = ' '.join(random.choice(words) for _ in range(length)).lower()
    return sentence

def main():
    """
    Handles user input and prints a random sentence.
    """
    print("Welcome to the Random Sentence Generator!")
    print("This program will generate a sentence using random English words.")

    user_input = input("Enter the length of the sentence (between 2 and 20): ")

    try:
        length = int(user_input)
        if 2 <= length <= 20:
            sentence = get_random_sentence(length)
            print("\nGenerated sentence:")
            print(sentence)
        else:
            print("Error: Number must be between 2 and 20.")
    except ValueError:
        print("Error: Invalid input. Please enter an integer.")

if __name__ == "__main__":
    main()

#Exercise 2

sampleJson = """{ 
   "company":{ 
      "employee":{ 
         "name":"emma",
         "payable":{ 
            "salary":7000,
            "bonus":800
         }
      }
   }
}"""

data = json.loads(sampleJson)

salary = data["company"]["employee"]["payable"]["salary"]
print("Salary:", salary)

data["company"]["employee"]["birth_date"] = "1990-05-21"

output_file = "modified_employee.json"

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)
