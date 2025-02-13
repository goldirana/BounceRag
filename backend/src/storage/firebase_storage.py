from backend.src.config.configuration import ConfigurationManager
from backend.src.entity.config_entity import FireStoreConfig
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
firestore_params = config_manager.get_firebase_params()


class FireStore:
    def __init__(self, config: FireStoreConfig=firestore_params):
        if config == None:
            self.config = config
        self.config = config
            
    def get_firestore_client(self):
        if not firebase_admin._apps: 
            cred = credentials.Certificate(self.config.firebase_credentials_path)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    
    def get_chat_history(self):
        chat_history=FirestoreChatMessageHistory(
            session_id=self.config.session_id,
            collection="chat_history",
            client=self.get_firestore_client()
        )
        return chat_history
        
    def load_messages(self, limit=5)-> list:
        chat_history=self.get_chat_history()
        return chat_history.messages[-limit:]
    
    def add_user_message(self,chat_history, human_message, ai_message) -> None:
        chat_history.add_user_message(human_message)
        chat_history.add_ai_message(ai_message)