from typing import *
from langchain.schema.document import Document
import numpy as np
from base64 import b64decode
from PIL import Image
from IPython.display import display, HTML
from langchain.retrievers.multi_vector import MultiVectorRetriever
from copy import deepcopy
import io


class QueryHandler:
    def __init__(self, retriever):
        self.retriever = retriever
        self.docstore = retriever.docstore
        self.vectorstore = retriever.vectorstore
        
    def similarity_search(self, query: str, top_k: int=5):
        return self.retriever.vectorstore.similarity_search(query, top_k)
    
    def relevant_documents(self, query: str, top_k: int=5):
        return self.vectorstore.get_relevant_documents(query, k=top_k, return_metadata=True)
    
    def query_by_vector(self, vector: np.array, top_k: int=5):
        return self.vectorstore.query_by_vector(vector, top_k)
    
    def query_by_document(self, document: Document, top_k: int=5):
        return self.vectorstore.query_by_document(document, top_k)
        
    def map_raw_docs(self, vectorstore_results: List[Document]) -> List:
        """To map the raw documents from vectorstore results by using doc_id from metadata
        Args:
            vectorstore_results (List[Document]): results from vectorstore
        Returns:
            List: containing raw documents
        """
        raw_docs = []
        meta_data = []
        for i in vectorstore_results:

            doc_id = i.metadata["doc_id"]
            doc = self.retriever.docstore.__dict__["store"].get(doc_id, "None") # if data is present in InMemoryStore
            if doc == "None":
                raw_docs.append(i.metadata.get("raw_string", "None"))
            else:
                raw_docs.append(doc)
            i.metadata.pop("raw_text", None)
            meta_data.append(i.metadata)
        return raw_docs, meta_data
        
    @staticmethod
    def split_image_text_types(docs: List[Document]) -> Dict:
    #     ''' Split base64-encoded images and texts '''
        docs_ = deepcopy(docs)
        b64, image_metadata = [], []
        text, text_metadata = [], []
        for doc in docs_:
            # print(doc.metadata)
            if doc.metadata["type"] == "image":
                try:
                    raw_string = doc.metadata.pop("raw_string")
                    # print("IMage raw string: ", raw_string)
                    b64.append(raw_string)
                    image_metadata.append(doc.metadata)
                except:
                    b64.append("None")
                    # print("Image append None")
                    image_metadata.append(doc.metadata)
            elif doc.metadata["type"] == "text":
                try:
                    raw_string = doc.metadata.pop("raw_string")
                    # print("text raw string: ", raw_string)
                    text.append(raw_string)
                    text_metadata.append(doc.metadata)
                except:
                    text.append("None")
                    # print("Text append None")
                    text_metadata.append(doc.metadata)
        # print("**"*40)
        # print("before return")
        # print(b64, text)
        # print("**"*40)
        # print(image_metadata, text_metadata)
        # print("**"*40)
        return {
            "images": b64,
            "images_metadata": image_metadata,
            "texts": text,
            "texts_metadata": text_metadata
        }

    @staticmethod
    def plt_img_base64(img_base64):

        # Create an HTML img tag with the base64 string as the source
        image_html = f'<img src="data:image/jpeg;base64,{img_base64}" />'

        # Display the image by rendering the HTML
        display(HTML(image_html))
        
    def plot_img_base64(self, img_base64: str):
        img = Image.open(io.BytesIO(b64decode(img_base64)))
        img.show()
        
    def get_vectorstore_as_retreiever(self) -> MultiVectorRetriever:
        if self.vectorstore == None:
            raise ValueError("Vectorstore is not initialized")
            
        return self.vectorstore.as_retriever()
    

if __name__ == "__main__":
    query_handler = QueryHandler(retriever)