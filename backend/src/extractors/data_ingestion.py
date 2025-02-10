from backend.src.extractors.extract import Extractor
from backend.src.config.configuration import ConfigurationManager
from backend.src.utils.common import create_directory
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
import os


class DataIngestion(Extractor):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.raw_pdf_elements = None
        self.current_pdf_file = None # to keep track of current pdf file being processed (future case)
    
    def process_pdf(self, pdf_file_path: str, **kwargs):  
        """To extract the data from pdf file using unstructured library
            Args:
                pdf_file_path (str): full path of pdf file

            Returns:
                tuple: raw_pdf_elements, report_dir (which is pdf_file_path - extension - filepath)
        """
        
        file_name = os.path.split(pdf_file_path)[-1].split(".")[0] # get the filename from file name and set it as directory name
        report_dir = os.path.join(self.config.reports, file_name) 
        print(report_dir)
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