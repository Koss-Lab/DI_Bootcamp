class Phone:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.call_history = []  # A list to store call history
        self.messages = []  # A list to store messages

    # Method to make a call to another phone
    def call(self, other_phone):
        call_message = f"Call from {self.phone_number} to {other_phone.phone_number}"
        print(call_message)
        self.call_history.append(call_message)

    # Method to show the call history
    def show_call_history(self):
        print(f"Call history for {self.phone_number}:")
        for call in self.call_history:
            print(call)

    # Method to send a message to another phone
    def send_message(self, other_phone, content):
        # Ensure message has 'to', 'from', and 'content' keys
        message = {
            "to": other_phone.phone_number,
            "from": self.phone_number,
            "content": content
        }
        self.messages.append(message)
        print(f"Message sent from {self.phone_number} to {other_phone.phone_number}: {content}")

    # Method to show all outgoing messages
    def show_outgoing_messages(self):
        print(f"Outgoing messages from {self.phone_number}:")
        for message in self.messages:
            if message["from"] == self.phone_number:
                print(f"To: {message['to']}, Message: {message['content']}")

    # Method to show all incoming messages
    def show_incoming_messages(self):
        print(f"Incoming messages to {self.phone_number}:")
        for message in self.messages:
            if message["to"] == self.phone_number:
                print(f"From: {message['from']}, Message: {message['content']}")

    # Method to show all messages from a specific phone number
    def show_messages_from(self, sender_phone):
        print(f"Messages from {sender_phone.phone_number} to {self.phone_number}:")
        for message in self.messages:
            if message["from"] == sender_phone.phone_number:
                print(f"To: {message['to']}, Message: {message['content']}")

# Testing the Phone class
phone1 = Phone("123-456-7890")
phone2 = Phone("987-654-3210")

# Making calls
phone1.call(phone2)
phone2.call(phone1)

# Show call history
phone1.show_call_history()
phone2.show_call_history()

# Sending messages
phone1.send_message(phone2, "Hey, how are you?")
phone2.send_message(phone1, "I'm good, thanks!")

# Show messages
phone1.show_outgoing_messages()
phone2.show_incoming_messages()

# Show messages from a specific number
phone1.show_messages_from(phone2)
