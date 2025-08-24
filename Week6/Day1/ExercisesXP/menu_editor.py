# menu_editor.py

from menu_item import MenuItem
from menu_manager import MenuManager

def show_user_menu():
    while True:
        print("\n--- Menu Manager ---")
        print("(V) View an Item")
        print("(A) Add an Item")
        print("(D) Delete an Item")
        print("(U) Update an Item")
        print("(S) Show the Menu")
        print("(E) Exit")
        choice = input("Choose an option: ").upper()

        if choice == "V":
            name = input("Enter the item name: ")
            item = MenuManager.get_by_name(name)
            if item:
                print(f"{item.name} – {item.price}₪")
            else:
                print("Item not found ❌")

        elif choice == "A":
            add_item_to_menu()

        elif choice == "D":
            remove_item_from_menu()

        elif choice == "U":
            update_item_from_menu()

        elif choice == "S":
            show_restaurant_menu()

        elif choice == "E":
            print("Exiting... Here is the final menu:")
            show_restaurant_menu()
            break

        else:
            print("Invalid choice ❌")

def add_item_to_menu():
    name = input("Enter item name: ")
    price = int(input("Enter item price: "))
    item = MenuItem(name, price)
    item.save()
    print("Item was added successfully ✅")

def remove_item_from_menu():
    name = input("Enter item name to delete: ")
    item = MenuItem(name, 0)
    try:
        item.delete()
        print("Item deleted successfully ✅")
    except:
        print("Error: could not delete ❌")

def update_item_from_menu():
    old_name = input("Enter current item name: ")
    old_price = int(input("Enter current price: "))
    new_name = input("Enter new item name: ")
    new_price = int(input("Enter new price: "))
    item = MenuItem(old_name, old_price)
    try:
        item.update(new_name, new_price)
        print("Item updated successfully ✅")
    except:
        print("Error: could not update ❌")

def show_restaurant_menu():
    items = MenuManager.all_items()
    print("\n--- Restaurant Menu ---")
    for item in items:
        print(f"{item.name} – {item.price}₪")

if __name__ == "__main__":
    show_user_menu()
