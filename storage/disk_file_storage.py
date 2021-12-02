# disk_file_storage.py

import os
import shutil
from typing import Tuple
from .storage_interface import IStorage


class DiskFileStorage(IStorage):

    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Uploading file...")
        try:
            shutil.copy(source, dest)
            reason = f"File {source} uploaded to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {source} : {e.strerror}")
            reason = "Failed to upload file"
            print(reason)
            return False, reason

    def downloadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Downloading file ....{source}")
        try:
            shutil.copy(source, dest)
            reason = f"File downloaded to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {source} : {e.strerror}")
            reason = "Failed to download file"
            print(reason)
            return False, reason

    def deleteFile(self, source: str) -> Tuple[bool, str]:
        print("Deleting file...")
        try:
            os.remove(source)
            reason = f"-File {source} deleted successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f'Error: {source} : {e.strerror}')
            reason = "File not found"
            return False, reason

    def getFileURL(self, url: str) -> str:
        print("getting file URL and signing it")
        return url

    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        # using shutil.copy() - doesnt copy metadata else use shutil.copy2()
        print("Copying File...")
        try:
            shutil.copy(source, dest)
            reason = f"File {source} copied to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {source} : {e.strerror}")
            reason = "Failed to copy file"
            print(reason)
            return False, reason

    def listFilesInDirectory(self, source: str) -> Tuple[bool, str]:
        print("Listing files in directory...")
        listed_files = []
        try:
            for entry in os.listdir(source):
                if os.path.isfile(os.path.join(source, entry)):
                    print(entry)
                    listed_files.append(entry)
            print(listed_files)
            reason = f"Successfully listed files in {source}"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {source} : {e.strerror}")
            reason = "Failed to list files"
            print(reason)
            return False, reason

    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        print("Checking if file exists...")
        if os.path.isfile(source):
            reason = f"File {source} exists"
            print(reason)
            return True, reason
        else:
            reason = f'Error: {source} not a valid filename'
            print(reason)
            return False, reason

    def createDirectory(self, dir_name: str) -> Tuple[bool, str]:
        print("Creating Directory...")
        try:
            os.makedirs(dir_name)
            reason = f"Directory {dir_name} created "
            print(reason)
            return True, reason
        except FileExistsError:
            reason = print(f"Directory {dir_name} already exists")
            print(reason)
            return False, reason

    def deleteDirectory(self, dir_name: str) -> Tuple[bool, str]:
        print("Deleting Directory...")
        try:
            os.rmdir(dir_name)
            reason = f"Deleted {dir_name} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f'Error: {dir_name} : {e.strerror}')
            reason = f"Failed to delete directory {dir_name}"
            print(reason)
            return False, reason


hello = DiskFileStorage()
source = "/home/dkaggs/Pictures"
# source = "/home/dkaggs/Pictures/awesome chords.png"
# source = "/home/dkaggs/Pictures/awesome_chords.png"
dest = "/home/dkaggs/Desktop/projects/designpatterns/data_download/"
dir_name = "/home/dkaggs/Music"

# hello.copyFile(source, dest)
# hello.deleteDirectory(dir_name)
hello.checkIfFileExists(source)
