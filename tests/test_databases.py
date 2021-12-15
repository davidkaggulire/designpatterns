# test_databases.py

import os
import sys
import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from database import FileSystemDatabase, InMemoryDatabase, MongoNoSQLDatabase, PostgreSQLDatabase
from phone_book import PhoneBookSystem


@pytest.fixture
def db_service(getDatabaseService):
    phone_book_system = PhoneBookSystem(getDatabaseService)
    phone_book_system.setUpSystem()
    return phone_book_system


@pytest.fixture
def db_name(request):
    """return """
    db = request.config.getoption("--db")
    return db


@pytest.fixture
def getDatabaseService(db_name):
    """choose database service"""
    print(db_name)
    if db_name == "inmemory":
        return InMemoryDatabase()
    elif db_name == "filesystem":
        return FileSystemDatabase()
    elif db_name == "postgres":
        return PostgreSQLDatabase()
    elif db_name == "mongo":
        return MongoNoSQLDatabase()


def test_create_contact(db_service):
    name = "David"
    phone = "0787870099"
    data = {"name": name, "phone": phone}
    output = db_service.createContact(data)
    expected = (True, 'Contact created successfully')
    assert output, expected
    db_service.tearDownSystem()


def test_fail_create(db_service):
    name = "David"
    phone = "/home/build/companies.txt"
    data = {"name": name, "phone": phone}
    db_service.createContact(data)
    output = db_service.createContact(data)
    reason = "failed to create contact"
    expected = (False, reason)
    assert output, expected
    db_service.tearDownSystem()


def test_read_contact(db_service):
    name = "David"
    phone = "0787870099"
    data = {"name": name, "phone": phone}
    db_service.createContact(data)
    output = db_service.read_contact(data)
    expected = (True, 'Contact read successfully', data)
    assert output, expected
    db_service.tearDownSystem()


def test_fail_read_contact(db_service):
    name = "David"
    phone = "0787870099"
    phone2 = "0790908765"
    data = {"name": name, "phone": phone}
    data2 = {"name": name, "phone": phone2}
    db_service.createContact(data)
    output = db_service.read_contact(data2)
    expected = (False, 'failed to read contact', "")
    assert output, expected
    db_service.tearDownSystem()


def test_update_contact(db_service):
    name = "David"
    phone = "0787870099"
    data = {"name": name, "phone": phone}
    db_service.createContact(data)
    output = db_service.update_contact(data)
    expected = (True, 'Contact updated successfully')
    assert output, expected
    db_service.tearDownSystem()


def test_fail_update_contact(db_service):
    name = "David"
    phone = "0787870099"
    phone2 = "0790909456"
    data = {"name": name, "phone": phone}
    data2 = {"name": name, "phone": phone2}
    db_service.createContact(data)
    output = db_service.update_contact(data2)
    reason = "failed to update contact"
    expected = (False, reason)
    assert output, expected
    db_service.tearDownSystem()


def test_delete_contact(db_service):
    name = "David"
    phone = "0787870098"
    data = {"name": name, "phone": phone}
    db_service.createContact(data)
    output = db_service.delete_contact(data)
    expected = (True, 'Contact deleted successfully')
    assert output, expected
    db_service.tearDownSystem()


def test_delete_nonexistent_contact(db_service):
    name = "David"
    phone = "0789909878"
    data = {"name": name, "phone": phone}
    output = db_service.delete_contact(data)
    expected = (False, 'failed to delete contact')
    assert output, expected
    db_service.tearDownSystem()
