#Exercises_XP_NINJA.py

#Exercises 1 and 2 on the terminal

#exercise 3

#>>> 3 <= 3 < 9
#>>> 3 == 3 == 3
#>>> bool(0)
#>>> bool(5 == "5")
#>>> bool(4 == 4) == bool("4" == "4")
#>>> bool(bool(None))
#x = (1 == True)
#y = (1 == False)
#a = True + 4
#b = False + 10

#print("x is", x)
#print("y is", y)
#print("a:", a)
#print("b:", b)

#True
#True
#False
#False
#True
#False
#x is True
#y is False
#a: 5
#b: 10

#Exercise 4

my_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

print(len(my_text))

#exercise 5

longest = ""

while True:
    sentence = input("Enter the longest sentence you can WITHOUT the letter 'A' (write 'exit' to end the game): ")

    if 'a' in sentence.lower():
        print("❌ Your sentence contains the letter 'A'! Try again.")
        continue

    if len(sentence) > len(longest):
        longest = sentence
        print("🎉 Congratulations! New record with", len(longest), "characters!")
    elif sentence.lower() == "exit":
        print("Goodbye 👋")
        break
    else:
        print("Nice try, but not longer than your best (" + str(len(longest)) + " chars).")

