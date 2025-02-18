from backend.src.config.configuration import ConfigurationManager
from backend.src.entity.config_entity import FireStoreConfig
import firebase_admin
from firebase_admin import credentials, firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from typing import *
from backend.exception import *


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
firestore_params = config_manager.get_firebase_params()


class FireStore:
    def __init__(self, config: FireStoreConfig=firestore_params):
        if config == None:
            self.config = config
        self.config = config
    
    @log_error(AuthenticationError, failure_message="Authentication failed")
    def get_firestore_client(self) -> firestore.client:
        """
        Initializes and returns a Firestore client.
        This method checks if there are any existing Firebase apps initialized. 
        If not, it initializes a new Firebase app using the credentials provided 
        in the configuration. It then returns a Firestore client instance.
        Returns:
            google.cloud.firestore.Client: An instance of the Firestore client.
        """
        if not firebase_admin._apps: 
            cred = credentials.Certificate(self.config.firebase_credentials_path)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    
    @log_error(AuthenticationError, failure_message="Error while getting chat history")
    def get_chat_history(self) -> FirestoreChatMessageHistory:
        """
        Retrieve the chat history from Firestore.
        This method initializes a FirestoreChatMessageHistory object using the session ID
        from the configuration and the Firestore client, and returns it.
        Returns:
            FirestoreChatMessageHistory: An object representing the chat history.
        """

        chat_history=FirestoreChatMessageHistory(
            session_id=self.config.session_id,
            collection="chat_history",
            client=self.get_firestore_client()
        )
        return chat_history
    

    def load_messages(self, limit:int=5)-> List:
        """
        Load a limited number of messages from the chat history.
        Args:
            limit (int, optional): The number of most recent messages to load. Defaults to 5.
        Returns:
            list: A list of the most recent messages, limited by the specified number.
        """

        chat_history=self.get_chat_history()
        return chat_history.messages[-limit:]
    
    @log_error(AuthenticationError, failure_message="Error while adding user message")
    def add_user_message(self,chat_history: object, human_message: str, ai_message: str) -> None:
        """
        Adds a human message and an AI message to the chat history.
        Args:
            chat_history: An object that manages the chat history.
            human_message: The message from the human user.
            ai_message: The message from the AI.
        Returns:
            None
        """
        chat_history.add_user_message(human_message)
        chat_history.add_ai_message(ai_message)