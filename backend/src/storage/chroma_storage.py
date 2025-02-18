from langchain_chroma import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.schema.document import Document
from langchain_openai import OpenAIEmbeddings
from zipfile import ZipFile
from typing import *
from dotenv import load_dotenv
import os
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.config.configuration import ConfigurationManager
from backend.src.extractors.extract import Extractor
from backend.exception import *


load_dotenv()

class VectorDatabase(Extractor):
    def __init__(self, config, persist_directory:str=None, collection_name: str=None):
        super(VectorDatabase, self).__init__()
        self.config = config
        self.vectorstore = None
        if persist_directory != None:
            self.config.persist_directory = persist_directory
        if collection_name != None:
            self.config.vectorstore_name = collection_name
    
    @log_error(StorageError, failure_message="Error while initializing ChromaDB")
    def init_chromadb(self, embeddings):
        """
        Initializes a Chroma database with the given embeddings.
        Args:
            embeddings: The embeddings to be used for initializing the Chroma database.
        Returns:
            Chroma: An instance of the Chroma database initialized with the provided embeddings.
        """
        
        return Chroma(self.config.vectorstore_name, 
                      embeddings, 
                      persist_directory=self.config.persist_directory)
    
    @log_error(StorageError, failure_message="Error while initializing MultiVectorRetriever")
    def get_multivector_retriever(self, vectorstore, id_key: str="doc_id") -> MultiVectorRetriever:
        """
        Retrieves a MultiVectorRetriever instance.
        Args:
            vectorstore: The vector store to be used by the retriever.
            id_key (str): The key to be used for document identification. Defaults to "doc_id".
        Returns:
            MultiVectorRetriever: An instance of MultiVectorRetriever configured with the provided vectorstore and an in-memory document store.
        """
        
        store = InMemoryStore()
        return MultiVectorRetriever(
            vectorstore=vectorstore,
            docstore=store,
            id_key=id_key
        )
    
    @log_error(DataIngestionError, failure_message="Error while generating unique id")
    def generate_document(self, data, metadata=None) -> Document:
        """
        Generates a list of Document objects from the provided data and metadata.
        Args:
            data (list): A list of page content strings.
            metadata (list, optional): A list of metadata dictionaries corresponding to each page content. 
                                       If None, unique metadata will be generated for each page content.
        Returns:
            list: A list of Document objects with the provided or generated metadata.
        """
        
        if metadata == None:
            metadata = self.generate_unique_id(data)
        documents = [Document(page_content=data_, metadata=metadata_)
                        for data_, metadata_ in zip(data, metadata)]
        return documents

    log_error(StorageError, failure_message="Error while performing sanity check on metadata before storage")
    def sanity_check_for_metadata(metadata: dict):
        """
        Perform a sanity check on the metadata dictionary to ensure all values are strings.
        This function iterates through the provided metadata dictionary and converts any 
        non-string values to strings. If a value is a list, tuple, or set, the first element 
        of the collection is taken and converted to a string. If the value is already a string 
        or any other type, it is directly converted to a string.
        Args:
            metadata (dict): The metadata dictionary to be checked and sanitized.
        Returns:
            dict: A new dictionary with all values converted to strings.
        """
        
        new_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (list, tuple)):
                new_metadata[key] = str(value[0])
            elif isinstance(value, set):
                new_metadata[key] = str(list(value)[0])
            else:
                new_metadata[key] = str(value)
        return new_metadata
    
    @log_error(StorageError, failure_message="Error while adding data to vectorbase")
    def store_to_vb(self, summaries: List[Document], retriever)->None:
        """
        Stores a list of document summaries to the vector base using the provided retriever.
        Args:
            summaries (List[Document]): A list of document summaries to be stored.
            retriever: An object that provides access to the vector store.
        Raises:
            Exception: If there is an error while storing data to the vector base.
        """
        try:
            retriever.vectorstore.add_documents(summaries)
        except Exception as e:
            print("Error in storing data to vectorbase: ", e)
            raise e

    @log_error(StorageError, failure_message="Error while compressing database")
    def zip_vector_database(self) -> None:
        """
        Compresses the contents of the directory specified by `self.config.persist_directory` 
        into a zip file. The zip file is created in the same location with the same name 
        as the directory, but with a .zip extension.
        This method walks through the directory tree, adding each file to the zip archive.
        Returns:
            None
        """
        with ZipFile(self.config.persist_directory + ".zip", 'w') as zipf:
            for root, dirs, files in os.walk(self.config.persist_directory):
                for file in files:
                    zipf.write(os.path.join(root, file))
                    
    @log_error(StorageError, failure_message="Error while unzipping vectorbase")
    def unzip_vectorbase(self, extract_to) -> None:
        """
        Extracts the contents of a zipped vector base file to the specified directory.
        Args:
            extract_to (str): The directory where the contents of the zip file will be extracted.

        Returns:
            None
        """

        with ZipFile(self.config.persist_directory + ".zip", 'r') as zip_ref:
            zip_ref.extractall(extract_to)

    @log_error(StorageError, failure_message="Error while loading vectorbase as retriever")
    def get_vectorstore_as_retreiever(self, vectorstore) -> MultiVectorRetriever:  
        """
        Converts the given vector store into a MultiVectorRetriever.
        Args:
            vectorstore: The vector store to be converted.
        Returns:
            MultiVectorRetriever: The retriever object created from the vector store.
        """
        return vectorstore.as_retriever()
    

# Unit testing
if __name__ == "__main__":
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    vector_database_config = config_manager.get_vectordatabase_config()
    vector_database = VectorDatabase(vector_database_config)
    vectorstore = vector_database.init_chromadb(embeddings=OpenAIEmbeddings())
    retriever = vector_database.get_retriever(vectorstore)
    print(retriever)