# test_databases.py

import os
import sys
import unittest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database import FileSystemDatabase, InMemoryDatabase, MongoNoSQLDatabase, PostgreSQLDatabase
from phone_book import PhoneBookSystem


class TestPhoneBookSystem(unittest.TestCase):

    def setUp(self) -> None:
        database_service = self.getDatabaseService()
        self.phone_book_system = PhoneBookSystem(database_service)
        self.phone_book_system.setUpSystem()
        return super().setUp()

    def getDatabaseService(self):
        # raise NotImplementedError("Child class is not supplying db")
        # return InMemoryDatabase()
        # return FileSystemDatabase()
        return PostgreSQLDatabase()
        # return MongoNoSQLDatabase()

    def test_create_contact(self):
        name = "David"
        phone = "0787870099"
        data = {"name": name, "phone": phone}
        output = self.phone_book_system.createContact(data)
        expected = (True, 'Contact created successfully')
        self.assertEqual(output, expected)

    def test_fail_create(self):
        name = "David"
        phone = "/home/build/companies.txt"
        data = {"name": name, "phone": phone}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.createContact(data)
        reason = "failed to create contact"
        expected = (False, reason)
        self.assertEqual(output, expected)

    def test_read_contact(self):
        name = "David"
        phone = "0787870099"
        data = {"name": name, "phone": phone}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.read_contact(data)
        expected = (True, 'Contact read successfully', data)
        self.assertEqual(output, expected)

    def test_fail_read_contact(self):
        name = "David"
        phone = "0787870099"
        phone2 = "0790908765"
        data = {"name": name, "phone": phone}
        data2 = {"name": name, "phone": phone2}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.read_contact(data2)
        expected = (False, 'failed to read contact', "")
        self.assertEqual(output, expected)

    def test_update_contact(self):
        name = "David"
        phone = "0787870099"
        data = {"name": name, "phone": phone}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.update_contact(data)
        expected = (True, 'Contact updated successfully')
        self.assertEqual(output, expected)

    def test_fail_update_contact(self):
        name = "David"
        phone = "0787870099"
        phone2 = "0790909456"
        data = {"name": name, "phone": phone}
        data2 = {"name": name, "phone": phone2}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.update_contact(data2)
        reason = "failed to update contact"
        expected = (False, reason)
        self.assertEqual(output, expected)

    def test_delete_contact(self):
        name = "David"
        phone = "0787870098"
        data = {"name": name, "phone": phone}
        self.phone_book_system.createContact(data)
        output = self.phone_book_system.delete_contact(data)
        expected = (True, 'Contact deleted successfully')
        self.assertEqual(output, expected)

    def test_delete_nonexistent_contact(self):
        name = "David"
        phone = "0789909878"
        data = {"name": name, "phone": phone}
        output = self.phone_book_system.delete_contact(data)
        expected = (False, 'failed to delete contact')
        self.assertEqual(output, expected)

    def tearDown(self) -> None:
        self.phone_book_system.tearDownSystem()
        return super().tearDown()

# class TestInMemoryProvider(TestPhoneBookSystem):

#     def getDatabaseService(self) -> None:
#         return InMemoryDatabase()


# class TestFileSystemProvider(TestPhoneBookSystem):

#     def getDatabaseService(self) -> None:
#         database_service = FileSystemDatabase()
#         self.phone_book_system = PhoneBookSystem(database_service)
#         self.phone_book_system.setUpSystem()
#         return super().setUp()


# class TestMongoProvider(TestPhoneBookSystem):

#     def getDatabaseService(self) -> None:
#         database_service = MongoNoSQLDatabase()
#         self.phone_book_system = PhoneBookSystem(database_service)
#         self.phone_book_system.setUpSystem()
#         return super().setUp()
