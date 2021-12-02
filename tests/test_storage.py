# test_storage.py

import os
import sys
import unittest


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from storage import DiskFileStorage, FirebaseStorage
from store_service import StoreFileService