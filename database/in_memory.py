# patterns.py

from .database_interface import IDatabase
from typing import Dict, Tuple


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
