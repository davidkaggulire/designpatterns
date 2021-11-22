# patterns.py

import os
import json
from typing import Dict, Tuple
from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        """connect database"""

    @abstractmethod
    def disconnect(self):
        """disconnect database"""

    @abstractmethod
    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """creates objects that are saved into the database"""

    @abstractmethod
    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        """views records in database"""

    @abstractmethod
    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """updates record in database"""

    @abstractmethod
    def delete(self, location: str) -> Tuple[bool, str]:
        """deletes record from database"""


class FileSystemDatabase(IDatabase):
    """database provider class"""

    def connect(self):
        self.base_path = "temp"
        return True

    def disconnect(self):
        print("-Disconnecting from FileSystemDatabase")
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """create files"""
        print(f"-Creating data in location {location}")
        try:
            with open(f"{self.base_path}/{location}.json", "w") as file_object:
                json.dump(data, file_object)
                reason = f"-Data created successfully in location {location}"
                print(reason)
                return (True, reason)
        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return (False, reason)

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        """read values from provider"""
        print(f"-Reading data in location {location}")
        results = {}
        path = f"{self.base_path}/{location}.json"

        try:
            with open(path) as f_obj:
                file_data = json.load(f_obj)
                results["output"] = file_data
                reason = "Successfully read"
                print(reason)
                return (True, reason, results)
        except Exception:
            reason = "Read operation failed"
            results["output"] = ""
            print(reason)
            return (False, reason, results)

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """update method"""
        path = f"{self.base_path}/{location}.json"
        try:
            with open(path):
                with open(path, "w") as file_object:
                    json.dump(data, file_object)
                    reason = f"-Data updated successful in location {location}"
                    print(reason)
                    return (True, reason)
        except Exception as e:
            reason = (
                f"-Failed to update data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return (False, reason)

    def delete(self, location: str) -> Tuple[bool, str]:
        """delete method"""
        path = f"{self.base_path}/{location}.json"
        if os.path.exists(path):
            os.remove(path)
            reason = f"-Data deleted successfully in location {location}"
            print(reason)
            return (True, reason)
        else:
            reason = "File not found"
            print(reason)
            return (False, reason)


class InMemoryDatabase(IDatabase):
    def __init__(self) -> None:
        super().__init__()
        self.data = {}

    __instance = None

    @staticmethod
    def get_instance():
        if InMemoryDatabase.__instance is None:
            return InMemoryDatabase()
        return InMemoryDatabase.__instance

    def connect(self):
        print("-Connecting to In Memory Database")
        return True

    def disconnect(self):
        print("-Disconnecting from In Memory Database")
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"-Creating data in location {location}")
        try:
            print(self.data[location])
            reason = "failed to create data in location"
            print(reason)
            return False, reason
        except Exception:
            self.data[location] = data
            print(self.data)
            reason = f"-Data created successfully in location {location}"
            print(reason)
            return True, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        print(f"-Viewing data in location {location}")
        print(self.data)
        # print(self.data[location]["phone"])
        try:
            print(self.data[location]["phone"])
            reason = f"-Data viewed successfully in location {location}"
            print(reason)
            print(self.data)
            return True, reason, self.data
        except Exception as k:
            reason = (
                f"-Failed to read data in location {location}, reason: "
                + f"{type(k).__name__} {str(k)}"
            )
            print(reason)
            return (False, reason, "")

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"-Updating data in location {location}")
        print(self.data)
        try:
            print(self.data[location]["phone"])
            self.data[location] = data
            print(self.data)
            reason = f"-Data updated successfully in location {location}"
            print(reason)
            print(self.data)
            return True, reason
        except Exception as k:
            reason = (
                f"-Failed to update data in location {location}, reason: "
                + f"{type(k).__name__} {str(k)}"
            )
            print(reason)
            return False, reason

    def delete(self, location: str) -> Tuple[bool, str]:
        print(f"-Deleting data in location {location}")
        try:
            self.data.pop(location)
            print(self.data)
            reason = f"-Data deleted successfully in location {location}"
            return True, reason
        except Exception as k:
            reason = (
                f"-Failed to delete data in location {location}, reason: "
                + f"{type(k).__name__} {str(k)}"
            )
            print(reason)
            return False, reason


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
database_service = FileSystemDatabase()

phone_book_system = PhoneBookSystem(database_service)
phone_book_system.setUpSystem()

name = "Person"
phone = "07878700789"
phone2 = "0789001012"

name2 = "Person2"


phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.createContact({"name": name, "phone": phone})
# phone_book_system.read_contact({"name": name, "phone": phone2})
# phone_book_system.read_contact({"name": name, "phone": ""})
# phone_book_system.update_contact({"name": name2, "phone": phone})
phone_book_system.update_contact({"name": name2, "phone": phone2})
# phone_book_system.delete_contact({"name": name2, "phone": phone})
# phone_book_system.delete_contact({"name": name2, "phone": ""})
