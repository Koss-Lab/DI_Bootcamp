#while_loops.py

# for loops

# for <variable> in <sequence>:
#           intended block of code that will happen in each iteration
# Possible sequences be used : strings, lists, tuples, sets, range

#while loops

# while <condition> :
#           intended block of code to be exercuted until the condition is false, or there is the 'break' keyword

sequence = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
i = 0
while i < len(sequence):
    print(i)
    i += 1

#game

winner = False

while winner is False:
