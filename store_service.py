# file application.py

from typing import Tuple
from storage import IStorage, DiskFileStorage, FirebaseStorage


class FileStorageApp:

    def __init__(self, storage_service_provider: IStorage) -> None:
        self.fs = storage_service_provider

    def setUpSystem(self, data: dict) -> Tuple[bool, str]:
        print("Connecting to file system")
        email = data['email']
        password = data['password']

        login_user, reason = self.fs.signIn(email, password)

        # create user and login when user doesn't exist
        if not login_user:
            created_user, create_reason = self.fs.signUp(email, password)
            print(create_reason)
            login, new_reason = self.fs.signIn(email, password)
        else:
            print(reason)
            return True, reason
        print("File System startup complete")

    def uploadFile(self, data: dict) -> Tuple[bool, str]:
        print("Uploading file...")
        source = data["source"]
        dest = data["dest"]
        uploaded, reason = self.fs.uploadFile(source, dest)

        if not uploaded:
            print(reason)
            reason = "Failed to upload file"
            return False, reason

        reason = "File uploaded successfully"
        print(reason)
        return True, reason

    def downloadFile(self, data: dict) -> Tuple[bool, str]:
        print("Downloading file...")
        source = data["source"]
        dest = data["dest"]
        downloaded, reason = self.fs.downloadFile(source, dest)

        if not downloaded:
            print(reason)
            reason = "Failed to download file"
            return False, reason

        reason = "File downloaded successfully"
        print(reason)
        return True, reason

    def deleteFile(self, data: dict) -> Tuple[bool, str]:
        print("Deleting file")
        source = data["source"]
        deleted, reason = self.fs.deleteFile(source)

        if not deleted:
            print(reason)
            reason = "File not found"
            return False, reason

        reason = "File deleted successfully"
        print(reason)
        return True, reason

    def getFileURL(self, data: dict) -> str:
        print("Signing URL...")
        source = data["source"]
        signed_url = self.fs.getFileURL(source)

        if not signed_url:
            reason = "URL cannot be retrieved"
            return reason

        reason = "URL signed successfully"
        print(reason)
        return signed_url

    def copyFile(self, data: dict) -> Tuple[bool, str]:
        print("Copying file...")
        source = data["source"]
        dest = data["dest"]
        copied_file, reason = self.fs.copyFile(source, dest)

        if not copied_file:
            print(reason)
            reason = "Failed to copy file"
            return False, reason

        reason = "File copied successfully"
        print(reason)
        return True, reason

    def listFilesInDirectory(self, data: dict) -> Tuple[bool, str]:
        #  work in progress
        print("Listing files...")
        source = data["source"]
        list_files, reason, file_list = self.fs.listFilesInDirectory(source)

        if not list_files:
            print(reason)
            reason = "Path to list not found"
            return False, reason, ""

        reason = "Files listed successfully"
        print(reason)
        return True, reason, file_list

    def checkIfFileExists(self, data: dict) -> Tuple[bool, str]:
        print("Checking if file exists...")
        source = data["source"]
        file_exists, reason = self.fs.checkIfFileExists(source)

        if not file_exists:
            print(reason)
            reason = "File not found"
            return False, reason

        reason = "File exists"
        print(reason)
        return True, reason

    def createDirectory(self, data: dict) -> Tuple[bool, str]:
        print("Creating Directory...")
        source = data["source"]
        dir_created, reason = self.fs.createDirectory(source)

        if not dir_created:
            print(reason)
            reason = "Directory exists"
            return False, reason

        reason = "Directory created"
        print(reason)
        return True, reason

    def deleteDirectory(self, data: dict) -> Tuple[bool, str]:
        print("Deleting Directory...")
        source = data["source"]
        dir_deleted, reason = self.fs.deleteDirectory(source)

        if not dir_deleted:
            print(reason)
            reason = "Failed to delete directory"
            return False, reason

        reason = "Directory deleted successfully"
        print(reason)
        return True, reason

    def renameFile(self, data: dict) -> Tuple[bool, str]:
        print("Renaming file...")
        source = data["source"]
        dest = data["dest"]
        file_renamed, reason = self.fs.renameFile(source, dest)

        if not file_renamed:
            print(reason)
            reason = "File not found"
            return False, reason

        reason = "File renamed successfully"
        print(reason)
        return True, reason


# testing
data = {
    "source": "data_download/awesome chords.png",
    "dest": "goodfoot.png"
}

data1 = {
    "source": "hello.png",
    "dest": "data_download/hello.png"
}

# dkaggs123@gmail.com

data2 = {
    "source": "goodfoot.png",
    "dest": "data_download/nowfour.png"
}

data3 = {
    "source": "goodfoot.png",
    "dest": "hello.png"
}

# data for failure
data4 = {
    "source": "fool.png",
    "dest": "data_download/nowfour.png"
}

# download file from cloud to local
data_download = {
    "source": "awesome chords.png",
    "dest": "data_download/cool.png"
}

# directory
data_dir = {
    "source": "music",
    "dest": ""
}

# get URL
url = "awesome chords.png"
data_url = {
    "source": url,
    "dest": ""
}

# rename file -- local storage
source1 = "awesome chords.png"
file_renamed = "goodfoot.png"
data_rename = {
    "source": source1,
    "dest": file_renamed
}

data5 = {
    "source": "data_download/awesome chords.png",
    "dest": "awesome chords.png"
}

# delete data - cloud
data_del = {
    "source": "goodfoot.png",
    "dest": ""
}

user = {
    "email": "dkaggs123@gmail.com",
    "password": "123456789"
}

user2 = {
    "email": "hillzound@gmail.com",
    "password": "123456789"
}

# storage_service = DiskFileStorage()
storage_service = FirebaseStorage()

file_app = FileStorageApp(storage_service)

file_app.setUpSystem(user)

# # operatioms
# file_app.uploadFile(data5)
# file_app.downloadFile(data_download)
# file_app.copyFile(data_download)
# file_app.uploadFile(data)
# file_app.deleteFile(data_del)
# file_app.getFileURL(data_url)
# file_app.checkIfFileExists(data_download)
# file_app.createDirectory(data_dir)
# file_app.listFilesInDirectory(data_dir)
# file_app.deleteDirectory(data_dir)
# file_app.renameFile(data_rename)
