#Exercises_XP_GOLD.py

#Exercise 1

print("Hello world\nHello world\nHello world\nHello world\nI love python\nI love python\nI love python\nI love python")

#Exercise 2

month = int(input("Enter month (1 to 12) : "))
if month < 1 or month > 12:
    print('Try again and enter a valid month')
else:
    if month in range(3,6):
        print('we are in spring')
    elif month in range(6,9):
        print('we are in summer')
    elif month in range(9,12):
        print('we are in autumn')
    else:
        print('we are in winter')


