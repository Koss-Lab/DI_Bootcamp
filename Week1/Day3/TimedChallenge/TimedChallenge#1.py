#python3 TimedChallenge#1.py

# yoda_reverser.py

sentence = input("💬 Speak, you must:\n> ")
print("\n🧙‍♂️ Yoda says:\n" + ' '.join(sentence.split()[::-1]))

