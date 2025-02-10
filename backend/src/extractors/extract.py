import uuid
from typing import *
from dataclasses import dataclass
from langchain.schema.document import Document
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import CompositeElement, Table, Image, ListItem  


class Extractor:
    def __init__(self):
        pass
    
    def get_metadata(raw_pdf_element: List) -> List:
        """To get the metadata of elements

        Args:
            raw_pdf_element (List): list of elements in pdf

        Returns:
            List: containing meta data
        """
        metadata = []
        for element in raw_pdf_element:
            metadata.append(element.metadata.to_dict())
        
        return metadata
    
    def add_metadata(self, element, **kwargs):
        metadata = kwargs
        return Document(element, metadata)
 
    def get_year(self, file: str) -> str:
        """To get the year from file name
        Args:
            file: name of with extension"""
        
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
        
    def extract_data(self, pdf_file, **kwargs):
        raw_pdf_elements = partition_pdf(filename=pdf_file, **kwargs)
        return raw_pdf_elements
    
    def generate_unique_id(self, data: Iterator)-> List[str]:
        """To generate unique id for each element"""
        
        unique_id = []
        for _ in data:
            unique_id.append(str(uuid.uuid4()))
        
        return unique_id
    
    def generate_document(self, content: List, id_key: str):
        """To generate document from content"""
                
        ids = self.generate_unique_id(content)
        summaries = [Document(page_content=summary, metadata={id_key: ids[index]})
                         for index, summary in enumerate(content)]
        
        return summaries
    
    @staticmethod
    def seprate_data_metadata_for_text(data: List[CompositeElement]) -> Tuple[List, List]:
        """To seprate data and metadata from dict

        Args:
            data (List[dict]): List containing raw_pdf_elements
            text_name (str): key to get text from dict. Defaults to "text"
            metadata_name (str): key to get metadata from dict. Defaults to "metadata"

        Returns:
            Tuple: containing text, metadata
        """
        text, metadata = [], []
        for i in data:
            text.append(str(i))
            metadata.append(i.metadata.to_dict())
        return text, metadata