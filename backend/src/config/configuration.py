from backend.src.constants import (CONFIG_FILE_PATH, PARAMS_FILE_PATH)
from backend.src.utils.common import read_yaml, read_json

from backend.src.entity.config_entity import (ImageSummarizerConfig, 
                                      DataIngestionConfig,
                                      VectorDatabaseConfig,
                                      TextSummarizerConfig)
import os
print(os.getcwd())                       

class ConfigurationManager:
    def __init__(self, CONFIG_FILE_PATH, PARAMS_FILE_PATH):
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.params = read_yaml(PARAMS_FILE_PATH)
        
    def get_image_summarizer_params(self) -> ImageSummarizerConfig:
        params = ImageSummarizerConfig(
            model=self.config.model.chat_model,
            image_summary_dir=self.config.image_summarizer.image_summary_dir,
            summarizer_prompt_dir=self.config.prompts.summarizer_prompt_dir)
        return params
    
    def get_text_summarizer_params(self) -> TextSummarizerConfig:
        summarizer_prompt_dir=read_json(self.config.prompts.summarizer_prompt_dir)
        
        params = TextSummarizerConfig(
            model=self.config.text_summarizer.model,
            text_summary_dir=self.config.text_summarizer.text_summary_dir,
            summarizer_prompt_dir=self.config.prompts.summarizer_prompt_dir,
            text_summarizer_prompt=summarizer_prompt_dir["text_summarizer_prompt"],
        )
        return params
    
    def get_data_ingestion_params(self) -> DataIngestionConfig:
        params = DataIngestionConfig(
            raw=self.config.data_dir.raw,
            reports=self.config.data_dir.reports,
            metadata=self.config.metadata)
        return params
    
    def get_vectordatabase_config(self) -> VectorDatabaseConfig:
        params = VectorDatabaseConfig(
            vectorstore_name=self.config.vector_database.vectorstore_name,
            persist_directory=self.config.vector_database.persist_directory)
        return params
    
if __name__ == "__main__":
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    print(config_manager.get_image_summarizer_params())
    print(config_manager.get_vectordatabase_config())
    print(config_manager.get_text_summarizer_params())