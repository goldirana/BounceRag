from server.services.chroma_service import VectorDatabase
# from backend.src.extractors.text_summarizer import TextSummarizer
# from backend.src.extractors.image_summarizer import ImageSummarizer
# from backend.src.extractors.data_ingestion import DataIngestion
# from backend.src.extractors.extract import Extractor
from backend.src.entity.config_entity import *
from backend.src.utils.common import read_yaml
from backend.src.storage.firebase_storage import FireStore
from backend.src.config.configuration import ConfigurationManager
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH


from server.services.query_service import QueryService
from server.services.rag_service import RAGService
from backend.src.llm_models import (get_openai_embeddings, get_openai_model)
import os


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
vector_database_config = config_manager.get_vectordatabase_config()
data_ingestion_config = config_manager.get_data_ingestion_params()
# image_summarizer_config = config_manager.get_image_summarizer_params()
# text_summarizer_config = config_manager.get_text_summarizer_params()
firestore_params = config_manager.get_firebase_params()


embeddings = get_openai_embeddings()
config_params = read_yaml(CONFIG_FILE_PATH)
model_name = config_params.model.chat_model
model_temp = config_params.model.temperature

def get_llm_model() -> object:
    model = get_openai_model()
    return model

def get_vector_db(config: VectorDatabaseConfig=vector_database_config) -> object:
    vector_database = VectorDatabase(config)
    return vector_database

# def get_data_ingestion(config: DataIngestionConfig=data_ingestion_config) -> object:
#     data_ingestion = DataIngestion(config)
#     return data_ingestion

# def get_text_summarizer(config: TextSummarizerConfig=text_summarizer_config) -> object:
#     text_summarizer = TextSummarizer(config, get_llm_model())
#     return text_summarizer

# def get_image_summarizer(config: ImageSummarizerConfig=image_summarizer_config) -> object:
#     image_summarizer = ImageSummarizer(config, get_llm_model())
#     return image_summarizer

def get_query_service():
    query_service = QueryService(embeddings, get_vector_db())
    return query_service

def get_rag_service():
    rag_service = RAGService()
    return rag_service

def get_firestore_chat_client():
    firestore = FireStore(firestore_params)
    firestore_chat_history = firestore.get_chat_history()
    return firestore_chat_history

if __name__ == "__main__":
    print(config_params)
    x = get_query_service()
    


