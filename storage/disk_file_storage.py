# disk_file_storage.py

import uuid
import os
import shutil
from typing import Tuple, List
from .storage_interface import IStorage


class DiskFileStorage(IStorage):

    def __init__(self):
        self.base = "repo"

    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Uploading file...from {source} to {dest}")
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
        print(f"Downloading file ...{source} to {dest}")
        try:
            path = f"{self.base}/{source}"
            shutil.copy(path, dest)
            reason = f"File downloaded to {dest} successfully"
            print(reason)
            return True, reason
        except OSError as e:
            reason = "Failed to download file "+f"Error: {path} : {e.strerror}"
            print(reason)
            return False, reason

    def deleteFile(self, source: str) -> Tuple[bool, str]:
        print(f"Deleting file {source}")
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
        print(f"getting file URL and signing it...{source}")
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
        print(f"Copying File...from {source} to {dest}")
        path = f"{self.base}/{source}"
        dest = f"{self.base}/{dest}"
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
        print(f"Listing files in directory...{source}")
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
        print(f"Checking if file {source} exists...")
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
        print(f"Creating Directory {source}...")
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
        print(f"Deleting Directory...{source}")
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
        print(f"Renaming File....{source} to {dest}")
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
        user_id = uuid.uuid3(uuid.NAMESPACE_DNS, email)
        print(user_id)
        reason = "User Created Successfully"
        print(reason)
        return True, reason

    def signIn(self, email: str, password: str) -> Tuple[bool, str, str]:
        print(f"logging in user...{email}")
        user_id = uuid.uuid3(uuid.NAMESPACE_DNS, email)
        reason = "Sign In Was Successful"
        print(reason)
        print(f"current user is {user_id}")
        return True, user_id, reason
