from backend.src.constants import (CONFIG_FILE_PATH, PARAMS_FILE_PATH, FIREBASE_CREDENTIALS_PATH)
from backend.src.storage.chroma_storage import VectorDatabase
from backend.src.config.configuration import ConfigurationManager
from backend.src.llm_models import get_openai_embeddings
from backend.src.llm_models import (get_openai_embeddings, get_openai_model)
from server.services.query_service import QueryService


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
vb_params = config_manager.get_vectordatabase_config()
image_vb = VectorDatabase(vb_params, persist_directory="vector_database/image")
image_chroma = image_vb.init_chromadb(get_openai_embeddings())
image_retriever = image_vb.get_multivector_retriever(image_chroma, id_key="doc_id")



def get_image_query_service():
    query_service = QueryService(get_openai_embeddings(), image_vb)
    return query_service

text_vb = VectorDatabase(vb_params, persist_directory="vector_database/text")
text_chroma = text_vb.init_chromadb(get_openai_embeddings())
text_retriever = text_vb.get_multivector_retriever(text_chroma, id_key="doc_id")


def get_text_query_service():
    query_service = QueryService(get_openai_embeddings(), text_vb)
    return query_service