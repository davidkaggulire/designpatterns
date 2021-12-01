# storage_interface.py

from typing import Tuple
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
    def getFileURL(self, url: str) -> str:
        """gets File path and returns a valid signed url"""

    @abstractmethod
    def copyFile(self, source: str, dest: str) -> Tuple[bool, str]:
        """copies Files"""

    @abstractmethod
    def listFilesInDirectory(self, source: str) -> Tuple[bool, str]:
        """list files"""
    
    @abstractmethod
    def checkIfFileExists(self, source: str) -> Tuple[bool, str]:
        """check if file exists"""

    @abstractmethod
    def createDirectory(self, dir_name: str) -> Tuple[bool, str]:
        """create directory"""

    @abstractmethod
    def deleteDirectory(self, dir_name: str) -> Tuple[bool, str]:
        """delete directory name"""

