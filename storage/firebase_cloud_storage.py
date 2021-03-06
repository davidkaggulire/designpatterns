# google_cloud_storage /firebase cloud storage

from firebase_admin import credentials, initialize_app, storage
from firebase_admin import auth
import os
from datetime import datetime, timedelta
from typing import Tuple, List
import requests
import json
import firebase_admin
from .storage_interface import IStorage
from dotenv import load_dotenv


load_dotenv()

config = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')


class FirebaseStorage(IStorage):

    def __init__(self):
        cred = credentials.Certificate(config)

        bucket_name = {
            'storageBucket': os.environ.get('storageBucket')
        }
        try:
            firebase_admin.get_app()
        except ValueError:
            initialize_app(cred, bucket_name)

        self.api_key = os.environ.get('apiKey')

        # setting base folder
        self.base = "repo"

    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Uploading file....{source} to {dest}")
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"{self.base}/{dest}")
            blob.upload_from_filename(source)
            reason = "Upload successful"
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {source} : {e}")
            reason = "Failed to upload"
            print(reason)
            return False, reason

    def downloadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Downloading file ....{source} to {dest}")
        try:
            path = f"{self.base}/{source}"
            bucket = storage.bucket()
            blob = bucket.blob(path)
            blob.download_to_filename(dest)

            reason = "Download successful"
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {dest} : {e}")
            reason = "Failed to download file"
            print(reason)
            return False, reason

    def deleteFile(self, source: str) -> Tuple[bool, str]:
        print(f"Deleting file...{source}")
        try:
            source = f"{self.base}/{source}"
            bucket = storage.bucket()
            blob = bucket.blob(source)
            blob.delete()
            reason = "File deleted successfully"
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {source} : {e}")
            reason = "Failed to delete file"
            print(reason)
            return False, reason

    def getFileURL(self, source: str) -> str:
        print(f"getting file URL and signing it...{source}")
        bucket = storage.bucket()
        blob = bucket.blob(f"{self.base}/{source}")

        file_exists = blob.exists()
        if file_exists:
            encryption_key = datetime.now() + timedelta(days=10000)
            signed_url = blob.generate_signed_url(encryption_key)
            print(f"SignedURL is {signed_url}")
            return signed_url
        else:
            print("Path not found")
            reason = "URL cannot be retrieved"
            print(reason)
            return reason

    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Copying File...{source} to {dest}")
        source_bucket = storage.bucket()
        path = f"{self.base}/{source}"
        blob = source_bucket.blob(path)
        dest = f"{self.base}/{dest}"
        dest_bucket = storage.bucket()

        try:
            print(blob)
            source_bucket.copy_blob(blob, dest_bucket, dest)
            reason = "file copied successfully"
            print(reason)
            return True, reason

        except Exception as e:
            print(f"failed to copy {e}")
            reason = "Failed to copy file"
            print(reason)
            return False, reason

    def listFilesInDirectory(self, source: str) -> Tuple[bool, str, List[str]]:
        print(f"Listing files in directory...{source}")
        dir_files = []
        path = f"{self.base}/{source}"
        bucket = storage.bucket()

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
            print("Error: Path not found")
            reason = f"Cannot list files in {source}"
            print(reason)
            return False, reason, ""

    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        print(f"Checking if file exists...{source}")
        if self.current_user is not None:
            bucket = storage.bucket()
            source = f"{self.base}/{source}"
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
        print(f"Creating Directory...{source}")
        bucket = storage.bucket()
        new_path = f"{self.base}/{source}"
        list_files = bucket.list_blobs(prefix=new_path)

        new_list = list(list_files)
        print(new_list)

        if len(new_list):
            print(f"Error: Directory {new_path} exists")
            reason = "Failed to create directory"
            print(reason)
            return False, reason

        else:
            empty_dir = ".file"
            path = f"{self.base}/{source}/{empty_dir}"

            # file_name is the location of file on local disk
            file_name = "repo/system_user/data_download/.file"
            blob = bucket.blob(path)
            blob.upload_from_filename(file_name)
            reason = f"Directory {source} created"
            print(reason)
            return True, reason

    def deleteDirectory(self, source: str) -> Tuple[bool, str]:
        print(f"Deleting Directory...{source}")
        bucket = storage.bucket()
        path = f"{self.base}/{source}"
        check_list = []

        blobs = bucket.list_blobs(prefix=path)
        new_list = list(blobs)
        for sample in new_list:
            if sample.name.endswith(".file"):
                print(f"{sample} cannot be added")
            else:
                check_list.append(sample)

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

    def renameFile(self, source: str, dest: str) -> Tuple[bool, str]:
        print(f"Renaming File...{source} to {dest}")

        try:
            bucket = storage.bucket()
            source = f"{self.base}/{source}"
            blob = bucket.blob(source)

            dest = f"{self.base}/{dest}"

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

    def signUp(self, email: str, password: str) -> Tuple[bool, str]:
        """method to signup user"""
        print(f"Creating user...{email}")
        try:
            # authenticate the user
            # self.auth.create_user_with_email_and_password(email, password)
            auth.create_user(email=email, password=password)
            reason = "User Created Successfully"
            print(reason)
            return True, reason
        except Exception as e:
            print(f"Error: {e}")
            reason = "failed to create user"
            print(reason)
            return False, reason

    def signIn(self, email: str, password: str) -> Tuple[bool, str, str]:
        """signin created user"""
        print(f"logging in user...{email}")
        try:
            # self.auth.sign_in_with_email_and_password(email, password)
            request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.api_key)
            headers = {"content-type": "application/json; charset=UTF-8"}
            data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
            request_object = requests.post(request_ref, headers=headers, data=data)
            # raise_detailed_error(request_object)
            self.current_user = request_object.json()

            reason = "Sign In Was Successful"
            # print(self.current_user)
            print(reason)
            user_id = self.current_user['localId']
            print(f"current user is {user_id}")
            return True, user_id, reason
        except Exception as e:
            print(f"Error: {e}")
            reason = "failed to signin user"
            print(reason)
            return False, "", reason
