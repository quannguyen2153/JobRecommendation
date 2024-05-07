import pyrebase
from .config import FIREBASE_CONFIG

firebase_client = pyrebase.initialize_app(FIREBASE_CONFIG)