from backend.src.config.configuration import ConfigurationManager
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.src.utils.common import read_json
import os
config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
prompt_params = config_manager.get_prompt()

def get_system_prompt():
    docs = read_json(os.path.join(prompt_params.prompt_dir, prompt_params.system_message_prompt))
    return docs["system_message"]
