from backend.src.storage.firebase_storage import FireStore
from backend.src.config.configuration import ConfigurationManager
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, FIREBASE_CREDENTIALS_PATH


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH, FIREBASE_CREDENTIALS_PATH)
firestore_params = config_manager.get_firebase_params()

def get_firestore():
    return FireStore(firestore_params)