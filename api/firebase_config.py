import firebase_admin
import os
from dotenv import load_dotenv
from firebase_admin import credentials
from logger import logger
load_dotenv()
def initialize_firebase():
    cred = credentials.Certificate(os.getenv("FIREBASE_KEYFILE_PATH"))
    firebase_admin.initialize_app(cred)
    logger.info("🔥 Firebase app initialized 🔥")

