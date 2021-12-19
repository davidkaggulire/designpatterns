# test_storage.py

import os
import sys
import pytest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from storage import DiskFileStorage, FirebaseStorage
from store_system import FileStorageApp


user = {
    "email": "dkaggs123@gmail.com",
    "password": "123456789"
}

user2 = {
    "email": "hillzound@gmail.com",
    "password": "123456789"
}


@pytest.fixture
def service(getStorageService):
    storage_app = FileStorageApp(getStorageService)
    storage_app.setUpSystem(user2)
    return storage_app


@pytest.fixture
def sys_name(request):
    service = request.config.getoption("--service")
    return service


@pytest.fixture
def getStorageService(sys_name):
    """return storage service"""
    print(sys_name)
    if sys_name == "cloud":
        return FirebaseStorage()
    elif sys_name == "local":
        return DiskFileStorage()


def test_upload_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    output = service.uploadFile(data)
    expected = (True, 'File uploaded successfully')
    assert output == expected


def test_upload_fail(service):
    data = {
        "source": "data_download/awesome.png",
        "dest": "awesome_chords.png"
    }
    output = service.uploadFile(data)
    expected = (False, 'Failed to upload file')
    assert output == expected


def test_download_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    data_download = {
        "source": "awesome_chords.png",
        "dest": "./repo/system_user/data_download/cool.png"
    }
    service.uploadFile(data)
    output = service.downloadFile(data_download)
    expected = (True, 'File downloaded successfully')
    assert output == expected


def test_download_fail(service):
    data_download = {
        "source": "awesome.png",
        "dest": "data_download/cool.png"
    }
    output = service.downloadFile(data_download)
    expected = (False, 'Failed to download file')
    assert output == expected


def test_delete_file_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "sample.png"
    }

    data_del = {
        "source": "sample.png",
        "dest": ""
    }
    service.uploadFile(data)
    output = service.deleteFile(data_del)
    expected = (True, 'File deleted successfully')
    assert output == expected


def test_delete_file_fail(service):
    data_del = {
        "source": "hello.png",
        "dest": ""
    }
    output = service.deleteFile(data_del)
    expected = (False, 'File not found')
    assert output == expected


def test_get_file_url_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    data_url = {
        "source": "awesome_chords.png",
        "dest": ""
    }
    service.uploadFile(data)
    output = service.getFileURL(data_url)
    assert isinstance(output, str)


def test_get_file_url_fail(service):
    # TO inquire
    data_url = {
        "source": "awesome.png",
        "dest": ""
    }
    expected = "URL cannot be retrieved"
    output = service.getFileURL(data_url)
    assert output == expected


def test_copy_file_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    data_download = {
        "source": "awesome_chords.png",
        "dest": "cool.png"
    }
    service.uploadFile(data)
    output = service.copyFile(data_download)
    expected = (True, 'File copied successfully')
    assert output == expected


def test_copy_file_fail(service):
    data_download = {
        "source": "awesomechords.png",
        "dest": "data_download/cool.png"
    }
    output = service.copyFile(data_download)
    expected = (False, 'Failed to copy file')
    assert output == expected


def test_create_dir_success(service):
    data_dir = {
        "source": "joy",
        "dest": ""
    }
    service.createDirectory(data_dir)
    service.deleteDirectory(data_dir)
    output = service.createDirectory(data_dir)
    expected = (True, 'Directory created')
    assert output == expected


def test_create_dir_fail(service):
    data_dir = {
        "source": "music",
        "dest": ""
    }
    service.createDirectory(data_dir)
    output = service.createDirectory(data_dir)
    expected = (False, 'Directory exists')
    assert output == expected


def test_list_files_dir_success(service):
    data_dir = {
        "source": "music",
        "dest": ""
    }
    service.createDirectory(data_dir)
    output = service.listFilesInDirectory(data_dir)
    expected = (True, 'Files listed successfully', [])
    assert output == expected


def test_list_files_dir_fail(service):
    data_dir = {
        "source": "something",
        "dest": ""
    }
    output = service.listFilesInDirectory(data_dir)
    expected = (False, 'Path to list not found', "")
    assert output == expected


def test_delete_directory_success(service):
    data_dir = {
        "source": "music",
        "dest": ""
    }
    service.createDirectory(data_dir)
    output = service.deleteDirectory(data_dir)
    expected = (True, 'Directory deleted successfully')
    assert output == expected


def test_delete_directory_fail(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "games/football.png"
    }
    data_dir = {
        "source": "games",
        "dest": ""
    }
    service.uploadFile(data)
    output = service.deleteDirectory(data_dir)
    expected = (False, 'Failed to delete directory')
    assert output == expected


def test_rename_file_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    data_rename = {
        "source": "awesome_chords.png",
        "dest": "goodfoot.png"
    }
    service.uploadFile(data)
    output = service.renameFile(data_rename)
    expected = (True, 'File renamed successfully')
    assert output == expected


def test_rename_file_fail(service):
    data_rename = {
        "source": "awesomechords.png",
        "dest": "goodfoot.png"
    }
    output = service.renameFile(data_rename)
    expected = (False, 'File not found')
    assert output == expected


def test_check_file_exists_success(service):
    data = {
        "source": "repo/system_user/data_download/awesome_chords.png",
        "dest": "awesome_chords.png"
    }
    data_download = {
        # "source": "music",
        "source": "awesome_chords.png",
        "dest": "data_download/cool.png"
    }
    service.uploadFile(data)
    output = service.checkIfFileExists(data_download)
    expected = (True, 'File exists')
    assert output == expected


def test_check_file_exists_fail(service):
    data_download = {
        "source": "awesomechords.png",
        "dest": "data_download/cool.png"
    }
    output = service.checkIfFileExists(data_download)
    expected = (False, 'File not found')
    assert output == expected
