from backend.src.constants import (CONFIG_FILE_PATH, PARAMS_FILE_PATH, FIREBASE_CREDENTIALS_PATH)
from backend.src.utils.common import read_yaml, read_json
from backend.src.entity.config_entity import (ImageSummarizerConfig, 
                                      DataIngestionConfig,
                                      VectorDatabaseConfig,
                                      TextSummarizerConfig,
                                      FireStoreConfig,
                                      PromptConfig)
import os
from typing import *
print("---"*100)
print(CONFIG_FILE_PATH)
print(PARAMS_FILE_PATH)
print(read_yaml(CONFIG_FILE_PATH))
print(os.getcwd())
# code to get the executing file name 
print("---"*100)

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Gets the absolute path of the current script
# CONFIG_FILE_PATH = os.path.join(BASE_DIR, "../../../config.yaml")
# PARAMS_FILE_PATH = os.path.join(BASE_DIR, "../../../params.yaml")

class ConfigurationManager:
    def __init__(self, CONFIG_FILE_PATH, PARAMS_FILE_PATH):
        self.config = read_yaml(CONFIG_FILE_PATH)
        self.params = read_yaml(PARAMS_FILE_PATH)
        if self.config is None:
            print("---"*100)
            print(os.path.abspath(__file__))
            
            raise ValueError("ERROR: Config file not loaded. Check config.yaml path.")
        
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
    
    def get_prompt_config(self) -> Optional[Union[PromptConfig, dict]]:
        params = PromptConfig(prompt_dir=self.config.prompts.prompt_dir,
                                system_message_prompt=self.config.prompts.system_message_prompt)
        return params

    def get_firebase_params(self):
        print("**"*100)
        print(self.config)
        cred = FireStoreConfig(
            firebase_credentials_path=self.config.firebase.firebase_credentials_path,
            session_id=self.config.firebase.session_id
        )
        return cred
    
if __name__ == "__main__":
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    print(config_manager.get_image_summarizer_params())
    print(config_manager.get_vectordatabase_config())
    print(config_manager.get_text_summarizer_params())
    print("__"* 50)
    print(config_manager.get_firebase_params())