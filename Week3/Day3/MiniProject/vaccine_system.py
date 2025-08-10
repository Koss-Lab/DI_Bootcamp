#vaccine_system.py

class Human:
    def __init__(self, id_number, name, age, priority, blood_type):
        self.id_number = id_number            # Unique ID of the human
        self.name = name                      # Human's name
        self.age = age                        # Human's age
        self.priority = priority              # Is the person priority (True/False)
        self.blood_type = blood_type          # "A", "B", "AB" or "O"
        self.family = []                      # List of family members (other Human objects)

    def add_family_member(self, person):
        # Add the person to this human’s family list (and vice versa)
        if person not in self.family:
            self.family.append(person)
        if self not in person.family:
            person.family.append(self)


class Queue:
    def __init__(self):
        self.humans = []  # List of humans waiting in the queue

    def add_person(self, person):
        # Add the human to the queue
        # If age > 60 or priority, add to the front manually (no insert)
        if person.age > 60 or person.priority:
            self.humans = [person] + self.humans
        else:
            self.humans += [person]

    def find_in_queue(self, person):
        # Return index of the human in the queue (or None if not found)
        for i in range(len(self.humans)):
            if self.humans[i] == person:
                return i
        return None

    def swap(self, person1, person2):
        # Swap two people in the queue
        index1 = self.find_in_queue(person1)
        index2 = self.find_in_queue(person2)
        if index1 is not None and index2 is not None:
            self.humans[index1], self.humans[index2] = self.humans[index2], self.humans[index1]

    def get_next(self):
        # Return the next person in the queue and remove them
        if len(self.humans) == 0:
            return None
        next_person = self.humans[0]
        self.humans = self.humans[1:]  # Remove without using pop
        return next_person

    def get_next_blood_type(self, blood_type):
        # Return the first person with the given blood type, and remove them
        for i in range(len(self.humans)):
            if self.humans[i].blood_type == blood_type:
                result = self.humans[i]
                self.humans = self.humans[:i] + self.humans[i+1:]  # Remove manually
                return result
        return None

    def sort_by_age(self):
        # Sort the queue: priority people → older than 60 → everyone else
        priority = []
        older = []
        younger = []

        for person in self.humans:
            if person.priority:
                priority += [person]
            elif person.age > 60:
                older += [person]
            else:
                younger += [person]

        self.humans = priority + older + younger  # Rebuild the queue

    def rearrange_queue(self):
        # Make sure no family members are standing right next to each other
        if len(self.humans) <= 1:
            return

        result = [self.humans[0]]  # Start with first person

        for i in range(1, len(self.humans)):
            current = self.humans[i]
            prev = result[-1]
            if current not in prev.family:
                result += [current]
            else:
                # Try to find someone to swap with further down the queue
                j = i + 1
                while j < len(self.humans):
                    if self.humans[j] not in prev.family:
                        # Swap current with j
                        self.humans[i], self.humans[j] = self.humans[j], self.humans[i]
                        result += [self.humans[i]]
                        break
                    j += 1
                else:
                    # Couldn't find anyone to swap with, just add them
                    result += [current]

        self.humans = result

