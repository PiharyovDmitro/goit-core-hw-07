import json

class ContactManager:
    def __init__(self):
        self.contacts = {}
        self.load_contacts_from_file()

    def add_contact(self, name, phone):
        self.contacts[name] = phone
        self.save_contacts_to_file()
        return 'Contact added.'

    def change_contact(self, name, new_phone):
        if name in self.contacts:
            self.contacts[name] = new_phone
            self.save_contacts_to_file()
            return 'Contact updated.'
        else:
            return f'Contact with name "{name}" not found.'

    def show_phone(self, name):
        if name in self.contacts:
            return self.contacts[name]
        else:
            return f'Contact with name "{name}" not found.'

    def show_all_contacts(self):
        if self.contacts:
            all_contacts = 'All contacts:\n'
            for name, phone in self.contacts.items():
                all_contacts += f'{name}: {phone}\n'
            return all_contacts
        else:
            return 'No contacts saved.'

    def save_contacts_to_file(self):
        with open('contacts.json', 'w') as f:
            json.dump(self.contacts, f)

    def load_contacts_from_file(self):
        try:
            with open('contacts.json', 'r') as f:
                self.contacts = json.load(f)
        except FileNotFoundError:
            pass

class AssistantBot:
    def __init__(self):
        self.contact_manager = ContactManager()

    def greet(self):
        print("Welcome to the assistant bot!")

    def parse_input(self, user_input):
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args

    def run(self):
        self.greet()
        print("Available commands:\nhello - greet\nadd [name] [phone] - add a contact\nchange [name] [new phone] - update a contact\nphone [name] - show phone number\nall - show all contacts\nclose or exit - close the bot")

        while True:
            user_input = input("Enter a command: ")
            command, args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == 'add':
                print(self.contact_manager.add_contact(*args))
            elif command == 'change':
                print(self.contact_manager.change_contact(*args))
            elif command == 'phone':
                print(self.contact_manager.show_phone(*args))
            elif command == 'all':
                print(self.contact_manager.show_all_contacts())
            elif command == "hello":
                print("How can I help you?")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()
