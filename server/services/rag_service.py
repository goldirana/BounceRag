
from langchain.schema.messages import HumanMessage, SystemMessage, AIMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from backend.src.storage.firebase_storage import FireStore
from server.services.prompt_service import get_system_prompt
from typing import final
import tempfile
import base64
import os
import uuid


firestore = FireStore()
firestore_chat_history = firestore.get_chat_history()


class RAGService:
    def __init__(self):
        pass
    
    
    @final # to prevent from 
    def get_last_n_messages(self, n:int):
        """Get last n messages from firestore chat history"""
        messages = firestore.load_messages(n)
        return messages
        
    def prompt_func(self, dict):
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
        """Decode base64 and save image to temp directory"""
        temp_dir = tempfile.gettempdir()  # Get system temp dir
        img_path = os.path.join(temp_dir, f"image_{uuid.uuid4().hex}.jpg")
        
        try:
            with open(img_path, "wb") as img_file:
                img_file.write(base64.b64decode(base64_string))
            return img_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None 
    
    def get_chain(self, query, query_service, model):
        """Modified RAG chain to preserve image paths"""
        chain = (
            RunnableLambda(lambda x: query_service.search_similar_documents(query))
            | RunnableLambda(query_service.get_stored_docs)
            | (lambda context: {"context": context, "question": RunnablePassthrough()})
            | RunnableLambda(self.prompt_func)
            | RunnableLambda(lambda result: {
                "response": model.invoke(result["messages"]),  # LLM output
                "image_paths": result["image_paths"]  # Preserve image paths
            })
        )
        return chain