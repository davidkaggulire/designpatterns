# test_storage.py

import os
import sys
import unittest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from storage import DiskFileStorage, FirebaseStorage
from store_service import FileStorageApp


user = {
    "email": "dkaggs123@gmail.com",
    "password": "123456789"
}

class TestStorageSystem(unittest.TestCase):

    
    def setUp(self) -> None:
        storage_service = self.getStorageService()
        self.storage_app = FileStorageApp(storage_service)
        self.storage_app.setUpSystem(user)
        return super().setUp()

    def getStorageService(self):
        # raise NotImplementedError("Child class is not supplying db")
        return DiskFileStorage()
        # return FirebaseStorage()

    def test_upload_success(self):
        data = {
            "source": "data_download/awesome chords.png",
            "dest": "awesome chords.png"
        }
        output = self.storage_app.uploadFile(data)
        expected = (True, 'File uploaded successfully')
        self.assertEqual(output, expected)

    def test_download_success(self):
        data_download = {
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.downloadFile(data_download)
        expected = (True, 'File downloaded successfully')
        self.assertEqual(output, expected)

    def test_delete_success(self):
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

    def test_get_file_url_success(self):
        data_url = {
            "source": "awesome chords.png",
            "dest": ""
        }
        output = self.storage_app.getFileURL(data_url)
        expected = data_url["source"]
        self.assertEqual(output, expected)

    def test_copy_file_success(self):
        data_download = {
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.copyFile(data_download)
        expected = (True, 'File copied successfully')
        self.assertEqual(output, expected)

    def test_create_dir_success(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        self.storage_app.deleteDirectory(data_dir)
        output = self.storage_app.createDirectory(data_dir)
        expected = (True, 'Directory created')
        self.assertEqual(output, expected)

    def test_list_files_dir(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        self.storage_app.createDirectory(data_dir)
        output = self.storage_app.listFilesInDirectory(data_dir)
        expected = (True, 'Files listed successfully', [])
        self.assertEqual(output, expected)

    def test_delete_directory(self):
        data_dir = {
            "source": "music",
            "dest": ""
        }
        output = self.storage_app.deleteDirectory(data_dir)
        expected = (True, 'Directory deleted successfully')
        self.assertEqual(output, expected)

    def test_rename_file(self):
        data_rename = {
            "source": "awesome chords.png",
            "dest": "goodfoot.png"
        }
        output = self.storage_app.renameFile(data_rename)
        expected = (True, 'File renamed successfully')
        self.assertEqual(output, expected)

    def test_check_file_exists(self):
        data_download = {
            "source": "awesome chords.png",
            "dest": "data_download/cool.png"
        }
        output = self.storage_app.checkIfFileExists(data_download)
        expected = (True, 'File exists')
        self.assertEqual(output, expected)