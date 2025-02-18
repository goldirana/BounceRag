from backend.src.extractors.extract import Extractor
from backend.src.config.configuration import ConfigurationManager
from backend.src.utils.common import create_directory
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
import os
from backend.exception import *

class DataIngestion(Extractor):
    """DataIngestion class for processing PDF files and extracting data.
    Attributes:
        config (dict): Configuration settings for data ingestion.
        raw_pdf_elements (list): Extracted elements from the PDF.
        current_pdf_file (str): The current PDF file being processed.
    Methods:
        __init__(config):
            Initializes the DataIngestion class with the provided configuration.
        process_pdf(pdf_file_path: str, **kwargs):"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.raw_pdf_elements = None
        self.current_pdf_file = None # to keep track of current pdf file being processed (future case)
    
    @log_error(DataIngestionError, sucess_message="Raw Data fetched sucessfully",
               failure_message="Error fetching raw data from pdf")
    def process_pdf(self, pdf_file_path: str, **kwargs):  
        """
        Processes a PDF file by extracting data and organizing it into a directory structure.
        Args:
            pdf_file_path (str): The path to the PDF file to be processed.
            **kwargs: Additional keyword arguments for data extraction.
        Keyword Args:
            extract_image_block_output_dir (str, optional): Directory to store extracted images. 
                If not provided, a default directory named 'images' will be created inside the report directory.
        Returns:
            tuple: A tuple containing:
                - raw_pdf_elements: Extracted data from the PDF.
                - report_dir (str): The directory where the report and images are stored.
        """
        file_name = os.path.split(pdf_file_path)[-1].split(".")[0] # get the filename from file name and set it as directory name
        report_dir = os.path.join(self.config.reports, file_name) 
        # print(report_dir)
        create_directory(report_dir, is_extension_present=False) # create directory with file_name
        if kwargs.get("extract_image_block_output_dir", None) == None: # to create image folder in report_dir
            kwargs["extract_image_block_output_dir"] = os.path.join(report_dir, "images")
            
        raw_pdf_elements = self.extract_data(pdf_file_path, **kwargs)
        
        return raw_pdf_elements, report_dir
    

# unit testing
if __name__ == "__main__":
    test_pdf_path = "backend/data/reports/2023_removed"
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    data_ingestion_params = config_manager.get_data_ingestion_params(config_manager)
    data_ingestion = DataIngestion(config_manager)
    raw_pdf_elements, report_dir = data_ingestion.process_pdf(test_pdf_path)
    print(raw_pdf_elements, report_dir)