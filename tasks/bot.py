from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)
    
    def validate(self, value):
        return value.isdigit() and len(value) == 10

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Phone not found")

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Phone not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

def parse_input(user_input):
    if not user_input.strip():
        return "", []
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Error: Contact not found."
        except ValueError:
            return "Error: Give me name and phone please."
        except IndexError:
            return "Error: Enter user name."

    return inner

@input_error
def add_contact(args, contacts):
    name, phone = args
    name = name.lower()
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    name, phone = args
    name = name.lower()
    if name not in contacts:
        raise KeyError
    contacts[name] = phone
    return "Contact updated."

@input_error
def show_phone(args, contacts):
    name = args[0].lower()
    if name not in contacts:
        raise KeyError
    return contacts[name]

def show_all(contacts):
    if not contacts:
        return "No contacts stored."
    result = []
    for name, phone in contacts.items():
        result.append(f"{name.capitalize()}: {phone}")
    return "\n".join(result)

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
            if len(args) < 2:
                print("Error: Give me name and phone please.")
            else:
                name = args[0]
                phone = args[1]
                record = book.find(name)
                if record:
                    try:
                        record.add_phone(phone)
                        print("Phone added.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    record = Record(name)
                    try:
                        record.add_phone(phone)
                        book.add_record(record)
                        print("Contact added.")
                    except ValueError as e:
                        print(f"Error: {e}")
        elif command == "change":
            if len(args) < 3:
                print("Error: Give me name, old phone and new phone please.")
            else:
                name = args[0]
                old_phone = args[1]
                new_phone = args[2]
                record = book.find(name)
                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print("Contact updated.")
                    except ValueError as e:
                        print(f"Error: {e}")
                else:
                    print("Error: Contact not found.")
        elif command == "phone":
            if len(args) < 1:
                print("Error: Enter user name.")
            else:
                name = args[0]
                record = book.find(name)
                if record:
                    if record.phones:
                        phones = "; ".join(p.value for p in record.phones)
                        print(phones)
                    else:
                        print("No phones for this contact.")
                else:
                    print("Error: Contact not found.")
        elif command == "all":
            if book.data:
                for name, record in book.data.items():
                    print(record)
            else:
                print("No contacts stored.")
        elif command == "delete":
            if len(args) < 1:
                print("Error: Enter user name.")
            else:
                name = args[0]
                if book.find(name):
                    book.delete(name)
                    print("Contact deleted.")
                else:
                    print("Error: Contact not found.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
     