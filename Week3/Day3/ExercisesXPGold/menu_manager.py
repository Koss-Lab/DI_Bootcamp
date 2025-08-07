#menu_manager.py

import json
import os

class MenuManager:
    def __init__(self, menu_file="restaurant_menu.json"):
        self.menu_file = menu_file
        self.menu = self.load_menu()

    def load_menu(self):
        if not os.path.exists(self.menu_file):
            return {"items": []}
        with open(self.menu_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def add_item(self, name, price):
        new_item = {"name": name, "price": price}
        self.menu["items"].append(new_item)

    def remove_item(self, name):
        for i, item in enumerate(self.menu["items"]):
            if item["name"].lower() == name.lower():
                del self.menu["items"][i]
                return True
        return False

    def save_to_file(self):
        with open(self.menu_file, "w", encoding="utf-8") as f:
            json.dump(self.menu, f, indent=2)

    def get_menu(self):
        return self.menu["items"]
