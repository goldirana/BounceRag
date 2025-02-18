import uuid
from typing import *
from langchain.schema.document import Document
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import CompositeElement, Table, Image, ListItem  
import os, re
from backend.exception import *


class Extractor:
    """Extractor class for processing PDF elements and extracting metadata.
    Methods:
        __init__():
            Initializes the Extractor class.
        get_metadata(raw_pdf_element: List) -> List:
            Extracts metadata from a list of PDF elements.
        add_metadata(self, element, **kwargs):
            Adds metadata to a given element and returns a Document object.
        get_year(self, file: str) -> str:
            Extracts the year from a given file name.
        extract_data(self, pdf_file, **kwargs):
            Extracts raw PDF elements from a given PDF file.
        generate_unique_id(self, data: Iterator) -> List[str]:
            Generates unique IDs for each element in the data.
        generate_document(self, content: List, id_key: str):
            Generates a list of Document objects from the given content.
        seprate_data_metadata_for_text(data: List[CompositeElement]) -> Tuple[List, List]:
            Separates text and metadata from a list of CompositeElement objects."""
    
    def __init__(self):
        pass
    
    @log_error(DataIngestionError, sucess_message="Metadata fetched sucessfully", 
            failure_message="Error fetching metadata from pdf")
    def get_metadata(raw_pdf_element: List) -> List[Dict]:
        """
        Extracts metadata from a list of raw PDF elements.
        Args:
            raw_pdf_element (List): A list of raw PDF elements, where each element 
                                    has a 'metadata' attribute that can be converted 
                                    to a dictionary.
        Returns:
            List[Dict]: A list of dictionaries containing metadata of each PDF element.
        """
        
        metadata = []
        for element in raw_pdf_element:
            metadata.append(element.metadata.to_dict())
        return metadata
    
    @log_error(DataIngestionError, sucess_message="Year fetched sucessfully", 
            failure_message="Error getting year from file")
    def get_year(self, file: str) -> str:
        """
        Extracts the year from the given file name.
        This method searches for a 4-digit year within the file name. If a year is found, it is returned as a string.
        If no year is found, the method attempts to extract the file name (without extension) and return it.
        In case of an error during this process, it logs the error and returns "1.0".
        Args:
            file (str): The file name from which to extract the year.
        Returns:
            str: The extracted year, the file name without extension, or "1.0" in case of an error.
        """
        year = re.search(r"\d{4}", file).group()    
        if year:
            return str(year)
        else:
            try:
                file_name = os.path.split(file)[-1].split(".")[0]
                return file_name
            except Exception as e:
                logger.error(f"Error in getting year from file: {file} with error: {e}")
                return "1.0"
        
    def extract_data(self, pdf_file, **kwargs)->List:
        """
        Extract data from a PDF file.
        This method uses the `partition_pdf` function to extract raw elements from the given PDF file.
        Args:
            pdf_file (str): The path to the PDF file to be processed.
            **kwargs: Additional keyword arguments to be passed to the `partition_pdf` function.
        Returns:
            list: A list of raw PDF elements extracted from the file.
        """
        
        raw_pdf_elements = partition_pdf(filename=pdf_file, **kwargs)
        return raw_pdf_elements
    
    @log_error(DataIngestionError, sucess_message="Unique ID generated sucessfully",
               failure_message="Error generating unique ID")
    def generate_unique_id(self, data: Iterator)-> List[str]:
        """
        Generate a list of unique IDs for each item in the provided data iterator.
        Args:
            data (Iterator): An iterator containing the data items for which unique IDs need to be generated.
        Returns:
            List[str]: A list of unique ID strings, one for each item in the input data.
        """
        unique_id = []
        for _ in data:
            unique_id.append(str(uuid.uuid4()))
        
        return unique_id
    
    def generate_document(self, content: List, id_key: str):
        """
        Generates a list of Document objects from the provided content.
        Args:
            content (List): A list of content strings to be converted into Document objects.
            id_key (str): The key to be used for the metadata dictionary in each Document.
        Returns:
            List[Document]: A list of Document objects with page content and metadata.
        """
        ids = self.generate_unique_id(content)
        summaries = [Document(page_content=summary, metadata={id_key: ids[index]})
                         for index, summary in enumerate(content)]
        return summaries
    
    @staticmethod
    def seprate_data_metadata_for_text(data: List[CompositeElement]) -> Tuple[List, List]:
        """
        Separates text and metadata from a list of CompositeElement objects.
        Args:
            data (List[CompositeElement]): A list of CompositeElement objects.
        Returns:
            Tuple[List, List]: A tuple containing two lists:
                - The first list contains the string representation of each CompositeElement.
                - The second list contains the metadata of each CompositeElement as dictionaries.
        """
        text, metadata = [], []
        for i in data:
            text.append(str(i))
            metadata.append(i.metadata.to_dict())
        return text, metadata