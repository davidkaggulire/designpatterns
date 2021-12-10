# test_storage.py

import os
import sys
import unittest
import argparse


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from storage import DiskFileStorage, FirebaseStorage
from store_service import FileStorageApp


user = {
    "email": "dkaggs123@gmail.com",
    "password": "123456789"
}

user2 = {
    "email": "hillzound@gmail.com",
    "password": "123456789"
}


class TestStorageSystem(unittest.TestCase):

    def setUp(self) -> None:
        storage_service = self.getStorageService()
        self.storage_app = FileStorageApp(storage_service)
        self.storage_app.setUpSystem(user2)
        return super().setUp()

    def parsed_args(args):
        """
        parse command line arguments needed for Kafka
        """
        parser = argparse.ArgumentParser(description="Send and receive messages using Kafka CLI")
        parser.add_argument('command', choices=['local', 'cloud'], help="Parse in either local or cloud")
        args = parser.parse_args(args)
        return vars(args)


    # def getStorageService(self, parsed_args):
    def getStorageService(self):
        # args = parsed_args(sys.argv[1:])

        # flag = args['command']

        # flag = "local"
        # if flag == "cloud":
        #     return FirebaseStorage()    
        # else:
        #     return DiskFileStorage()
        # return DiskFileStorage()
        return FirebaseStorage()


    def test_upload_success(self):
        data = {
            "source": "data_download/awesome chords.png",
            "dest": "awesome chords.png"
        }
        output = self.storage_app.uploadFile(data)
        expected = (True, 'File uploaded successfully')
        self.assertEqual(output, expected)

    def test_upload_fail(self):
        data = {
            "source": "data_download/awesome.png",
            "dest": "awesome chords.png"
        }
        output = self.storage_app.uploadFile(data)
        expected = (False, 'Failed to upload file')
        self.assertEqual(output, expected)

    def test_download_success(self):
        data_download = {
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.downloadFile(data_download)
        expected = (True, 'File downloaded successfully')
        self.assertEqual(output, expected)

    def test_download_fail(self):
        data_download = {
            "source": "awesome.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.downloadFile(data_download)
        expected = (False, 'Failed to download file')
        self.assertEqual(output, expected)

    def test_delete_file_success(self):
        data = {
            "source": "data_download/awesome chords.png",
            "dest": "goodfoot.png"
        }

        data_del = {
            "source": "goodfoot.png",
            "dest": ""
        }
        self.storage_app.uploadFile(data)
        output = self.storage_app.deleteFile(data_del)
        expected = (True, 'File deleted successfully')
        self.assertEqual(output, expected)

    def test_delete_file_fail(self):
        data_del = {
            "source": "hello.png",
            "dest": ""
        }
        output = self.storage_app.deleteFile(data_del)
        expected = (False, 'File not found')
        self.assertEqual(output, expected)

    def test_get_file_url_success(self):
        # TO inquire
        data_url = {
            "source": "awesome chords.png",
            "dest": ""
        }
        output = self.storage_app.getFileURL(data_url)
        self.assertIsInstance(output, str)

    def test_get_file_url_fail(self):
        # TO inquire
        data_url = {
            "source": "awesome.png",
            "dest": ""
        }
        expected = "URL cannot be retrieved"
        output = self.storage_app.getFileURL(data_url)
        self.assertEqual(output, expected)

    def test_copy_file_success(self):
        data_download = {
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.copyFile(data_download)
        expected = (True, 'File copied successfully')
        self.assertEqual(output, expected)

    def test_copy_file_fail(self):
        data_download = {
            "source": "awesomechords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.copyFile(data_download)
        expected = (False, 'Failed to copy file')
        self.assertEqual(output, expected)

    def test_create_dir_success(self):
        data_dir = {
            "source": "joy",
            "dest": ""
        }
        self.storage_app.createDirectory(data_dir)
        self.storage_app.deleteDirectory(data_dir)
        output = self.storage_app.createDirectory(data_dir)
        expected = (True, 'Directory created')
        self.assertEqual(output, expected)

    def test_create_dir_fail(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        self.storage_app.createDirectory(data_dir)
        output = self.storage_app.createDirectory(data_dir)
        expected = (False, 'Directory exists')
        self.assertEqual(output, expected)

    def test_list_files_dir_success(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        self.storage_app.createDirectory(data_dir)
        output = self.storage_app.listFilesInDirectory(data_dir)
        expected = (True, 'Files listed successfully', [])
        self.assertEqual(output, expected)

    def test_list_files_dir_fail(self):
        data_dir = {
            "source": "something",
            "dest": ""
        }
        output = self.storage_app.listFilesInDirectory(data_dir)
        expected = (False, 'Path to list not found', "")
        self.assertEqual(output, expected)

    def test_delete_directory_success(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        self.storage_app.createDirectory(data_dir)
        output = self.storage_app.deleteDirectory(data_dir)
        expected = (True, 'Directory deleted successfully')
        self.assertEqual(output, expected)

    def test_delete_directory_fail(self):
        data = {
            "source": "data_download/awesome chords.png",
            "dest": "games/football.png"
        }
        data_dir = {
            "source": "games",
            "dest": ""
        }
        self.storage_app.uploadFile(data)
        output = self.storage_app.deleteDirectory(data_dir)
        expected = (False, 'Failed to delete directory')
        self.assertEqual(output, expected)

    def test_rename_file_success(self):
        data_rename = {
            "source": "awesome chords.png",
            "dest": "goodfoot.png"
        }
        output = self.storage_app.renameFile(data_rename)
        expected = (True, 'File renamed successfully')
        self.assertEqual(output, expected)

    def test_rename_file_fail(self):
        data_rename = {
            "source": "awesomechords.png",
            "dest": "goodfoot.png"
        }
        output = self.storage_app.renameFile(data_rename)
        expected = (False, 'File not found')
        self.assertEqual(output, expected)

    def test_check_file_exists_success(self):
        data = {
            "source": "data_download/awesome chords.png",
            "dest": "awesome chords.png"
        }
        data_download = {
            # "source": "music",
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        self.storage_app.uploadFile(data)
        output = self.storage_app.checkIfFileExists(data_download)
        expected = (True, 'File exists')
        self.assertEqual(output, expected)

    def test_check_file_exists_fail(self):
        data_download = {
            "source": "awesomechords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.checkIfFileExists(data_download)
        expected = (False, 'File not found')
        self.assertEqual(output, expected)
