import json
import re
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    def validate(self):
        if not re.match(r'^\d{10}$', self.value):
            raise ValueError("Invalid phone number format")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [p.value for p in self.phones]:
            raise ValueError("Phone number {} not found in the record.".format(old_phone))
        else:
            for p in self.phones:
                if p.value == old_phone:
                    p.value = new_phone
                    p.validate()
                    break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for record in self.data.values():
            if record.name.value == name:
                return record
        return None

    def delete(self, name):
        del self.data[name]

class ContactManager:
    def __init__(self):
        self.address_book = AddressBook()
        self.load_contacts_from_file()

    def add_contact(self, name, phone):
        if name in self.address_book.data:
            self.address_book.data[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
        self.save_contacts_to_file()
        return 'Contact added.'

    def change_contact(self, name, old_phone, new_phone):
        if name in self.address_book.data:
            record = self.address_book.data[name]
            record.edit_phone(old_phone, new_phone)
            self.save_contacts_to_file()
            return 'Contact updated.'
        else:
            return f'Contact with name "{name}" not found.'

    def show_phone(self, name):
        if name in self.address_book.data:
            record = self.address_book.data[name]
            return '\n'.join([p.value for p in record.phones])
        else:
            return f'Contact with name "{name}" not found.'

    def show_all_contacts(self):
        if self.address_book.data:
            all_contacts = 'All contacts:\n'
            for record in self.address_book.data.values():
                all_contacts += f'{record.name.value}: {", ".join([p.value for p in record.phones])}\n'
            return all_contacts
        else:
            return 'No contacts saved.'

    def save_contacts_to_file(self):
        with open('contacts.json', 'w') as f:
            json.dump([{'name': record.name.value, 'phones': [p.value for p in record.phones]} for record in self.address_book.data.values()], f)

    def load_contacts_from_file(self):
        try:
            with open('contacts.json', 'r') as f:
                data = json.load(f)
                for contact in data:
                    record = Record(contact['name'])
                    for phone in contact['phones']:
                        record.add_phone(phone)
                    self.address_book.add_record(record)
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
        print("Available commands:\nhello - greet\nadd [name] [phone] - add a contact\nchange [name] [old phone] [new phone] - update a contact\nphone [name] - show phone number\nall - show all contacts\nclose or exit - close the bot")

        while True:
            user_input = input("Enter a command: ")
            command, args = self.parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == 'add':
                if len(args) == 2:
                    print(self.contact_manager.add_contact(*args))
                else:
                    print("Invalid command format. Please provide name and phone number.")
            elif command == 'change':
                if len(args) == 3:
                    print(self.contact_manager.change_contact(*args))
                else:
                    print("Invalid command format. Please provide name, old phone number, and new phone number.")
            elif command == 'phone':
                if len(args) == 1:
                    print(self.contact_manager.show_phone(*args))
                else:
                    print("Invalid command format. Please provide name.")
            elif command == 'all':
                print(self.contact_manager.show_all_contacts())
            elif command == "hello":
                print("How can I help you?")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()
