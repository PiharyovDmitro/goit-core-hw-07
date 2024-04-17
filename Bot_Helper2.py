import re
from collections import UserDict
from datetime import datetime, timedelta

# Декоратор для обробки помилок введення
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

# Базовий клас для поля контакту
class Field:
    def __init__(self, value):
        self.value = value

# Клас для обробки дати народження
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            date_format = '%m.%d.%Y'
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError('Invalid date format. Use MM.DD.YYYY')

# Клас для імені контакту
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

# Клас для телефонного номеру контакту
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate()

    # Валідація телефонного номеру
    def validate(self):
        if not re.match(r'^\d{10}$', self.value):
            raise ValueError("Invalid phone number format")

# Клас для запису контакту
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # Додавання телефонного номеру
    def add_phone(self, phone):
        existing_phones = [p.value for p in self.phones]
        if phone not in existing_phones:
            self.phones.append(Phone(phone))
        else:
            return "Phone number already exists for this contact."

    # Зміна телефонного номеру
    def change_phone(self, new_phone):
        if len(self.phones) == 0:
            return "No phone numbers found for this contact."
        else:
            self.phones[0].value = new_phone
            return "Phone number updated successfully."

    # Відображення телефонного номеру
    def show_phone(self):
        if len(self.phones) == 0:
            return "No phone numbers found for this contact."
        else:
            return self.phones[0].value

    # Додавання дати народження
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    # Відображення дати народження
    def show_birthday(self):
        if self.birthday:
            return self.birthday.value
        else:
            return "Birthday not set for this contact."

# Клас для адресної книги
class AddressBook(UserDict):
    # Додавання контакту
    @input_error
    def add(self, name, phone):
        if name in self.data:
            return self.data[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.data[name] = record
            return "Contact added successfully."
    
    # Виведення списку контактів
    def list_contacts(self):
        if not self.data:
            return "Address book is empty."
        else:
            contact_list = "Contacts in the address book:\n"
            for name, record in self.data.items():
                contact_list += f"{name}: {record.show_phone()}, {record.show_birthday()}\n"
            return contact_list

    # Зміна телефонного номеру
    @input_error
    def change(self, name, new_phone):
        if name in self.data:
            return self.data[name].change_phone(new_phone)
        else:
            return "Contact not found."

    # Відображення телефонного номеру
    @input_error
    def phone(self, name):
        if name in self.data:
            return self.data[name].show_phone()
        else:
            return "Contact not found."
   
    # Додавання дати народження
    @input_error
    def birthday(self, name, birthday):
        if name in self.data:
            self.data[name].add_birthday(birthday)
            return "Birthday added successfully."
        else:
            return "Contact not found."
        
    # Відображення дати народження
    @input_error
    def s_birthday(self, name):
        if name in self.data:
            return self.data[name].show_birthday()
        else:
            return "Contact not found."

    # Пошук контактів з днями народження на наступному тижні
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

# Головна функція програми
def main():
    address_book = AddressBook()

    print("""Welcome to the Address Book Bot!
    Available commands:
    add [name] [phone]: Add a new contact or a phone number to an existing contact.
    change [name] [new_phone]: Change the phone number for the specified contact.
    phone [name]: Show the phone number for the specified contact.
    birthday [name] [birthday]: Add a birthday for the specified contact.
    s-birthday [name]: Show the birthday for the specified contact.
    birthdays: Show birthdays happening within the next week.
    list: Show all contacts.
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

        elif command.startswith("birthday"):
            _, name, birthday = command.split()
            result = address_book.birthday(name, birthday)
            print(result)

        elif command.startswith("s-birthday"):
            _, name = command.split()
            result = address_book.s_birthday(name)
            print(result)

        elif command == "list":
            print(address_book.list_contacts())

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


