from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.config.configuration import ConfigurationManager


config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
config_params = config_manager.config

def get_openai_model():
    """
    Initializes and returns an instance of the ChatOpenAI model with specified parameters.
    The model's name and temperature are retrieved from the configuration parameters.
    Returns:
        ChatOpenAI: An instance of the ChatOpenAI model initialized with the specified temperature and model name.
    """
    
    model_name = config_params.model.chat_model
    model_temp = config_params.model.temperature
    model = ChatOpenAI(temperature=model_temp, model_name=model_name)
    return model

def get_openai_embeddings():
    embeddings = OpenAIEmbeddings()
    return embeddings
