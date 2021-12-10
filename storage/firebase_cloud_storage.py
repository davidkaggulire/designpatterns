# google_cloud_storage /firebase cloud storage

import os
import pyrebase
from datetime import datetime, timedelta
from typing import Tuple, List
from .storage_interface import IStorage
from dotenv import load_dotenv 


load_dotenv()

config = {
    "apiKey": os.environ.get('apiKey'),
    "authDomain": os.environ.get('authDomain'),
    "projectId": os.environ.get('projectId'),
    "storageBucket": os.environ.get('storageBucket'),
    "messagingSenderId": os.environ.get('messagingSenderId'),
    "appId": os.environ.get('appId'),
    "measurementId": os.environ.get('measurementId'),
    "serviceAccount": os.environ.get('serviceAccount'),
    "databaseURL": os.environ.get('databaseURL'),
}


class FirebaseStorage(IStorage):

    def __init__(self):
        firebase = pyrebase.initialize_app(config)
        self.storage = firebase.storage()
        # create authentication
        self.auth = firebase.auth()
        # setting base folder
        self.base = "repo"

    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Uploading file....")
        if self.auth.current_user is None:
            reason = "User should login first"
            print(reason)
            return False, reason
        else:
            user_id = self.auth.current_user["localId"]
            print(f"user_id is {user_id}")

            try:
                self.storage.child(f"{self.base}/{user_id}/{dest}").put(source)
                reason = "Upload successful"
                print(reason)
                return True, reason
            except Exception as e:
                print(f"Error: {source} : {e}")
                reason = "Failed to upload"
                print(reason)
                return False, reason

    def downloadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Downloading file ....{source}")
        if self.auth.current_user is not None:
            try:
                user_id = self.auth.current_user["localId"]
                print(user_id)
                path = f"{self.base}/{user_id}/{source}"
                self.storage.child(path).download(dest)

                reason = "Download successful"
                print(reason)
                return True, reason
            except Exception as e:
                print(f"Error: {source} : {e}")
                reason = "Failed to download file"
                print(reason)
                return False, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def deleteFile(self, source: str) -> Tuple[bool, str]:
        print("Deleting file...")
        if self.auth.current_user is not None:
            try:
                user_id = self.auth.current_user["localId"]
                self.storage.delete(f"{self.base}/{user_id}/{source}")
                reason = "File deleted successfully"
                print(reason)
                return True, reason
            except Exception as e:
                print(f"Error: {source} : {e}")
                reason = "Failed to delete file"
                print(reason)
                return False, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def getFileURL(self, source: str) -> str:
        print("getting file URL and signing it...")
        if self.auth.current_user is not None:
            
            user_id = self.auth.current_user["localId"]
            bucket = self.storage.bucket
            blob = bucket.blob(f"{self.base}/{user_id}/{source}")

            file_exists = blob.exists()
            if file_exists:

                encryption_key = datetime.now() + timedelta(days=10000)
                signed_url = blob.generate_signed_url(encryption_key)
                print(f"SignedURL is {signed_url}")
                return signed_url
            else:
                print(f"Path not found")
                reason = "URL cannot be retrieved"
                print(reason)
                return reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Copying File....")
        if self.auth.current_user is not None:
            source_bucket = self.storage.bucket
            user_id = self.auth.current_user["localId"]
            path = f"{self.base}/{user_id}/{source}"
            blob = source_bucket.blob(path)
            dest = f"{self.base}/{user_id}/{dest}"
            dest_bucket = self.storage.bucket

            try:
                print(blob)
                source_bucket.copy_blob(blob, dest_bucket, new_name=dest)
                reason = "file copied successfully"
                print(reason)
                return True, reason

            except Exception as e:
                print(f"failed to copy {e}")
                reason = "Failed to copy file"
                print(reason)
                return False, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def listFilesInDirectory(self, source: str) -> Tuple[bool, str, List[str]]:
        print("Listing files in directory...")
        if self.auth.current_user is not None:
            user_id = self.auth.current_user["localId"]
            dir_files = []
            path = f"{self.base}/{user_id}/{source}"
            bucket = self.storage.bucket
            
            list_files = bucket.list_blobs(prefix=path)
            new_list = list(list_files)

            if len(new_list) > 0:
                for sample in new_list:
                    if sample.name.endswith(".file"):
                        print(f"{sample} to be ignored")
                    else:
                        dir_files.append(sample)

                reason = f"Files in {source} listed"
                print(reason)
                print(dir_files)
                return True, reason, dir_files
            else:
                print(f"Error: Path not found")
                reason = f"Cannot list files in {source}"
                print(reason)
                return False, reason, ""
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        print("Checking if file exists...")
        if self.auth.current_user is not None:
            bucket = self.storage.bucket
            user_id = self.auth.current_user["localId"]
            source = f"{self.base}/{user_id}/{source}"
            blob = bucket.blob(source)
            file_exists = blob.exists()
            print(file_exists)
            if file_exists:
                reason = f"File {source} exists"
                print(reason)
                return True, reason
            else:
                reason = f"File {source} doesn't exist"
                print(reason)
                return False, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def createDirectory(self, source: str) -> Tuple[bool, str]:
        print("Creating Directory...")
        if self.auth.current_user is not None:
            user_id = self.auth.current_user["localId"]
            bucket = self.storage.bucket
            new_path = f"{self.base}/{user_id}/{source}"
            list_files = bucket.list_blobs(prefix=new_path)

            new_list = list(list_files)
            print(new_list)

            if len(new_list):
                print("Error: Directory exists")
                reason = "Failed to create directory"
                print(reason)
                return False, reason
                
            else:
                empty_dir = ".file"
                path = f"{self.base}/{user_id}/{source}/{empty_dir}"
                self.storage.child(path).put("data_download/.file")
                reason = f"Directory {source} created"
                print(reason)
                return True, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def deleteDirectory(self, source: str) -> Tuple[bool, str]:
        print("Deleting Directory...")
        print(f"Deleting source {source}")
        if self.auth.current_user is not None:
            user_id = self.auth.current_user["localId"]
            bucket = self.storage.bucket
            path = f"{self.base}/{user_id}/{source}"
            check_list = []

            blobs = bucket.list_blobs(prefix=path)
            new_list = list(blobs)
            for sample in new_list:
                if sample.name.endswith(".file"):
                    print(f"{sample} cannot be added")
                else:
                    check_list.append(sample)
                    print(f"list is {check_list}")

            print(f"list is {check_list}")
            length_blobs = len(check_list)
            print(f"directory has {length_blobs} files.")
            if len(check_list) > 0:
                reason = "Folder not empty"
                print(reason)
                return False, reason
            else:
                for val in new_list:
                    val.delete()
                    print(f"Directory deleted successfully {val}")
                reason = f"Deleted {path} successfully"
                print(reason)
                return True, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def renameFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print("Renaming File...")
        if self.auth.current_user is not None:
            try:
                user_id = self.auth.current_user["localId"]
                bucket = self.storage.bucket
                source = f"{self.base}/{user_id}/{source}"
                blob = bucket.blob(source)

                dest = f"{self.base}/{user_id}/{dest}"

                new_blob = bucket.rename_blob(blob, dest)
                print(f"File {blob.name} has been renamed to {new_blob.name}")
                reason = "File renamed successfully"
                print(reason)
                return True, reason
            except Exception as e:
                print(f"Error: {e}")
                reason = "File not found"
                print(reason)
                return False, reason
        else:
            reason = "User should login first"
            print(reason)
            return False, reason

    def signUp(self, email: str, password: str) -> Tuple[bool, str]:
        """method to signup user"""
        print(f"Creating user...{email}")
        try:
            # authenticate the user
            self.auth.create_user_with_email_and_password(email, password)
            reason = "User Created Successfully"
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {e}")
            reason = "failed to create user"
            print(reason)
            return False, reason

    def signIn(self, email: str, password: str) -> Tuple[bool, str]:
        """signin created user"""
        print(f"logging in user...{email}")
        try:
            self.auth.sign_in_with_email_and_password(email, password)
            reason = "Sign In Was Successful"
            print(self.auth.current_user)
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {e}")
            reason = "failed to signin user"
            print(reason)
            return False, reason