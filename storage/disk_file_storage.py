# disk_file_storage.py

import uuid
import os
import shutil
from typing import Tuple, List
from .storage_interface import IStorage


class DiskFileStorage(IStorage):

    def __init__(self):
        user_id = uuid.uuid3(uuid.NAMESPACE_DNS, "david")
        print(user_id)
        self.base = f"repo/{user_id}"

    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Uploading file...")
        print(self.base)
        dest = f"{self.base}/{dest}"
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
            path = f"{self.base}/{source}"
            shutil.copy(path, dest)
            reason = f"File downloaded to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {path} : {e.strerror}")
            reason = "Failed to download file"
            print(reason)
            return False, reason

    def deleteFile(self, source: str) -> Tuple[bool, str]:
        path = f"{self.base}/{source}"
        print(f"Deleting file...{path}")

        try:
            os.remove(path)
            reason = f"-File {path} deleted successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f'Error: {path} : {e.strerror}')
            reason = "File not found"
            return False, reason

    def getFileURL(self, source: str) -> str:
        print("getting file URL and signing it")
        path = f"{self.base}/{source}"
        if os.path.isfile(path):
            reason = f"File {path} exists"
            print(reason)
            return source
        else:
            print(f'Error: {path} not a valid filename')
            reason = "URL cannot be retrieved"
            return reason

    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        # using shutil.copy() - doesnt copy metadata else use shutil.copy2()
        print("Copying File...")
        path = f"{self.base}/{source}"
        try:
            shutil.copy(path, dest)
            reason = f"File {path} copied to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f"Error: {path} : {e.strerror}")
            reason = "Failed to copy file"
            print(reason)
            return False, reason

    def listFilesInDirectory(self, source: str) -> Tuple[bool, str, List[str]]:
        print("Listing files in directory...")
        path = f"{self.base}/{source}"
        listed_files = []
        try:
            for entry in os.listdir(path):
                if os.path.isfile(os.path.join(path, entry)):
                    print(entry)
                    listed_files.append(entry)
            print(listed_files)
            reason = f"Successfully listed files in {path}"
            print(reason)
            return True, reason, listed_files
        except OSError as e:
            print(f"Error: {path} : {e.strerror}")
            reason = "Failed to list files"
            print(reason)
            return False, reason, ""

    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        print("Checking if file exists...")
        path = f"{self.base}/{source}"
        if os.path.isfile(path):
            reason = f"File {path} exists"
            print(reason)
            return True, reason
        else:
            reason = f'Error: {path} not a valid filename'
            print(reason)
            return False, reason

    def createDirectory(self, source: str) -> Tuple[bool, str]:
        print("Creating Directory...")
        path = f"{self.base}/{source}"
        try:
            os.makedirs(path)
            reason = f"Directory {path} created "
            print(reason)
            return True, reason
        except Exception:
            reason = print(f"Directory {path} already exists")
            print(reason)
            return False, reason

    def deleteDirectory(self, source: str) -> Tuple[bool, str]:
        print("Deleting Directory...")
        path = f"{self.base}/{source}"
        try:
            os.rmdir(path)
            reason = f"Deleted {path} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            print(f'Error: {path} : {e.strerror}')
            reason = f"Folder {path} not empty"
            print(reason)
            return False, reason

    def renameFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Renaming File....")
        path = f"{self.base}/{source}"
        dest = f"{self.base}/{dest}"
        try:
            os.rename(path, dest)
            reason = f"File {path} renamed successfully"
            print(reason)
            return True, reason

        except OSError as e:
            print(f'Error: {e.strerror}')
            reason = f"Failed to rename {path}"
            print(reason)
            return False, reason

    def signUp(self, email: str, password: str) -> Tuple[bool, str]:
        print(f"Creating user...{email}")
        reason = "User Created Successfully"
        print(reason)
        return True, reason

    def signIn(self, email: str, password: str) -> Tuple[bool, str]:
        print(f"logging in user...{email}")
        reason = "Sign In Was Successful"
        print(reason)
        return True, reason
