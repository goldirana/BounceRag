from backend.src.extractors.extract import Extractor
from backend.src.extractors.data_ingestion import DataIngestion
from backend.src.config.configuration import ConfigurationManager
from langchain_openai import ChatOpenAI
from langchain.schema.document import Document
from unstructured.documents.elements import CompositeElement, ListItem
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from typing import *


load_dotenv()

class TextSummarizer(Extractor):
    def __init__(self, config, model):
        self.config = config
        self.model = model
        
    def generate_summary(self, docs: List[dict]):
        """To generate summary of the text

        Args:
            model (object): model used to generate summary of text
            docs (List[dict]): List containing dict >> text with metadata
                len of docs = len of dict containing text with metadata
                        dict -> text, metadata 
        """
                    
        raw_text, metadata = Extractor.seprate_data_metadata_for_text(docs)
        prompt = ChatPromptTemplate.from_template(self.config.text_summarizer_prompt)
        summarize_chain = {"element": lambda x: x} | prompt | self.model | StrOutputParser()
        summaries = summarize_chain.batch(raw_text, {"max_concurrency": 5})
        return raw_text, summaries, metadata
    
    def get_text_data(self, raw_pdf_elements)-> List[Any]:
        text = []
        for element in raw_pdf_elements:
            if isinstance(element, CompositeElement) or isinstance(element, ListItem):
                text.append(element)
        return text
    
    @staticmethod
    def sanity_check_for_metadata(metadata: dict):
        """To check if metadata value has no data structure; if present take 1st value as str"""
        new_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (list, tuple)):
                new_metadata[key] = str(value[0])
            elif isinstance(value, set):
                new_metadata[key] = str(list(value)[0])
            else:
                new_metadata[key] = str(value)
        return new_metadata
        
    def add_metadata(self, raw_text, summaries, summary_metdata: dict=None):
        """To add rawtext as metadata for summaries"""
        uuids = [str(uuid.uuid4()) for i in raw_text]
        summaries_with_metadata = []
        for index, data in enumerate(zip(summaries, summary_metdata)):
            summary, metadata = data
            metadata["doc_id"] = uuids[index]
           
            metadata["raw_text"] = raw_text[index]
            metadata = TextSummarizer.sanity_check_for_metadata(metadata)
            summaries_with_metadata.append(Document(page_content=summary, metadata=metadata))
        
        return summaries_with_metadata
        
    
# Unit Testing
if __name__ == "__main__":
    model = ChatOpenAI(temperature=0, model="gpt-4o")
    pdf_file_path="backend/data/raw_pdfs/2023_removed.pdf"
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    text_summarizer_config = config_manager.get_text_summarizer_params()
    data_extractor_config = config_manager.get_data_ingestion_params()
    
    text_summarizer = TextSummarizer(text_summarizer_config, model)
    data_extractor = DataIngestion(data_extractor_config)
    

    data, current_pdf_dir = data_extractor.process_pdf(pdf_file_path,
                                  save=True,
                                    strategy="hi_res", # 
                                    split_pdf_page=True,  # to process each page seprately
                                    split_pdf_allow_failed=True, # continue processing even if some pages fail
                                    extract_images_in_pdf=True,
                                    infer_table_structure=True,
                                    chunking_strategy="by_title",
                                    extract_image_block_types = ["Image" , "Table"],
                                    max_characters=4000,
                                    new_after_n_chars=3800,
                                    combine_text_under_n_chars=2000
                                    )
    text_data = text_summarizer.get_text_data(data)