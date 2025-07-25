#DailyChallengeGOLD_CaesarCipher.py

def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            encrypted_text += encrypted_char
        else:
            encrypted_text += char
    return encrypted_text


def decrypt(text, shift):
    return encrypt(text, -shift)


def main():
    print("Welcome to the Caesar Cipher Program 🏛️")
    choice = input("Type 'encrypt' to encode or 'decrypt' to decode: ").lower()

    if choice not in ['encrypt', 'decrypt']:
        print("Invalid choice. Please type 'encrypt' or 'decrypt'.")
        return

    message = input("Enter your message: ")

    try:
        shift = int(input("Enter the shift number (e.g., 3): "))
    except ValueError:
        print("Shift must be a number.")
        return

    if choice == "encrypt":
        result = encrypt(message, shift)
    else:
        result = decrypt(message, shift)

    print(f"\nResult: {result}")

if __name__ == "__main__":
    main()
