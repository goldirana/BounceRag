from dataclasses import dataclass
from typing import *


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
