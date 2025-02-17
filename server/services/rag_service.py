from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from backend.src.storage.firebase_storage import FireStore
from server.services.prompt_service import get_system_prompt, get_ror_prompt
from typing import final
import tempfile
import base64
import os
import uuid
from typing import *
from langchain.schema.document import Document
from server.services.vb_service import (get_image_query_service, 
                                           get_text_query_service)
from server.services.cosine_score import get_top_matching_documents
from backend.src.llm_models import get_openai_model
import time
import sys
firestore = FireStore()
firestore_chat_history = firestore.get_chat_history()


class RAGService:
    def __init__(self):
        pass
    
    @final # Prevent method from being overridden
    def get_last_n_messages(self, n:int):
        """
        Retrieve the last 'n' messages from the Firestore database.
        Args:
            n (int): The number of recent messages to retrieve.
        Returns:
            list: A list of the last 'n' messages.
        """
        messages = firestore.load_messages(n)
        return messages
        
    def filter_metadata(self, x: Dict, filters: list = ["filename", "page_number"])-> Dict:
            """
            Filters the metadata dictionary to include only specified keys.
            Args:
                x (Dict): The metadata dictionary to filter.
                filters (list, optional): The list of keys to retain in the filtered dictionary. 
                              Defaults to ["filename", "page_number"].
            Returns:
                Dict: A dictionary containing only the key-value pairs where the key is in the filters list.
            """

            return {k: v for k, v in x.items() if k in filters}
        
    def prompt_func(self, dict):
        """
        Constructs a prompt message for the model based on the provided context and question.
        Args:
            dict (dict): A dictionary containing the context and question. The dictionary should have the following structure:
                {
                    "context": {
                        "texts": [list of text strings],
                        "images": [list of base64 encoded images]
                    },
                    "question": str
                }
        Returns:
            dict: A dictionary containing:
                - "messages" (list): A list of message objects including system messages, past conversation, and the current question with context.
                - "image_paths" (list): A list of file paths to the saved images.
        """
        message_content = []
        meta_data = []
        message_content.append(SystemMessage(content=get_system_prompt()))

        # Get metadata of text
        for i in dict["context"]["texts_metadata"]:
            meta_data.append(self.filter_metadata(i))   
        
        # get teh last conversation messages
        past_conversation = self.get_last_n_messages(5)
        if len(past_conversation) > 0:
            message_content.extend(past_conversation)

        # Add text content if available
        if "texts" in dict["context"] and len(dict["context"]["texts"]) > 0:
            format_texts = "\n".join(dict["context"]["texts"])
            message_content.append(
                HumanMessage(content=f"""Answer the question based only on the following context:
                Question: {dict["question"]}
                
                Text and tables:
                {format_texts}
                """) 
            )
        # save and decode raw image
        image_paths = []
        if "images" in dict["context"] and len(dict["context"]["images"]) > 0:
            for img_b64 in dict["context"]["images"]:
                img_path = self.save_image(img_b64)
                if img_path:
                    image_paths.append(img_path)

        return {"messages": message_content, "image_paths": image_paths,
                "text_metadata": meta_data}
    
    def save_image(self, base64_string):
        """
        Decode a base64 encoded string and save the resulting image to a temporary directory.
        Args:
            base64_string (str): The base64 encoded string representing the image.
        Returns:
            str: The file path of the saved image if successful, None otherwise.
        Raises:
            Exception: If there is an error during the decoding or saving process.
        """
        temp_dir = tempfile.gettempdir()  # Get system temp dir
        img_path = os.path.join(temp_dir, f"image_{uuid.uuid4().hex}.jpg")
        
        try:
            with open(img_path, "wb") as img_file:
                img_file.write(base64.b64decode(base64_string))
            return img_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None 
    
    @staticmethod
    def get_rephrased_question_(query, model):
        prompt = get_ror_prompt()
        prompt = prompt.format(query=query)
        return model.invoke(prompt).content

    # @staticmethod
    # def search_similar_documents_(query_service, query):
    #     return query_service.search_similar_documents(query)

    @staticmethod
    def search_similar_documents_(query) -> List[Document]:
        total_docs = []
        # to get the images
        query_service = get_image_query_service()
        image_docs = query_service.search_similar_documents(query)
        total_docs.extend(image_docs)
        
        # ---> image data= image_docs -> doc["page_content"]
        # del query_service
        # # to get the text
        query_service = get_text_query_service()
        text_docs = query_service.search_similar_documents(query)
        total_docs.extend(text_docs)
        # print(type(total_docs))
        # time.sleep(40)
        
        total_docs = get_top_matching_documents(total_docs, query, top_n=12)
        # print("--DEBUG--"*100)
        # print(len(total_docs))    
        # print("---"*100)
        # print("length of image docs: ", len(text_docs))
        # # print("length of text docs: ", len(text_docs))
        # time.sleep(10)
        # print("image_docs")
        # print(text_docs[0])
        # time.sleep(20)
        # print(text_docs[0].page_content)
        # # sys.exit()
        return total_docs
    
    @staticmethod
    def get_images_from_vb(query):
        query_service = get_image_query_service()
        image_docs = query_service.search_similar_documents(query)
        return image_docs
    
    @staticmethod
    def get_text_from_vb(query):
        query_service = get_text_query_service()
        text_docs = query_service.search_similar_documents(query)
        return text_docs
    

    @staticmethod
    def get_stored_docs_(query_service, context: List[Document]):
        if isinstance(context, list):
            return query_service.get_stored_docs(context)
        else:
            raise TypeError("Expected context to be a dictionary")

    @staticmethod
    def rephrased_question_(query, model):
        return RAGService.get_rephrased_question(query, model)

    def prompt_func_(self, result):
        return self.prompt_func(result)
    
    @staticmethod
    def generate_response(model, result):
        return {
            "response": model.invoke(result["messages"]),  # LLM output
            "image_paths": result["image_paths"],  # Preserve image paths
            "text_metadata": result["text_metadata"]
        }
        
    def get_chain(self, query, query_service, model):
        chain = (
            RunnableParallel({
                "context": RunnableLambda(lambda x: RAGService.search_similar_documents_(query)) # list[document]
                            # RunnableLambda(lambda x: RAGService.search_similar_documents_(query_service, query)) # list[document]
                            # | RunnableLambda(lambda x: self.debug(x))
                            | RunnableLambda(lambda x: RAGService.get_stored_docs_(query_service, x)), # input: dict, 
                "question": RunnableLambda(lambda x: RAGService.get_rephrased_question_(query, model))
            })
            # |  RunnableLambda(lambda x: self.debug(x))
            | RunnableLambda(lambda x: self.prompt_func_(x))
            | RunnableLambda(lambda result: RAGService.generate_response(model, result))
            # |  RunnableLambda(lambda x: self.debug(x))
        )
        
        return chain
    @staticmethod
    def compute_cosine(x):
        total_docs = []
        total_docs.extend(x["text_vb"])
        total_docs.extend(x["images_vb"])
        
        # compute cosine similarity
        get_top_matching_documents(total_docs, x["query"], top_n=5)
        return total_docs
    
    def get_chain2(self, query, query_service, model):
        chain = (
            RunnableParallel({
                "context": RunnableParallel({"text_vb": RunnableLambda(lambda _: RAGService.get_text_from_vb(query)),
                                             "images_vb": RunnableLambda(lambda _: RAGService.get_images_from_vb(query)),
                                             "query": RunnablePassthrough()})
                          | RunnableLambda(lambda x: RAGService.compute_cosine(x)) # list[documents]
                            | RunnableLambda(lambda x: RAGService.get_stored_docs_(query_service, x)), # input: dict, 
                "question": RunnableLambda(lambda _: RAGService.get_rephrased_question_(query, model))
            })
            | RunnableLambda(lambda x: self.prompt_func_(x))
            | RunnableLambda(lambda result: RAGService.generate_response(model, result))
        )
        
        return chain
    
    def debug(self, x):
        print( "***"*100)
        print("This is debug function ")
        print(type(x))
        print(x.keys())
        print(x["text_metadata"])
        return x
   