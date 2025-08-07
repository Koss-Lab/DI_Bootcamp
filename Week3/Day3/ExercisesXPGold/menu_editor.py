#menu_editor.py

from menu_manager import MenuManager

def load_manager():
    return MenuManager()

def show_user_menu():
    print("\n--- Menu Manager ---")
    print("1. View restaurant menu")
    print("2. Add item to menu")
    print("3. Remove item from menu")
    print("4. Save and exit")

def add_item_to_menu(manager):
    name = input("Enter the item name: ")
    try:
        price = float(input("Enter the item price: "))
        manager.add_item(name, price)
        print("Item added successfully.")
    except ValueError:
        print("Invalid price. Must be a number.")

def remove_item_from_menu(manager):
    name = input("Enter the item name to remove: ")
    success = manager.remove_item(name)
    if success:
        print("Item removed successfully.")
    else:
        print("Error: Item not found.")

def show_restaurant_menu(manager):
    print("\n--- Restaurant Menu ---")
    for item in manager.get_menu():
        print(f"- {item['name']}: {item['price']} ₪")

def main():
    manager = load_manager()
    while True:
        show_user_menu()
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            show_restaurant_menu(manager)
        elif choice == "2":
            add_item_to_menu(manager)
        elif choice == "3":
            remove_item_from_menu(manager)
        elif choice == "4":
            manager.save_to_file()
            print("Menu saved. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
