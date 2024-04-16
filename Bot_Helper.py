import json
import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def validate(self):
        if not re.match(r'^\d{10}$', self.value):
            raise ValueError("Invalid phone number format")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone not in [p.value for p in self.phones]:
            raise ValueError("Phone number {} not found in the record.".format(old_phone))
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                p.validate()
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        return next((p for p in self.phones if p.value == phone), None)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value.replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                if (birthday_date - today).days <= 7:
                    upcoming_birthdays.append((record.name.value, birthday_date))
        return upcoming_birthdays

    def get_birthday(self, name):
        record = self.data.get(name)
        if record and record.birthday:
            return record.birthday.value.strftime('%d.%m.%Y')
        return f'Birthday not found for {name}'

    def get_next_week_birthdays(self):
        next_week_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value.replace(year=today.year)
                if birthday_date < today:
                    birthday_date = birthday_date.replace(year=today.year + 1)
                if today <= birthday_date <= next_week:
                    next_week_birthdays.append((record.name.value, birthday_date))
        return next_week_birthdays

class ContactManager:
    def __init__(self):
        self.address_book = AddressBook()
        self.load_contacts_from_file()

    def add_contact(self, name, phone):
        record = self.address_book.get(name)
        if record:
            record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
        self.save_contacts_to_file()
        return 'Contact added.'

    def add_birthday(self, name, birthday):
        record = self.address_book.get(name)
        if record:
            record.add_birthday(birthday)
            self.save_contacts_to_file()
            return 'Birthday added to contact.'
        return f'Contact with name "{name}" not found.'

    def change_contact(self, name, old_phone, new_phone):
        record = self.address_book.get(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            self.save_contacts_to_file()
            return 'Contact updated.'
        return f'Contact with name "{name}" not found.'

    def show_phone(self, name):
        record = self.address_book.get(name)
        if record:
            return '\n'.join([p.value for p in record.phones])
        return f'Contact with name "{name}" not found.'

    def show_all_contacts(self):
        if self.address_book.data:
            all_contacts = 'All contacts:\n'
            for record in self.address_book.data.values():
                all_contacts += f'{record.name.value}: {", ".join([p.value for p in record.phones])}\n'
            return all_contacts
        return 'No contacts saved.'

    def save_contacts_to_file(self):
        with open('contacts.json', 'w') as f:
            json.dump([
                {'name': record.name.value,
                 'phones': [p.value for p in record.phones],
                 'birthday': record.birthday.value.strftime('%d.%m.%Y') if record.birthday else None}
                for record in self.address_book.data.values()], f)

    def load_contacts_from_file(self):
        try:
            with open('contacts.json', 'r') as f:
                data = json.load(f)
                for contact in data:
                    record = Record(contact['name'])
                    for phone in contact['phones']:
                        record.add_phone(phone)
                    if contact['birthday']:
                        record.add_birthday(contact['birthday'])
                    self.address_book.add_record(record)
        except FileNotFoundError:
            pass

class AssistantBot:
    def __init__(self):
        self.contact_manager = ContactManager()

    def greet(self):
        print("Welcome to the assistant bot!")

    def parse_input(self, user_input):
        return user_input.strip().lower().split(maxsplit=2)

    def run(self):
        self.greet()
        print("""Available commands:
- add [name] [phone]: Add or update a contact with the given name and phone number.
- change [name] [new phone]: Change phone number for the specified contact.
- phone [name]: Show phone number for the specified contact.
- all: Show all contacts.
- add-birthday [name] [birthday]: Add birthday for the specified contact.
- show-birthday [name]: Show birthday for the specified contact.
- birthdays: Show upcoming birthdays for the next week.
- hello: Get a greeting from the bot.
- close or exit: Close the bot.""")

        while True:
            user_input = input("Enter a command: ")
            command, *args = self.parse_input(user_input)

            if command == "exit" or command == "close":
                print("Good bye!")
                break
            elif command == 'add':
                if len(args) == 2:
                    print(self.contact_manager.add_contact(*args))
                else:
                    print("Invalid command format. Please provide name and phone number.")
            elif command == 'add_birthday':
                if len(args) == 2:
                    print(self.contact_manager.add_birthday(*args))
                else:
                    print("Invalid command format. Please provide name and birthday (DD.MM.YYYY).")
            elif command == 'change':
                if len(args) == 2:
                    print(self.contact_manager.change_contact(*args))
                else:
                    print("Invalid command format. Please provide name and new phone number.")
            elif command == 'phone':
                if len(args) == 1:
                    print(self.contact_manager.show_phone(*args))
                else:
                    print("Invalid command format. Please provide name.")
            elif command == 'all':
                print(self.contact_manager.show_all_contacts())
            elif command == 'upcoming_birthdays':
                upcoming_birthdays = self.contact_manager.address_book.get_upcoming_birthdays()
                if upcoming_birthdays:
                    print("Upcoming birthdays:")
                    for name, birthday in upcoming_birthdays:
                        print(f'{name}: {birthday.strftime("%d.%m.%Y")}')
                else:
                    print("No upcoming birthdays.")
            elif command == 'show_birthday':
                if len(args) == 1:
                    print(self.contact_manager.address_book.get_birthday(args[0]))
                else:
                    print("Invalid command format. Please provide name.")
            elif command == 'birthdays':
                next_week_birthdays = self.contact_manager.address_book.get_next_week_birthdays()
                if next_week_birthdays:
                    print("Users to greet next week:")
                    for name, birthday in next_week_birthdays:
                        print(f'{name}: {birthday.strftime("%d.%m.%Y")}')
                else:
                    print("No users to greet next week.")
            elif command == "hello":
                print("How can I help you?")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()