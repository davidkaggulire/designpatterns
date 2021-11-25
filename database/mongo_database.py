# patterns.py

from .database_interface import IDatabase
from typing import Dict, Tuple
from pymongo import MongoClient


class MongoNoSQLDatabase(IDatabase):
    def __init__(self) -> None:
        # creating database
        self.db: MongoClient = None
        print(self.db)
        # creating collection
        self.contact = None
        print(self.contact)
        super().__init__()

    def connect(self):
        try:
            client = MongoClient(host="localhost", port=27017)
            # creating database
            self.db = client.patterns
            print(self.db)
            # creating collection
            self.contact = self.db.contact
            print(self.contact)
            print("Connected successfully to MongoDB!!!")
        except Exception:
            print("Could not connect to MongoDB")
        return True

    def disconnect(self):
        self.db.contact.drop()
        # self.db.contact.remove()
        return True

    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"-Creating data in location {location}")

        try:
            result = self.contact.insert_one({"_id": location, "data": data})
            print(result)
            print(f"Data inserted: {result.inserted_id}")
            reason = "Successfully created"
            return True, reason
        except Exception as e:
            reason = (
                f"-Failed to create data in location {location}, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(reason)
            return False, reason

    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        print(f"-Viewing data in location {location}")
        # read data from database
        result = self.contact.find_one({"_id": location})

        if result:
            print(result)
            reason = f"-Data viewed successfully in location {location}"
            print(reason)
            return True, reason, result
        else:
            reason = (
                f"-Failed to read data in location {location} "
            )
            print(reason)
            return False, reason, ""

    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        print(f"-Updating data in location {location}")
        # update data from database
        old_value = self.contact.find_one({"_id": location})
        print(f"old value is {old_value}")

        my_query = {"_id": location}
        new_values = {"$set": {"data": data}}
        read_value = self.contact.find_one(my_query)

        if read_value:
            # update value since it is found
            self.contact.update_one(my_query, new_values)
            reason = f"-Data updated successfully in location {location}"
            updated_value = self.contact.find_one(my_query)
            print(f"updated value is {updated_value}")
            print(reason)
            return True, reason
        else:
            reason = (
                f"-Failed to update data in location {location} "
            )
            print(reason)
            return False, reason

    def delete(self, location: str) -> Tuple[bool, str]:
        print(f"-Deleting data in location {location}")
        my_query = {"_id": location}
        read_value = self.contact.find_one(my_query)

        if read_value:
            print(read_value)
            self.contact.delete_one(my_query)
            reason = f"-Data deleted successfully in location {location}"
            return True, reason
        else:
            reason = (
                f"-Failed to delete data in location {location}"
            )
            print(reason)
            return False, reason
