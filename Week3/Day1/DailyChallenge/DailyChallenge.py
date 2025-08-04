#DailyChallenge.py

import math

class Pagination:
    def __init__(self, items=None, page_size=10):
        self.items = items if items is not None else []
        self.page_size = page_size
        self.current_idx = 0
        self.total_pages = math.ceil(len(self.items) / self.page_size)

    def get_visible_items(self):
        start = self.current_idx * self.page_size
        end = start + self.page_size
        return self.items[start:end]

    def go_to_page(self, page_num):
        if not isinstance(page_num, int) or page_num < 1 or page_num > self.total_pages:
            raise ValueError(f"Page number must be between 1 and {self.total_pages}")
        self.current_idx = page_num - 1

    def first_page(self):
        self.current_idx = 0
        return self

    def last_page(self):
        self.current_idx = self.total_pages - 1
        return self

    def next_page(self):
        if self.current_idx < self.total_pages - 1:
            self.current_idx += 1
        return self

    def previous_page(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        return self

    def __str__(self):
        return "\n".join(self.get_visible_items())


alphabetList = list("abcdefghijklmnopqrstuvwxyz")
p = Pagination(alphabetList, 4)

print(p.get_visible_items())

p.next_page()
print(p.get_visible_items())

p.last_page()
print(p.get_visible_items())

try:
    p.go_to_page(10)
except ValueError as e:
    print("Error:", e)

p.go_to_page(6)
print(p.get_visible_items())

while True:
    print("\nCurrent page:", p.current_idx + 1)
    print(p.get_visible_items())

    command = input("Enter command (next, prev, first, last, go [n], exit): ")

    if command == "next":
        p.next_page()
    elif command == "prev":
        p.previous_page()
    elif command == "first":
        p.first_page()
    elif command == "last":
        p.last_page()
    elif command.startswith("go"):
        try:
            page_num = int(command.split()[1])
            p.go_to_page(page_num)
        except Exception as e:
            print("Error:", e)
    elif command == "exit":
        break
    else:
        print("Unknown command.")

