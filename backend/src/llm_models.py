from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.config.configuration import ConfigurationManager


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
config_params = config_manager.config

def get_openai_model():
    model_name = config_params.model.chat_model
    model_temp = config_params.model.temperature
    model = ChatOpenAI(temperature=model_temp, model_name=model_name)
    return model

def get_openai_embeddings():
    embeddings = OpenAIEmbeddings()
    return embeddings
