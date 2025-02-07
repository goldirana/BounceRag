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



def read_yaml(path: str, format: str="r"):
    try:
        with open(path, format                     ) as f:
            params = yaml.safe_load(f)
            logger.info("Yaml read successfully from %s", path)
            return ConfigBox(params)
    except FileNotFoundError:
        logger.error("FileNotFoundError: %s", path)
    except Exception as e:
        logger.error(f"Exception occured while reading yaml file from \
                        location: {path}\n {e}")
        
def save_pickle(object: Any, path: str):
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


def read_json(path):
    try:
        with open(path, "r") as f:
            params = json.load(f)
            logger.info("Json object read sucessfully ")
            if params == None:
                logger.info("Json not read")
        print(params)
        return params
    except Exception as e:
        logger.info(e)
        raise e      

def log_error(sucess_message=None, faliure_message=None):
    def decorator(func):  # This is the actual decorator
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if sucess_message is not None:
                    logger.info(sucess_message)
                return result
            except Exception as e:
                print(f"ERROR: {faliure_message}\nException in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator  

def perform_multiprocessing(func, iterable):
    with Pool(processes=cpu_count()) as pool:
        tqdm(pool.imap(func, iterable), total=len(iterable))