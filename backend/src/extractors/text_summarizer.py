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
import uuid
from backend.exception import *

load_dotenv()

class TextSummarizer(Extractor):
    def __init__(self, config, model):
        super().__init__()
        self.config = config
        self.model = model
    
    @log_error(TextSummarizerError, failure_message="Error while generating summary")
    def generate_summary(self, docs: List[dict]):
        """
        Generates summaries for a list of documents.
        Args:
            docs (List[dict]): A list of dictionaries where each dictionary contains 
                               the raw text and associated metadata of a document.
        Returns:
            Tuple[List[str], List[str], List[dict]]: A tuple containing:
                - raw_text (List[str]): A list of raw text extracted from the documents.
                - summaries (List[str]): A list of generated summaries for the documents.
                - metadata (List[dict]): A list of metadata associated with the documents.
        """

        raw_text, metadata = Extractor.seprate_data_metadata_for_text(docs)
        prompt = ChatPromptTemplate.from_template(self.config.text_summarizer_prompt)
        summarize_chain = {"element": lambda x: x} | prompt | self.model | StrOutputParser()
        summaries = summarize_chain.batch(raw_text, {"max_concurrency": 5})
        return raw_text, summaries, metadata
    
    @log_error(TextSummarizerError, failure_message="Error while getting composite and listitems")
    def get_text_data(self, raw_pdf_elements)-> List[Any]:
        """
        Extracts text data from a list of raw PDF elements.
        This method iterates through the provided list of raw PDF elements and 
        appends elements that are instances of CompositeElement or ListItem to 
        the text list.
        Args:
            raw_pdf_elements (List[Any]): A list of raw elements extracted from a PDF.
        Returns:
            List[Any]: A list containing elements that are instances of CompositeElement or ListItem.
        """  
        text = []
        for element in raw_pdf_elements:
            if isinstance(element, CompositeElement) or isinstance(element, ListItem):
                text.append(element)
        return text
    
    @staticmethod
    def sanity_check_for_metadata(metadata: dict):
        """
        Check and sanitize metadata values.
        This function iterates through the provided metadata dictionary and ensures that each value is converted to a string.
        If the value is a list, tuple, or set, it takes the first element and converts it to a string.
        Otherwise, it directly converts the value to a string.
        Args:
            metadata (dict): The metadata dictionary to be sanitized.
        Returns:
            dict: A new dictionary with sanitized metadata values as strings.
        """
        new_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, (list, tuple)):
                new_metadata[key] = str(value[0])
            elif isinstance(value, set):
                new_metadata[key] = str(list(value)[0])
            else:
                new_metadata[key] = str(value)
        return new_metadata
        
    @log_error(TextSummarizerError, failure_message="Error while adding metadata to summaries")
    def add_metadata(self, raw_text, summaries, summary_metdata: dict=None):
        """
        Adds metadata to the provided summaries and returns a list of Document objects with the enriched metadata.
        Args:
            raw_text (list of str): The list of raw text strings corresponding to the summaries.
            summaries (list of str): The list of summary strings to which metadata will be added.
            summary_metdata (dict, optional): A dictionary containing metadata for each summary. Defaults to None.
        Returns:
            list of Document: A list of Document objects, each containing a summary and its associated metadata.
        Raises:
            ValueError: If the lengths of `raw_text`, `summaries`, and `summary_metdata` do not match.
        """
        
        uuids = [str(uuid.uuid4()) for i in raw_text]
        summaries_with_metadata = []

        for index, data in enumerate(zip(summaries, summary_metdata)):
            summary, metadata = data
            metadata["doc_id"] = uuids[index]
            metadata["type"] = "text"
            metadata["raw_string"] = raw_text[index]
            metadata = TextSummarizer.sanity_check_for_metadata(metadata)
            summaries_with_metadata.append(Document(page_content=summary, metadata=metadata))
        
        return summaries_with_metadata
        
    
# Unit Testing
if __name__ == "__main__":
    model = ChatOpenAI(temperature=0, model="gpt-4o")
    pdf_file_path="data/raw_pdfs/2023_removed.pdf"
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