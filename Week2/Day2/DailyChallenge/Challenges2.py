#Challenges2.py

#Exercise 1

# Pattern 1
n = 3  # Number of rows
for i in range(1, n + 1):  # Loop through rows
    print(' ' * (n - i) + '*' * (2 * i - 1))  # Print spaces and stars

# Pattern 2
n = 5  # Number of rows
for i in range(1, n + 1):  # Loop through rows
    print(' ' * (n - i) + '*' * i)  # Print spaces and stars

# Pattern 3
n = 5  # Number of rows for the first half
# Top half of the pattern (increasing)
for i in range(1, n + 1):
    print('*' * i)

# Bottom half of the pattern (decreasing)
for i in range(n, 0, -1):
    print(' ' * (n - i) + '*' * i)

#Exercise 2

my_list = [2, 24, 12, 354, 233]  # Initialize the list
for i in range(len(my_list) - 1):  # Outer loop, i goes from 0 to 3
    minimum = i  # Initialize minimum index as i
    for j in range(i + 1, len(my_list)):  # Inner loop, j goes from i+1 to the end of the list
        if my_list[j] < my_list[minimum]:  # Check if current element is smaller than the element at minimum index
            minimum = j  # If true, update minimum index
            if minimum != i:  # If minimum index is not i, swap the elements
                my_list[i], my_list[minimum] = my_list[minimum], my_list[i]  # Swap elements at i and minimum index
print(my_list)  # Output the final list
