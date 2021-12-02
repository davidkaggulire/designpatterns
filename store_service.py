# store_files.py

from typing import Tuple
from storage import IStorage, DiskFileStorage, FirebaseStorage


class StoreFileService:

    def __init__(self, storage_service_provider: IStorage) -> None:
        self.db = storage_service_provider

    