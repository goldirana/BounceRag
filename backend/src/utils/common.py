import json, yaml
from backend.logger import logger
from box import ConfigBox
from pathlib import Path
import os
import pickle
from multiprocessing import Pool, cpu_count
from typing import *
from tqdm import tqdm


def split_file_extension(path: str) -> str:
    """
    To remove the extension name from the given path
    Args:
        path: str
    """
    try:
        root_dir = str(Path(path).resolve().parent)
        # logger.debug("File path without extension is %s", root_dir)
        return root_dir
    except Exception as e:
        logger.error(e)
        
def check_directory_path(path: str) -> None:
    """
    To check whether directory presents at given location
    Args:
        path(str)
    Return:
        Boolean
    """
    try:
        check = os.path.isdir(path)
        if check:
            # logger.info("Directory already present at %s", path)
            return True
        else:
            # logger.info("Directory not present at %s", path)
            return False
    except Exception as e:
        logger.error(e)
        
def create_directory(path: str, is_extension_present: bool=True)-> None:
    """Create directory at given location
    Args:
        path(str): path where directory needs to be created
        is_extension_present: whether extension of file present in path
            If present then extract the root path and creates directory"""
    if is_extension_present: # remove extension to create directory
            path = str(split_file_extension(path))
    _ = check_directory_path(path)
    try:
        if _ == False:
            os.makedirs(path, exist_ok=True) # create directoy at given location
            logger.info("Creating directory at %s", path)
        else: 
            pass
    except Exception as e:
        logger.error(f"Error occured while creating directory at {path} \n{e}")

def read_yaml(path: str, format: str="r", log_info: bool=False) -> ConfigBox:
    """
    Reads a YAML file and returns its contents as a ConfigBox object.
    Args:
        path (str): The path to the YAML file.
        format (str, optional): The mode in which the file is opened. Defaults to "r".
        log_info (bool, optional): If True, logs an info message upon successful read. Defaults to False.
    Returns:
        ConfigBox: An object containing the parsed YAML data.
    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: For any other exceptions that occur during file reading.
    """
    
    try:
        with open(path, format                     ) as f:
            params = yaml.safe_load(f)
            if log_info == True:
                logger.info("Yaml read successfully from %s", path)
            return ConfigBox(params)
    except FileNotFoundError:
        logger.error("FileNotFoundError: %s", path)
    except Exception as e:
        logger.error(f"Exception occured while reading yaml file from \
                        location: {path}\n {e}")
        
def save_pickle(object: Any, path: str):
    """
    Save an object to a file using pickle.
    Args:
        object (Any): The object to be serialized and saved.
        path (str): The file path where the object will be saved.
    Raises:
        pickle.PickleError: If there is an error during the pickling process.
        Exception: For any other exceptions that occur during the file operation.
    Logs:
        Info: When the object is successfully saved.
        Error: If there is an error during the saving process.
    """
    try:
        create_directory(path, is_extension_present=True)
        with open(path, "wb") as f:
            pickle.dump(object, f)
        logger.info("Pickle object stored at %s", path)
    except pickle.PickleError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)

def read_pickle(path: str):
    try:
        path = str(Path(path).resolve())
        with open(path, "rb") as f:
            params = pickle.load(f)
            logger.info("Read pickle from dir: %s", path)
            return params
    except Exception as e:
        logger.error("Error occured while reading pickle %s", e)


def read_json(path, log_info=False):
    """
    Reads a JSON file from the specified path and returns its contents as a dictionary.
    Args:
        path (str): The file path to the JSON file.
        log_info (bool, optional): If True, logs information about the reading process. Defaults to False.
    Returns:
        dict: The contents of the JSON file.
    Raises:
        Exception: If there is an error reading the JSON file.
    """
    
    try:
        with open(path, "r") as f:
            params = json.load(f)
            if log_info == True:
                logger.info("Json read successfully from %s", path)
            if params == None:
                logger.info("Json not read")
        return params
    except Exception as e:
        logger.info(e)
        raise e    
    
def save_json(object, path):
    """
    Save a Python object as a JSON file.
    Args:
        object (any): The Python object to be saved as JSON.
        path (str): The file path where the JSON file will be saved.
    Raises:
        Exception: If there is an error during the file writing process, it will be logged.
    """
    
    try:
        with open(path, "w") as f:
            json.dump(object, f)
            logger.info("Json object saved at %s", path)
    except Exception as e:
        logger.error(e)

def log_error(exception, sucess_message=None, failure_message=None):
    """
    A decorator that logs a success message if the decorated function executes without exceptions,
    and logs an error message along with the exception details if an exception is raised.
    Args:
        sucess_message (str, optional): The message to log if the function executes successfully.
        failure_message (str, optional): The message to log if the function raises an exception.
    Returns:
        function: The decorated function with added logging functionality.
    """
    def decorator(func):  # This is the actual decorator
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if sucess_message is not None:
                    logger.info(sucess_message)
                return result
            except exception as e:
                print(f"ERROR: {failure_message}\nException in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator 

def perform_multiprocessing(func, iterable):
    with Pool(processes=cpu_count()) as pool:
        tqdm(pool.imap(func, iterable), total=len(iterable))