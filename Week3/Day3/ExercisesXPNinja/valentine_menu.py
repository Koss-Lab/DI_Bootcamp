import re
import json
import os


def load_menu(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_menu(menu, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(menu, f, indent=2)


def is_valid_name(name):
    # First word must start with V uppercase
    if not name.split()[0].startswith("V"):
        return False

    # Connection words allowed in lowercase
    connection_words = ['of', 'the', 'and', 'in', 'with', 'on', 'for']

    words = name.split()
    for word in words:
        if word.lower() in connection_words:
            if word != word.lower():
                return False
        else:
            if not word[0].isupper():
                return False

    # At least two 'e' and no numbers
    if name.count('e') < 2:
        return False
    if re.search(r'\d', name):
        return False

    return True


def is_valid_price(price):
    return re.fullmatch(r'\d{2},14', price) is not None


def display_heart():
    heart = [
        "  **   **  ",
        " **** **** ",
        " ********* ",
        "  *******  ",
        "   *****   ",
        "    ***    ",
        "     *     "
    ]
    for line in heart:
        print(line)


def add_valentine_item():
    file_path = "restaurant_menu.json"
    menu = load_menu(file_path)

    name = input("Enter the Valentine's Day item name: ").strip()
    price = input("Enter the price (format XX,14): ").strip()

    if is_valid_name(name) and is_valid_price(price):
        menu["valentines_items"].append({"name": name, "price": price})
        save_menu(menu, file_path)
        print("✅ Item added to Valentine’s Day menu.")
    else:
        print("❌ Invalid item. Please follow the Valentine’s rules.")

    print("\n❤️ Here’s your special menu display:\n")
    display_heart()


if __name__ == "__main__":
    add_valentine_item()
