from backend.src.extractors.data_ingestion import DataIngestion
from backend.src.extractors.image_summarizer import ImageSummarizer
from backend.src.extractors.text_summarizer import TextSummarizer
from backend.src.constants import *
from backend.src.config.configuration import ConfigurationManager
from backend.src.storage.chroma_storage import VectorDatabase
from backend.src.queries.handler import QueryHandler

from backend.src.llm_models import get_openai_model, get_openai_embeddings
from backend.src.constants import (CONFIG_FILE_PATH, PARAMS_FILE_PATH, FIREBASE_CREDENTIALS_PATH)

import os


from dotenv import load_dotenv
load_dotenv()

model = get_openai_model()
embedding = get_openai_embeddings()


# get config manger
config_manager = ConfigurationManager(CONFIG_FILE_PATH, PARAMS_FILE_PATH)
data_ingestion_config = config_manager.get_data_ingestion_params()
image_summarizer_config = config_manager.get_image_summarizer_params()
text_summarizer_config = config_manager.get_text_summarizer_params()
vector_database_config = config_manager.get_vectordatabase_config()

data_ingestion = DataIngestion(data_ingestion_config)
image_summarizer = ImageSummarizer(image_summarizer_config, model)
vector_database = VectorDatabase(vector_database_config)
chroma = vector_database.init_chromadb(embeddings=get_openai_embeddings())
retriever = vector_database.get_multivector_retriever(chroma)


# pdf file paths
raw_pdf_path = "backend/data/raw_pdfs"
pdfs = os.listdir(raw_pdf_path)
pdf_file_paths = [os.path.join(raw_pdf_path, i) for i in pdfs]

def main(pdf_file_paths=pdf_file_paths):
    for pdf_path in pdf_file_paths:
        
        print("processing pdf: ", pdf_path)
        raw_pdf_elements, report_dir = data_ingestion.process_pdf(pdf_path,
                                                                save=True,
                                                                strategy="hi_res", # 
                                                                split_pdf_page=True,  # to process each page seprately
                                                                split_pdf_allow_failed=True, # continue processing even if some pages fail
                                                                extract_images_in_pdf=True,
                                                                infer_table_structure=True,
                                                                chunking_strategy="by_title",
                                                                extract_image_block_types = ["Image" , "Table"],
                                                                max_characters=4000,
                                                                new_after_n_chars=3800,
                                                                combine_text_under_n_chars=2000)
        image_path = os.path.join(report_dir, "images")
        images_path = image_summarizer.get_image_path(image_path)
        
        encoded_images = []
        images_summaries = []
        meta_data = []
        
        for image in images_path:
            encoded_image, image_source_path = image_summarizer.encode_image(image)
            images_summaries.append(image_summarizer.image_summarize(encoded_image))
            encoded_images.append(encoded_image)
            meta_data.append({"source": image_source_path,
                            "type": "image",
                            "title": image.split("/")[-1]})
            
        image_summaries = image_summarizer.add_metadata(encoded_images, images_summaries, metadata=meta_data, 
                                                        automatic_metadata=False)

        # # text summaries
        text_summarizer = TextSummarizer(text_summarizer_config, model)
        text_data = text_summarizer.get_text_data(raw_pdf_elements)     
        
        # Store text data
        raw_text, text_summaries, summary_metadata = text_summarizer.generate_summary(text_data)
        text_summaries = text_summarizer.add_metadata(raw_text, text_summaries, summary_metadata)
        vector_database.store_to_vb(text_summaries, retriever)
        
        # Store image data
        vector_database.store_to_vb(image_summaries, retriever)
        

if __name__ == "__main__":
    main()
    
