# patterns.py

from typing import Dict, Tuple
from abc import ABC, abstractmethod


class IDatabase(ABC):

    @abstractmethod
    def connect(self):
        """connect database"""

    @abstractmethod
    def disconnect(self):
        """disconnect database"""

    @abstractmethod
    def create(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """creates objects that are saved into the database"""

    @abstractmethod
    def read(self, location: str) -> Tuple[bool, str, Dict[str, str]]:
        """views records in database"""

    @abstractmethod
    def update(self, location: str, data: Dict[str, str]) -> Tuple[bool, str]:
        """updates record in database"""

    @abstractmethod
    def delete(self, location: str) -> Tuple[bool, str]:
        """deletes record from database"""
