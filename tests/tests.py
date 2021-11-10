# tests.py

import os
import sys
import unittest
import json
import stat


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from unittest.mock import patch, mock_open
from patterns import DatabaseProvider

class TestFileProvider(unittest.TestCase):

    def setUp(self) -> None:
        self.db = DatabaseProvider()
        return super().setUp()

    def test_init(self):
        self.assertTrue(self.db.boolean)
        self.assertEqual(self.db.status, "")


    def test_singleton(self):
        """testing singleton pattern"""
        p1 = self.db.get_instance
        p2 = self.db.get_instance
        self.assertEqual(p1, p2)
        self.assertIsNotNone(p1)


    @patch("builtins.open", new_callable=mock_open,
       read_data=json.dumps({'district' : 'Kampala','weather' : "sunny"}))
    def test_create_success(self, mock_file):
        """success test for create operation"""
        file_data = {
                    'district' : 'Kampala',
                    'weather' : "sunny",
                    }
        expected_output = (True, "Create operation successful")
        filename = 'example.json'
        actual_output = self.db.create(filename, file_data)

        # Assert filename is file that is opened
        mock_file.assert_called_with(filename, 'w')
        
        self.assertEqual(expected_output, actual_output)


    @patch("builtins.open", new_callable=mock_open,
       read_data=json.dumps({'district' : 'Kampala','weather' : "sunny"}))
    def test_create_fail(self, mock_file):
        """success test for create operation"""
        file_data = {
                    'district' : 'Kampala',
                    'weather' : "sunny",
                    }
        expected_output = (False, "Create operation failed")
        filename = '/../../../../etc/example.json'
        print("xxxx")
        print(sys)
        # actual_output = self.db.create(filename, file_data)
        # self.assertEqual(expected_output, actual_output)


    @patch("builtins.open", new_callable=mock_open,
       read_data=json.dumps({'district' : 'Kampala','weather' : "sunny"}))
    def test_read_data_success(self, mock_file):
        """success test for read operation"""
        file_data = {
                    'district' : 'Kampala',
                    'weather' : "sunny",
                    }
        expected_output = (True, "Successfully read", {"output": file_data})
        filename = 'example.json'
        actual_output = self.db.read(filename)

        # Assert filename is file that is opened
        mock_file.assert_called_with(filename)

        self.assertEqual(expected_output, actual_output)


    def test_read_data_fail(self):
        """fail test for read operation"""
        expected_output = (False, "Read operation failed", {"output": ""})
        filename = 'read.json'
        actual_output = self.db.read(filename)

        self.assertEqual(expected_output, actual_output)


    @patch("builtins.open", new_callable=mock_open,
       read_data=json.dumps({'district' : 'Kampala','weather' : "sunny"}))
    def test_update_success(self, mock_file):
        """test successful update"""
        file_data = {
                    'district' : 'Kampala',
                    'weather' : "sunny",
                    }
        expected_output = (True, "Successfully updated")
        filename = 'example.json'
        actual_output = self.db.update(filename, file_data)

        # Assert filename is file that is opened
        mock_file.assert_called_with(filename, 'w')
        
        self.assertEqual(expected_output, actual_output)


    def test_delete_nonexistent(self):
        """test deleting file which does not exist"""

        filename = 'example2.json'
        expected_output = (False, "File not found")

        actual_output = self.db.delete(filename)
        self.assertEqual(expected_output, actual_output)


    def test_remove_file(self):
        """test to delete file if it exists"""
        filename = 'example3.json'
        file_data = {
                    'district' : 'Kampala',
                    'weather' : "sunny",
                    }
        expected_output = (True, "Successfully deleted")

        self.db.create(filename, file_data)
        with patch('os.remove'):
            actual_output = self.db.delete(filename)
            self.assertEqual(expected_output, actual_output)


    def tearDown(self) -> None:
        del self.db
        return super().tearDown()