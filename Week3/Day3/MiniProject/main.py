#main.py

from vaccine_system import Human, Queue

if __name__ == "__main__":
    h1 = Human("001", "Alice", 65, False, "A")
    h2 = Human("002", "Bob", 35, True, "B")
    h3 = Human("003", "Charlie", 30, False, "O")
    h4 = Human("004", "Diana", 70, False, "AB")
    h5 = Human("005", "Eve", 25, False, "A")

    # Add family relations
    h1.add_family_member(h3)
    h2.add_family_member(h5)

    q = Queue()
    q.add_person(h1)
    q.add_person(h2)
    q.add_person(h3)
    q.add_person(h4)
    q.add_person(h5)

    print("Queue before rearrange:")
    for h in q.humans:
        print(h.name)

    q.rearrange_queue()

    print("\nQueue after rearrange:")
    for h in q.humans:
        print(h.name)
