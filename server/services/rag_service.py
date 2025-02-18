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
from backend.src.utils.common import read_json

firestore = FireStore()
firestore_chat_history = firestore.get_chat_history()

image_summarizer_prompt = read_json("backend/src/prompts/summarizer.json")
image_summarizer_prompt = image_summarizer_prompt["image_summarizer_prompt"]


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
        
    # def image_summarize(self, img_base64_list: List[str]) -> str:
    #     """Summarize multiple images using LLM model API
    #     Args:
    #         img_base64_list: List of base64 encoded images
    #     Returns:
    #         str: summary of images"""
    #     model = get_openai_model()
    #     messages = [
    #         HumanMessage(
    #             content=[
    #                 {"type": "text", "text": image_summarizer_prompt},
    #                 {
    #                     "type": "image_url",
    #                     "image_url": {
    #                         "url": f"data:image/jpg;base64,{img_base64}"
    #                     },
    #                 },
    #             ]
    #         )
    #         for img_base64 in img_base64_list[:3]
    #     ]
    #     combined_messages = "\n".join(
    #     [f"-{model.invoke(msg.content).content}" for msg in messages[:3]]
    #     )
    #     image_summary = []
    #     for msg in messages:
    #         image_summary.append(model.invoke(msg).content)   
    #     print("-0---00"*100)
    #     print("\n".join(image_summary))
    #     time.sleep(40)  
    #     return "\n".join(image_summary)
    
        
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
        # img_base64_list = []
        if "images" in dict["context"] and len(dict["context"]["images"]) > 0:
            for img_b64 in dict["context"]["images"]:
                img_path = self.save_image(img_b64)
                if img_path:
                    image_paths.append(img_path)
            # message_content.append(
            #     self.image_summarize(dict["context"]["images"]))

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
        

        # # to get the text
        query_service = get_text_query_service()
        text_docs = query_service.search_similar_documents(query)
        total_docs.extend(text_docs)
        
        total_docs = get_top_matching_documents(total_docs, query, top_n=12)
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
            | RunnableLambda(lambda x: self.prompt_func_(x))
            | RunnableLambda(lambda result: RAGService.generate_response(model, result))        )
        
        return chain
    
    def get_encoded_images(self, docs: list[Document]):
        img_base64_list = []
        for i in docs:
            img_base64_list.append(i.metadata["raw_string"])
            
        msg = self.image_summarize(img_base64_list)
        return msg
        
    @staticmethod
    def compute_cosine(x):
        total_docs = []
        total_docs.extend(x["images_vb"])
        total_docs.extend(x["text_vb"])
    
        # compute cosine similarity
        total_docs = get_top_matching_documents(total_docs, x["question"], top_n=17)
        return total_docs
    
    def get_chain2(self, query, query_service, model):
        chain = (
            RunnableParallel({
                "context": RunnableParallel({"text_vb": RunnableLambda(lambda _: RAGService.get_text_from_vb(query)),
                                            #  | RunnableLambda(lambda _: self.debug(_)),
                                             "images_vb": RunnableLambda(lambda _: RAGService.get_images_from_vb(query)),
                                             "question": RunnablePassthrough()})
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
        print(len(x))
        print(x)
        # print(x[0].metadata)
        # print(x.keys())
        # print("length of images",len(x["images"]))
        # print("length of text",len(x["texts"]))
        time.sleep(40)
        # print(x["text_metadata"])w
        return x
   
