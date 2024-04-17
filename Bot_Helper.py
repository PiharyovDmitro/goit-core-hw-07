import re
from datetime import datetime, timedelta
from collections import UserDict

class Field:
    """Базовий клас для полів."""
    def __init__(self, value):
        """Ініціалізує об'єкт полів."""
        self.value = value

class Name(Field):
    """Клас для імені контакту."""
    pass

class Phone(Field):
    """Клас для телефонного номера."""
    def validate(self):
        """Перевіряє правильність формату телефонного номера."""
        if not re.match(r'^\d{10}$', self.value):
            raise ValueError("Invalid phone number format")

class Birthday(Field):
    """Клас для дня народження."""
    def __init__(self, value):
        """Ініціалізує об'єкт дня народження."""
        try:
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    """Клас для запису контакту."""
    def __init__(self, name):
        """Ініціалізує об'єкт запису контакту."""
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """Додає телефонний номер до запису контакту."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє телефонний номер з запису контакту."""
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        """Змінює телефонний номер в записі контакту."""
        if old_phone not in [p.value for p in self.phones]:
            raise ValueError("Phone number {} not found in the record.".format(old_phone))
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                p.validate()
                break

    def add_birthday(self, birthday):
        """Додає день народження до запису контакту."""
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        """Повертає телефонний номер з запису контакту."""
        return next((p for p in self.phones if p.value == phone), None)

class AddressBook(UserDict):
    """Клас для адресної книги."""
    def add_record(self, record):
        """Додає запис контакту до адресної книги."""
        self.data[record.name.value] = record

    def delete_record(self, name):
        """Видаляє запис контакту з адресної книги."""
        del self.data[name]

    def get_upcoming_birthdays(self):
        """Повертає список майбутніх днів народження."""
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
        """Повертає день народження для вказаного контакту."""
        record = self.data.get(name)
        if record and record.birthday:
            return record.birthday.value.strftime('%d.%m.%Y')
        return f'Birthday not found for {name}'

    def get_next_week_birthdays(self):
        """Повертає список днів народження на наступному тижні."""
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
    """Клас для керування контактами."""
    def __init__(self):
        """Ініціалізує об'єкт керування контактами."""
        self.address_book = AddressBook()

    def add_contact(self, name, phone):
        """Додає контакт."""
        record = self.address_book.get(name)
        if record:
            record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.address_book.add_record(record)
        return 'Contact added.'

    def add_birthday(self, name, birthday):
        """Додає день народження до контакту."""
        record = self.address_book.get(name)
        if record:
            record.add_birthday(birthday)
            return 'Birthday added to contact.'
        return f'Contact with name "{name}" not found.'

    def change_contact(self, name, old_phone, new_phone):
        """Змінює телефонний номер контакту."""
        record = self.address_book.get(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return 'Contact updated.'
        return f'Contact with name "{name}" not found.'

    def show_phone(self, name):
        """Показує телефонний номер контакту."""
        record = self.address_book.get(name)
        if record:
            return '\n'.join([p.value for p in record.phones])
        return f'Contact with name "{name}" not found.'

    def show_all_contacts(self):
        """Показує всі контакти."""
        if self.address_book.data:
            all_contacts = 'All contacts:\n'
            for record in self.address_book.data.values():
                all_contacts += f'{record.name.value}: {", ".join([p.value for p in record.phones])}\n'
            return all_contacts
        return 'No contacts saved.'

    def upcoming_birthdays(self):
        """Показує майбутні дні народження."""
        upcoming_birthdays = self.address_book.get_upcoming_birthdays()
        if upcoming_birthdays:
            return '\n'.join([f'{name}: {birthday.strftime("%d.%m.%Y")}' for name, birthday in upcoming_birthdays])
        return "No upcoming birthdays."

    def next_week_birthdays(self):
        """Показує дні народження на наступному тижні."""
        next_week_birthdays = self.address_book.get_next_week_birthdays()
        if next_week_birthdays:
            return '\n'.join([f'{name}: {birthday.strftime("%d.%m.%Y")}' for name, birthday in next_week_birthdays])
        return "No users to greet next week."

class AssistantBot:
    """Клас для взаємодії з користувачем."""
    def __init__(self):
        """Ініціалізує об'єкт асистента."""
        self.contact_manager = ContactManager()
        self.commands = {
            'add': self.contact_manager.add_contact,
            'change': self.contact_manager.change_contact,
            'phone': self.contact_manager.show_phone,
            'all': self.contact_manager.show_all_contacts,
            'add-birthday': self.contact_manager.add_birthday,
            'show-birthday': self.contact_manager.address_book.get_birthday,
            'birthdays': self.contact_manager.next_week_birthdays,
            'hello': lambda: 'How can I help you?',
            'close': lambda: 'Good bye!'
        }

    def greet(self):
        """Привітання користувача."""
        print("Welcome to the assistant bot!")

    def parse_input(self, user_input):
        """Розбиває введену команду на окремі частини."""
        return user_input.strip().lower().split(maxsplit=2)

    def run(self):
        """Запускає основний цикл програми."""
        self.greet()
        print("""Available commands:
- add [name] [phone]: Add or update a contact with the given name and phone number.
- change [name] [old phone] [new phone]: Change phone number for the specified contact.
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

            if command in self.commands:
                if len(args) == 1 or len(args) == 2:
                    print(self.commands[command](*args))
                elif len(args) == 3 and command == 'change':
                    print(self.commands[command](*args))
                else:
                    print("Invalid command format.")
            else:
                print("Invalid command.")

if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()

