from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.config.configuration import ConfigurationManager
from backend.exception import ModelError

# import google.generativeai as genai
from IPython.display import Markdown
# from google.colab import userdata
from dotenv import load_dotenv
import os



load_dotenv()

config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
config_params = config_manager.config

def get_openai_model():
    """
    Initializes and returns an instance of the ChatOpenAI model with specified parameters.
    The model's name and temperature are retrieved from the configuration parameters.
    Returns:
        ChatOpenAI: An instance of the ChatOpenAI model initialized with the specified temperature and model name.
    """
    try:
        model_name = config_params.model.chat_model
        model_temp = config_params.model.temperature
        model = ChatOpenAI(temperature=model_temp, model_name=model_name)
        return model
    except ModelError:
        raise ModelError("Model initialization failed")
    
def get_openai_embeddings():
    embeddings = OpenAIEmbeddings()
    return embeddings


GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
# genai.configure(api_key=GOOGLE_API_KEY)

# def get_gemini_model():
#     model_name = config_params.gemini.model_name
#     genai.configure(api_key=GOOGLE_API_KEY)
#     model = genai.GenerativeModel(model_name=model_name)
#     return model