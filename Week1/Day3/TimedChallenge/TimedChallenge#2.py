#Python3 TimedChallenge#2.py

x = int(input("Enter the Number: "))

divisor_sum = sum(i for i in range(1, x) if x % i == 0)

print(divisor_sum == x)
