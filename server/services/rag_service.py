from backend.src.queries.handler import QueryHandler
from langchain.schema import Document
from backend.src.extractors.text_summarizer import TextSummarizer
from backend.src.extractors.image_summarizer import ImageSummarizer
from server.dependencies import *


text_summarizer = get_text_summarizer()
image_summarizer = get_image_summarizer()


class RAGService:
    pass