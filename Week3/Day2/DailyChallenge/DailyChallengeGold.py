#DailyChallengeGold.py

user_data = []

for _ in range(5):
    raw = input("Enter name, age, score (comma-separated): ")
    name, age, score = raw.strip().split(",")
    user_data.append((name, age, score))

sorted_data = sorted(user_data, key=lambda x: (x[0], int(x[1]), int(x[2])))

print(sorted_data)

