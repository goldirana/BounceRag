
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from backend.src.storage.firebase_storage import FireStore
from typing import final

firestore = FireStore()
firestore_chat_history = firestore.get_chat_history()

class RAGService:
    def __init__(self):
        pass
    
    # def prompt_func(self, dict):
    #     message_content = []

    #     # ✅ Add text content if available
    #     if "texts" in dict["context"] and len(dict["context"]["texts"]) > 0:
    #         format_texts = "\n".join(dict["context"]["texts"])
    #         message_content.append(
    #             HumanMessage(content={"type": "text", "text": f"""Answer the question based only on the following context:
    #             Question: {dict["question"]}

    #             Text and tables:
    #             {format_texts}
    #             """})
    #         )

    #     # ✅ Add image content if available
    #     if "images" in dict["context"] and len(dict["context"]["images"]) > 0:
    #         message_content.append(
    #             HumanMessage(content={"type": "image_url", 
    #                                   "image_url": {"url": f"data:image/jpeg;base64,{dict['context']['images'][0]}"}})
    #         )

    #     print(message_content)  # Debugging: Print what is being sent
    #     return HumanMessage(content=message_content)  # ✅ Single `HumanMessage`
    
    @final
    def get_last_n_messages(self, n:int):
        """Get last n messages from firestore chat history"""
        messages = firestore.load_messages(n)
        return messages

    
    def prompt_func(self, dict):
        message_content = []
        past_conversation = self.get_last_n_messages(5)
        if len(past_conversation) > 0:
            message_content.extend(past_conversation)
        print("----"*200)
        # ✅ Add text content if available
        if "texts" in dict["context"] and len(dict["context"]["texts"]) > 0:
            format_texts = "\n".join(dict["context"]["texts"])
            message_content.append(
                HumanMessage(content=f"""Answer the question based only on the following context:
                Question: {dict["question"]}

                Text and tables:
                {format_texts}
                """)  # ✅ Pass string directly
            )

        # ✅ Add image content if available
        # if "images" in dict["context"] and len(dict["context"]["images"]) > 0:
        #     image_url = f"data:image/jpeg;base64,{dict['context']['images'][0]}"
        #     message_content.append(HumanMessage(content=f"Image URL: {image_url}"))  # ✅ Pass string directly

        print(message_content)  # Debugging: Print what is being sent
        return message_content  # ✅ Return a list of `HumanMessage` objects
    
    def get_chain(self, query, query_service, model):
        chain = (
            RunnableLambda(lambda x: query_service.search_similar_documents(query))
            | RunnableLambda(query_service.get_stored_docs)
            | (lambda context: {"context": context,
                                "question": RunnablePassthrough()})
            | RunnableLambda(self.prompt_func)
            | model
            | StrOutputParser()
        )
        return chain
    

#     def get_chain(self, query, query_service, model):
#         chain = (
#              RunnableParallel(
#                 {""RunnableLambda(lambda x: query_service.search_similar_documents(query))
#                 |RunnableLambda(query_service.get_stored_docs),
#                 RunnableLambda(lambda x: query_service.get_last_n_messages(5))}
#             )
#             | (lambda context: {"context": context,
#                                 "question": RunnablePassthrough()})
#             | RunnableLambda(self.prompt_func)
#             | model
#             | StrOutputParser()
#         )
#         return chain
    
# parallel_chain = RunnableParallel(
#     {
#         "text_result": RunnableLambda(process_text),
#         "image_result": RunnableLambda(process_image),
#     }
# )