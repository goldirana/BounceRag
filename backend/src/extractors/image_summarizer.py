from backend.src.config.configuration import ConfigurationManager
from backend.src.utils.common import read_json
from langchain.schema.messages import HumanMessage
from langchain.schema.document import Document
from langchain_openai import ChatOpenAI
from typing import *
import base64
import uuid
from backend.src.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
import os
from dotenv import load_dotenv
from backend.src.llm_models import (get_openai_embeddings, get_openai_model)
load_dotenv()   

class ImageSummarizer:
    def __init__(self, config, model: object):
        super().__init__()
        self.config = config
        self.model = model
        self.image_summary_prompt = read_json(self.config.summarizer_prompt_dir)["image_summarizer_prompt"]
        
        # automatic metadata
        self.image_path = None
        self.type = "Image"
        self.uuids = None
        
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
        
    def image_summarize(self, img_base64) -> str:
        """Summarize image using LLM model API
        Args:
            img_base64: base64 encoded image
            prompt: prompt to summarize image
        Returns:
            str: summary of image"""
        
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
        """To create document from list of data"""
        _ = []
        
        for metadata, doc in data:
            metadata = {"doc_id": metadata}
            _.append(Document(doc, metadata=metadata))
        return _
    
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            encoded_images_with_metadata, summaries_with_metadata = func(self, *args, **kwargs)
            for index, summary in enumerate(summaries_with_metadata):
                summary.metadata["raw_string"] = encoded_images_with_metadata[index][1]
            return summaries_with_metadata
        return wrapper
    
    @decorator
    def add_metadata(self, encoded_images, summaries, metadata: list[dict]=None, automatic_metadata=False) -> Tuple[List[tuple], List[Document]]:
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