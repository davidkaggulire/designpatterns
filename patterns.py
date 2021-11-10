# patterns.py

import os
import json
from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def create():
        """creates objects that are saved into the database"""

    @abstractmethod
    def read():
        """views records in database"""

    @abstractmethod
    def update():
        """updates record in database"""

    @abstractmethod
    def delete():
        """deletes record from database"""


class DatabaseProvider(IDatabase):
    """database provider class"""

    __instance = None

    @staticmethod
    def get_instance():
        if DatabaseProvider.__instance is None:
            return DatabaseProvider()
        return DatabaseProvider.__instance

    def __init__(self, boolean=True, status=""):
        self.boolean = boolean
        self.status = status

    def create(self, location, data):
        """create files"""
        try:
            with open(location, 'w') as file_object:
                json.dump(data, file_object)
                self.status = "Create operation successful"
        except Exception:
            self.status = "Create operation failed"
            self.boolean = False

        return (self.boolean, self.status)

    def read(self, location):
        """read values from provider"""

        results = {}
        try:
            with open(location) as f_obj:
                file_data = json.load(f_obj)
                results["output"] = file_data
                self.status = "Successfully read"
        except Exception:
            self.status = "Read operation failed"
            self.boolean = False
            results["output"] = ""

        read_result = (self.boolean, self.status, results)
        return read_result

    def update(self, location, data):
        """update method"""

        try:
            with open(location, 'w') as file_object:
                json.dump(data, file_object)
                self.status = "Successfully updated"
        except Exception:
            self.status = "Update operation failed"
            self.boolean = False

        update_result = (self.boolean, self.status)
        return update_result

    def delete(self, location):
        """delete method"""
        if os.path.exists(location):
            os.remove(location)
            self.status = "Successfully deleted"
        else:
            self.status = "File not found"
            self.boolean = False

        delete_output = (self.boolean, self.status)
        return delete_output
