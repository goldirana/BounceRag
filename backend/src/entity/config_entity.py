from dataclasses import dataclass
from typing import *

"""
This module defines configuration entities using dataclasses for various components of the project.
Classes:
    DataIngestionConfig: Configuration for data ingestion process.
    VectorDatabaseConfig: Configuration for vector database.
    PromptConfig: Configuration for prompt settings.
    ImageSummarizerConfig: Configuration for image summarization.
    TextSummarizerConfig: Configuration for text summarization.
    FireStoreConfig: Configuration for Firestore settings.
Attributes:
    DataIngestionConfig.raw (str): Path to raw PDF files.
    DataIngestionConfig.reports (str): Path to processed reports.
    DataIngestionConfig.metadata (list): Metadata to collect from raw PDF elements.
    
    VectorDatabaseConfig.vectorstore_name (str): Name of the vector store.
    VectorDatabaseConfig.persist_directory (str): Directory to persist vector store data.
    
    PromptConfig.prompt_dir (str): Directory for prompt files.
    PromptConfig.system_message_prompt (str): System message prompt.
    
    ImageSummarizerConfig.model (str): Name of the model used for image summarization.
    ImageSummarizerConfig.image_summary_dir (str): Directory to save image summaries.
    ImageSummarizerConfig.summarizer_prompt_dir (str): Directory for summarizer prompts.
    
    TextSummarizerConfig.model (str): Name of the model used for text summarization.
    TextSummarizerConfig.text_summary_dir (str): Directory to save text summaries.
    TextSummarizerConfig.summarizer_prompt_dir (str): Directory for summarizer prompts.
    TextSummarizerConfig.text_summarizer_prompt (str): Prompt for text summarization.
    
    FireStoreConfig.firebase_credentials_path (str): Path to Firebase credentials.
    FireStoreConfig.session_id (str): Session ID for Firestore.
"""



@dataclass
class DataIngestionConfig:
    raw: str # raw pdf path
    reports: str # processed reports path
    metadata: list # metadata to collect from raw_pdf_elements
    
@dataclass
class VectorDatabaseConfig:
    vectorstore_name: str
    persist_directory: str

@dataclass
class PromptConfig:
    prompt_dir: str
    system_message_prompt: str
    

@dataclass
class ImageSummarizerConfig:
    model: str # name of model
    image_summary_dir: str # image summaries directory
    summarizer_prompt_dir: str
    
@dataclass 
class TextSummarizerConfig:
    model: str # model name used to generate summary
    text_summary_dir: str # path to save text summaries
    summarizer_prompt_dir: str
    text_summarizer_prompt: str 
    
@dataclass
class FireStoreConfig:
    firebase_credentials_path:str
    session_id: str
