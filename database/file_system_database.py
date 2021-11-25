# patterns.py

import os
import json
from .database_interface import IDatabase
from typing import Dict, Tuple


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
