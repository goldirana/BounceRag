from backend.src.llm_models import  get_openai_model
from backend.src.config.configuration import ConfigurationManager
from backend.src.utils.common import read_json
from langchain.schema.messages import HumanMessage
from langchain.schema.document import Document
from langchain_openai import ChatOpenAI
import base64, uuid, os, requests
from dotenv import load_dotenv
from typing import *
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from backend.exception import *


load_dotenv()   
llama_api_key = os.getenv("LLAMA_API_KEY")

class ImageSummarizer:
    """ImageSummarizer is a class designed to summarize images using a language model API. It provides methods to encode images, summarize them, and manage metadata.
    Attributes:
        config (object): Configuration object containing settings and paths.
        model (object): Language model object used for summarization.
        image_summary_prompt (str): Prompt used for image summarization.
        image_path (str): Path to the image directory.
        type (str): Type of the summarizer, default is "Image".
        uuids (list): List of UUIDs for the images.
    Methods:
        __init__(config, model):
            Initializes the ImageSummarizer with the given configuration and model.
        encode_image(image_path):
            Encodes an image to base64 format.
        image_summarize(img_base64):
            Summarizes an image using the language model API.
        get_image_path(path):
            Returns the paths of images in the specified directory.
        create_doc_from_list(data):
        decorator(func):
        add_metadata(encoded_images, summaries, metadata=None, automatic_metadata=False):
    """
    def __init__(self, config, model: object=None):
        super().__init__()
        self.config = config
        if model == None:
            self.api_url = "https://api.llama-api.com/chat/completions",
            
            self.headers = {
            "Authorization": f"Bearer {llama_api_key}",
            "Content-Type": "application/json"
             }
            self.model_name = "llama3.2-11b-vision"
            self.model = "llama3.2-11b-vision"
        else:
            self.model = model
        self.image_summary_prompt = read_json(self.config.summarizer_prompt_dir)["image_summarizer_prompt"]
        
        # automatic metadata
        self.image_path = None
        self.type = "Image"
        self.uuids = None
        
        # setting different model to use
        if model==None:
            self.model_name = "llama3.2-11b-vision"
        elif "gpt" in model.model_name:
            self.model_name = "gpt"
        elif "gemini" in model.model_name:
            self.model_name = "gemini"
        
    @log_error(ImageSummarizerError, failure_message="Error occured while encoding image")
    def encode_image(self, image_path):
        """Encode image to base64
        Args:
            image_path: path to image
        Returns:
            str: base64 encoded image"""
        try:
            with open(image_path, "rb") as image:
                return base64.b64encode(image.read()).decode("utf-8"), image_path
        except Exception as e:
            print(f"Error: {e}")
            raise e
    
    @log_error(ImageSummarizerError, failure_message="Error occured while summarizing image")
    def image_summarize(self, img_base64) -> str:
        """Summarize image using LLM model API
        Args:
            img_base64: base64 encoded image
            prompt: prompt to summarize image
        Returns:
            str: summary of image"""
        # print("Using model for image summarizing:", self.model_name)
        if "gpt" in self.model_name:
            msg = self.model.invoke(
                [
                    HumanMessage(
                        content=[
                            {"type": "text", "text": self.image_summary_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_base64}"
                                },
                            },
                        ]
                    )
                ]
            )
            return msg.content
        elif "gemini" in self.model_name: # to use gemin model for image summarizing
            msg = self.model.generate_content(
            [
                self.image_summary_prompt,
                {
                    "mime_type": "image/jpg",  # Change if needed (e.g., "image/png")
                    "data": img_base64
                }
            ]
            )
            return msg.text
        
        elif "llama" in self.model_name:
            payload = {
                        "model": self.model_name,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": self.image_summary_prompt},
                                    {
                                        "type": "image",
                                        "image": img_base64
                                    },
                                ]
                            }
                        ],
                    "max_tokens": 300
                    }

            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()  # Raise an error if the request fails

            return response.json()["choices"][0]["message"]["content"]
            
    @log_error(ImageSummarizerError, failure_message="Error occured while getting image path")
    def get_image_path(self, path: str):
        """Returns the images path by joining the main path and the image names
        Args:
            path (str): image folder

        Returns:
            list[str]: containing images path 
        """
        # automatic metadata
        self.image_path = path
        
        x = os.listdir(path)
        images_path = []
        for image in x:
            images_path.append(os.path.join(path, image))
        return images_path
    
    
    @staticmethod
    def create_doc_from_list(data: List) -> List:
        """
        Creates a list of Document objects from a list of tuples containing metadata and document content.
        Args:
            data (List): A list of tuples where each tuple contains metadata and document content.
        Returns:
            List: A list of Document objects with the provided metadata and content.
        """

        _ = []
        
        for metadata, doc in data:
            metadata = {"doc_id": metadata}
            _.append(Document(doc, metadata=metadata))
        return _
    
    def decorator(func):
        """
        A decorator that processes the output of a function to add raw string metadata to summaries.
        This decorator assumes that the decorated function returns a tuple containing two lists:
        1. `encoded_images_with_metadata`: A list where each element is a tuple, and the second element of the tuple is a raw string.
        2. `summaries_with_metadata`: A list of summary objects, each having a `metadata` attribute which is a dictionary.
        The decorator iterates over the `summaries_with_metadata` list and adds the corresponding raw string from `encoded_images_with_metadata` to the `metadata` dictionary of each summary.
        Args:
            func (callable): The function to be decorated.
        Returns:
            callable: The wrapped function with added functionality.
        """
        def wrapper(self, *args, **kwargs):
            encoded_images_with_metadata, summaries_with_metadata = func(self, *args, **kwargs)
            for index, summary in enumerate(summaries_with_metadata):
                summary.metadata["raw_string"] = encoded_images_with_metadata[index][1]
            return summaries_with_metadata
        return wrapper
    
    @log_error(ImageSummarizerError, failure_message="Error occured while adding metadata")
    @decorator
    def add_metadata(self, encoded_images, summaries, metadata: list[dict]=None, 
                     automatic_metadata=False) -> Tuple[List[tuple], List[Document]]:
        """
        Adds metadata to encoded images and summaries.
        Args:
            encoded_images (List[bytes]): A list of encoded images.
            summaries (List[str]): A list of summaries corresponding to the images.
            metadata (list[dict], optional): A list of metadata dictionaries for each image and summary. Defaults to None.
            automatic_metadata (bool, optional): If True, automatically generates metadata using the image path and type. Defaults to False.
        Returns:
            Tuple[List[tuple], List[Document]]: A tuple containing a list of tuples with UUIDs and encoded images, 
                                                and a list of Document objects with summaries and metadata.
        """
        if automatic_metadata:
            metadata = {"source": self.image_path,
                        "type": self.type}
        self.uuids = [str(uuid.uuid4()) for i in encoded_images]
        encoded_images_with_metadata = list(zip(self.uuids, encoded_images))
        
        summaries_with_metadata = []
        for index, summary in enumerate(summaries):
            if automatic_metadata == False:
                meta_data = metadata[index]
            meta_data["doc_id"] = self.uuids[index]
            summaries_with_metadata.append(Document(page_content=summary, metadata=meta_data))
            
        return encoded_images_with_metadata, summaries_with_metadata
        
            
# unit testing
if __name__ == "__main__":
    model = get_openai_model()
    config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
    image_summarizer_config = config_manager.get_image_summarizer_params()
    image_summarizer = ImageSummarizer(image_summarizer_config, model)
    
    image_path = "backend/data/reports/2023_removed/images"
    images_path = image_summarizer.get_image_path(image_path)

    encoded_images = []
    image_summaries = []

    for image in images_path:
        encoded_image = image_summarizer.encode_image(image)
        image_summaries.append(image_summarizer.image_summarize(encoded_image))
        
        encoded_images.append(encoded_image)
    encoded_images, image_summaries = image_summarizer.add_metadata(encoded_images, image_summaries, automatic_metadata=True)