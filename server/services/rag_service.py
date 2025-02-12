
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


from server.services.query_service import QueryService
from backend.src.storage.chroma_storage import VectorDatabase



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
    
    def prompt_func(self, dict):
        message_content = []

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