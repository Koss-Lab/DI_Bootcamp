#DailyChallenge.py

MATRIX_STR = '''
7ir
Tsi
h%x
i ?
sM# 
$a 
#t%'''

# Step 1: Convert matrix_string to a 2D list (matrix)
matrix = []
for row in MATRIX_STR.strip().split('\n'):
    matrix.append(list(row))

# Step 2: Iterate through columns (Neo-style!)
num_rows = len(matrix)
num_cols = len(matrix[0])
raw_message = ""

for col in range(num_cols):
    for row in range(num_rows):
        raw_message += matrix[row][col]

# Step 3: Filtering alpha characters (and Step 4: Replace symbols by spaces)
# We build the message, inserting spaces only between alpha blocks separated by symbols

final_message = ""
buffer = ""
for char in raw_message:
    if char.isalpha():
        if buffer and not buffer[-1].isalpha():
            final_message += " "
        final_message += char
    else:
        final_message += " "  # Mark symbol positions as space

# Remove extra spaces
import re
final_message = re.sub(' +', ' ', final_message).strip()

# Step 5: Print the decoded message
print(final_message)
