import re
from collections import UserDict
from datetime import datetime, timedelta

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found."

    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

class Birthday(Field):
    def __init__(self, value):
        try:
            date_format = '%m.%d.%Y'
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError('Invalid date format. Use MM.DD.YYYY')

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
        self.birthday = None

    def add_phone(self, phone):
        existing_phones = [p.value for p in self.phones]
        if phone not in existing_phones:
            self.phones.append(Phone(phone))
        else:
            return "Phone number already exists for this contact."

    def change_phone(self, new_phone):
        if len(self.phones) == 0:
            return "No phone numbers found for this contact."
        else:
            self.phones[0].value = new_phone
            return "Phone number updated successfully."

    def show_phone(self):
        if len(self.phones) == 0:
            return "No phone numbers found for this contact."
        else:
            return self.phones[0].value

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        else:
            return "Birthday not set for this contact."

class AddressBook(UserDict):
    @input_error
    def add(self, name, phone):
        if name in self.data:
            return self.data[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.data[name] = record
            return "Contact added successfully."

    @input_error
    def change(self, name, new_phone):
        if name in self.data:
            return self.data[name].change_phone(new_phone)
        else:
            return "Contact not found."

    @input_error
    def phone(self, name):
        if name in self.data:
            return self.data[name].show_phone()
        else:
            return "Contact not found."

    @input_error
    def add_birthday(self, name, birthday):
        if name in self.data:
            self.data[name].add_birthday(birthday)
            return "Birthday added successfully."
        else:
            return "Contact not found."

    @input_error
    def show_birthday(self, name):
        if name in self.data:
            return self.data[name].show_birthday()
        else:
            return "Contact not found."

    def birthdays_this_week(self):
        upcoming_birthdays = []
        today = datetime.today()
        for record in self.data.values():
             if record.birthday:
                birthday_month = record.birthday.value.month
                birthday_day = record.birthday.value.day
                for i in range(7):
                    next_date = today + timedelta(days=i)
                    if (birthday_month, birthday_day) == (next_date.month, next_date.day):
                        upcoming_birthdays.append((record.name.value, record.birthday.value))
                    break
        return upcoming_birthdays


def main():
    address_book = AddressBook()

    print("""Welcome to the Address Book Bot!
    Available commands:
    add [name] [phone]: Add a new contact or a phone number to an existing contact.
    change [name] [new_phone]: Change the phone number for the specified contact.
    phone [name]: Show the phone number for the specified contact.
    add-birthday [name] [birthday]: Add a birthday for the specified contact.
    show-birthday [name]: Show the birthday for the specified contact.
    birthdays: Show birthdays happening within the next week.
    hello: Get a greeting from the bot.
    close or exit: Close the program.""")

    while True:
        command = input("Enter command: ").strip()

        if command.startswith("add"):
            _, name, phone = command.split()
            result = address_book.add(name, phone)
            print(result)
        elif command.startswith("change"):
            _, name, new_phone = command.split()
            result = address_book.change(name, new_phone)
            print(result)
        elif command.startswith("phone"):
            _, name = command.split()
            result = address_book.phone(name)
            print(result)
        elif command.startswith("add-birthday"):
            _, name, birthday = command.split()
            result = address_book.add_birthday(name, birthday)
            print(result)
        elif command.startswith("show-birthday"):
            _, name = command.split()
            result = address_book.show_birthday(name)
            print(result)
        elif command == "birthdays":
            upcoming_birthdays = address_book.birthdays_this_week()
            if upcoming_birthdays:
                print("Upcoming birthdays within next week:")
                for name, birthday in upcoming_birthdays:
                    print(f"{name}: {birthday}")
            else:
                print("No upcoming birthdays within next week.")
        elif command == "hello":
            print("Hello! How can I assist you today?")
        elif command in ["close", "exit"]:
            print("Closing the program.")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()

