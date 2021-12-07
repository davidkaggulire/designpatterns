# storage_interface.py

from typing import Tuple, List
from abc import ABC, abstractmethod


class IStorage(ABC):

    @abstractmethod
    def uploadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        """uploads file"""

    @abstractmethod
    def downloadFile(self, source: str, dest: str) -> Tuple[bool, str]:
        """downloads file"""

    @abstractmethod
    def deleteFile(self, source: str) -> Tuple[bool, str]:
        """deletes file"""

    @abstractmethod
    def getFileURL(self, source: str) -> str:
        """gets File path and returns a valid signed url"""

    @abstractmethod
    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        """copies Files"""

    @abstractmethod
    def listFilesInDirectory(self, source: str) -> Tuple[bool, str, List[str]]:
        """list files"""

    @abstractmethod
    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        """check if file exists"""

    @abstractmethod
    def createDirectory(self, source: str) -> Tuple[bool, str]:
        """create directory"""

    @abstractmethod
    def deleteDirectory(self, source: str) -> Tuple[bool, str]:
        """delete directory name"""

    @abstractmethod
    def renameFile(self, source: str, dest: str) -> Tuple[bool, str]:
        """renames a file"""

    @abstractmethod
    def signUp(self, email: str, password: str) -> Tuple[bool, str]:
        """signs up user"""

    @abstractmethod
    def signIn(self, email: str, password: str) -> Tuple[bool, str]:
        """signs up user"""
