#DailyChallenge.py

import random

list_of_numbers = [random.randint(0, 10000) for _ in range(20000)]

target_number   = 3728

pairs = []

count_dict = {}

for num in list_of_numbers:
    complement = target_number - num
    if complement in count_dict:
        pairs.append((complement, num))
        count_dict[complement] -= 1
    else:
        if num not in count_dict:
            count_dict[num] = 0
            count_dict[num] += 1

print(f'Found {len(pairs)} pairs that sum to {target_number}')
for pair in pairs:
    print(pair)
