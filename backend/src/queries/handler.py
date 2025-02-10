from typing import *
from langchain.schema.document import Document
import numpy as np
import uuid
from base64 import b64decode
from PIL import Image
from IPython.display import display, HTML



class QueryHandler:
    def __init__(self, retriever):
        self.retriever = retriever
        self.docstore = retriever.docstore
        self.vectorstore = retriever.vectorstore
        
    def similarity_search(self, query: str, top_k: int=5):
        return self.retriever.vectorstore.similarity_search(query, top_k)
    
    def relevant_documents(self, query: str, top_k: int=5):
        return self.retriever.get_relevant_documents(query, k=top_k, return_metadata=True)
    
    def query_by_vector(self, vector: np.array, top_k: int=5):
        return self.retriever.query_by_vector(vector, top_k)
    
    def query_by_document(self, document: Document, top_k: int=5):
        return self.retriever.query_by_document(document, top_k)
        
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
                raw_docs.append(i.metadata.get("raw_text", "None"))
            else:
                raw_docs.append(doc)
            i.metadata.pop("raw_text", None)
            meta_data.append(i.metadata)
        return raw_docs, meta_data
    
    def split_image_text_types(self, docs: List[Document]) -> Dict:
    #     ''' Split base64-encoded images and texts '''
        b64 = []
        text = []
        for doc in docs:
            if doc.metadata["type"] == "Image":
                b64.append(self.query_by_id(doc.id))
            elif doc.metadata["type"] == "Text":
                text.append(doc)

        return {
            "images": b64,
            "texts": text
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

if __name__ == "__main__":
    query_handler = QueryHandler(retriever)