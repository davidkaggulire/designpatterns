# patterns.py


from typing import Dict, Tuple
from database import FileSystemDatabase, IDatabase, InMemoryDatabase, MongoNoSQLDatabase, PostgreSQLDatabase


class PhoneBookSystem:
    # # System set up

    def __init__(self, db_service_provider: IDatabase) -> None:
        self.db = db_service_provider

    def setUpSystem(self) -> None:
        print("Starting up system")
        self.db.connect()
        print("System startup complete")

    # # End of system setup

    # # System functionality
    def createContact(self, data: dict) -> Tuple[bool, str]:
        print("Creating contact")

        phone = data["phone"]

        created, reason = self.db.create(phone, data)
        if not created:
            print(reason)
            reason = "failed to create contact"
            return False, reason

        reason = "Contact created successfully"
        print(reason)
        return True, reason

    def read_contact(self, data: dict) -> Tuple[bool, str, Dict[str, str]]:
        print("Viewing contact information")
        phone = data["phone"]

        read, reason, output = self.db.read(phone)
        if not read:
            print(reason)
            reason = "failed to read contact"
            return False, reason, ""

        reason = "Contact read successfully"
        print(reason)
        return True, reason, data

    def update_contact(self, data: Dict[str, str]) -> Tuple[bool, str]:
        print("Updating contact")
        phone = data["phone"]
        print(phone)
        updated, reason = self.db.update(phone, data)
        print(reason)
        if not updated:
            print(reason)
            reason = "failed to update contact"
            return False, reason

        reason = "Contact updated successfully"
        print(reason)
        return True, reason

    def delete_contact(self, data: Dict[str, str]) -> Tuple[bool, str]:
        print("Deleting contact information")

        phone = data["phone"]
        deleted, reason = self.db.delete(phone)

        if not deleted:
            print(reason)
            reason = "failed to delete contact"
            return False, reason

        reason = "Contact deleted successfully"
        print(reason)
        return True, reason
    # # End of system functionality

    # # System tear down
    def tearDownSystem(self) -> None:
        print("Shutting down system")
        self.db.disconnect()
        print("System shut down complete")


# database_service = InMemoryDatabase()
# database_service = FileSystemDatabase()
database_service = PostgreSQLDatabase()
# database_service = MongoNoSQLDatabase()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

name = "Person"
phone = "0787870078"
phone2 = "0789001012"

name2 = "Person2"


phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.read_contact({"name": name, "phone": phone2})
phone_book_system.read_contact({"name": name, "phone": phone})
phone_book_system.update_contact({"name": name, "phone": phone})
# phone_book_system.update_contact({"name": name2, "phone": phone})
# phone_book_system.read_contact({"name": name, "phone": phone})
# phone_book_system.delete_contact({"name": name, "phone": phone})
# phone_book_system.delete_contact({"name": name2, "phone": ""})
