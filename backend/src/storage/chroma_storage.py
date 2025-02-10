from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings

from typing import *
from dotenv import load_dotenv
import os

from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.config.configuration import ConfigurationManager
from backend.src.extractors.extract import Extractor

load_dotenv()

class VectorDatabase(Extractor):
    def __init__(self, config):
        super(VectorDatabase, self).__init__()
        self.config = config
    
    def init_chromadb(self, embeddings):
        return Chroma(self.config.vectorstore_name, 
                      embeddings, 
                      persist_directory=self.config.persist_directory)
        
    def get_retriever(self, vectorstore, id_key: str="doc_id") -> MultiVectorRetriever:
        store = InMemoryStore()
        return MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=store,
            id_key=id_key
        )
          
    def generate_document(self, data, metadata=None) -> Document:
        if metadata == None:
            metadata = self.generate_unique_id(data)
        documents = [Document(page_content=data_, metadata=metadata_)
                        for data_, metadata_ in zip(data, metadata)]
        return documents
    
    def store_to_vb(self, data: List[Tuple], summaries: List[Document], retriever)->None:
        try:
            retriever.docstore.mset(data)
            retriever.vectorstore.add_documents(summaries)
        except Exception as e:
            print("Error in storing data to vectorbase: ", e)
            raise e
    
    def store_to_vb(self, summaries: List[Document], retriever)->None:
        try:
            retriever.vectorstore.add_documents(summaries)
        except Exception as e:
            print("Error in storing data to vectorbase: ", e)
            raise e
    
    @staticmethod
    def sanity_check_for_metadata(metadata: dict):
        """To check if metadata value has no data structure; if present take 1st value as str"""
        new_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (list, tuple)):
                new_metadata[key] = str(value[0])
            elif isinstance(value, set):
                new_metadata[key] = str(list(value)[0])
            else:
                new_metadata[key] = str(value)
        return new_metadata
    

# unit testing
if __name__ == "__main__":
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    vector_database_config = config_manager.get_vectordatabase_config()
    vector_database = VectorDatabase(vector_database_config)
    vectorstore = vector_database.init_chromadb(embeddings=OpenAIEmbeddings())
    retriever = vector_database.get_retriever(vectorstore)
    print(retriever)