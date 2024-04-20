from collections import defaultdict, UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super.__init__(value)
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) == 10 and value.isdigit():
            self.__value = value
        else:
            raise ValueError("Invalid phone number.")
        
class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, format : "%d.%m.%Y").date()
            super.__init__(value)
        except ValueError:
             raise ValueError('Invalid date format. Use MM.DD.YYYY')
        
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_number(self, phone_number):
        self.phones = [p for p in self.phones if str(p) != phone_number]

    def edit_phone(self, value):
        pass

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    def __str__(self):
        return f"Contact name : {self.name.value}, phones: {';'.join(p.value for p in self.phones)}"
    
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        pass

    def find_next_birthday(self, weekday):
        pass
    
    def get_upcoming_birthday(self, days = 7):
        pass

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


@input_error
def add_contact(args, book : AddressBook):
    name , phone, *_ = args
    record = book.find(name)
    massage = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        massage = "Contact added."
    if phone:
        record.add_phone(phone)
    return massage

@input_error
def change_contact(args, book : AddressBook):
    pass

@input_error
def show_phone(args, book : AddressBook):
    pass

@input_error
def show_all(book : AddressBook):
    pass

@input_error
def add_birthday(args, book):
    pass

@input_error
def show_birthday(args, book):
    pass

@input_error
def birthdays(args, book):
    pass

def parse_input(user_input):
    pass


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            pass

        elif command == "phone":
            pass

        elif command == "all":
            pass

        elif command == "add-birthday":
            pass

        elif command == "show-birthday":
            pass

        elif command == "birthdays":
            pass

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()