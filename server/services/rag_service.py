
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from backend.src.storage.firebase_storage import FireStore
from server.services.prompt_service import get_system_prompt, get_ror_prompt
from typing import final
import tempfile
import base64
import os
import uuid
from typing import *
from langchain.schema.document import Document

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
        message_content.append(SystemMessage(content=get_system_prompt()))
        
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

        return {"messages": message_content, "image_paths": image_paths}
    
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

    @staticmethod
    def search_similar_documents_(query_service, query):
        return query_service.search_similar_documents(query)

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
            "image_paths": result["image_paths"]  # Preserve image paths
        }
        
    def get_chain(self, query, query_service, model):
        chain = (
            RunnableParallel({
                "context": RunnableLambda(lambda x: RAGService.search_similar_documents_(query_service, query))
                            # | RunnableLambda(lambda x: self.debug(x))
                            | RunnableLambda(lambda x: RAGService.get_stored_docs_(query_service, x)),
                "question": RunnableLambda(lambda x: RAGService.get_rephrased_question_(query, model))
            })
            | RunnableLambda(lambda x: self.prompt_func_(x))
            | RunnableLambda(lambda result: RAGService.generate_response(model, result))
        )
        
        return chain
    
    # def debug(self, x):
    #     print( "***"*100)
    #     print("This is debug function ")
    #     print(type(x))
    #     print(x[0])
    #     if isinstance(x, dict):
    #         print(x.keys())
    #     # print(x)