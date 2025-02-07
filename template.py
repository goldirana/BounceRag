import os
from pathlib import Path

front_end = "frontend"
back_end = "backend"

backend_structure = [
    f"{back_end}/__init__.py",
    f"{back_end}/data/raw_pdfs/",
    f"{back_end}/data/reports/",
    
    # src
    f"{back_end}/src/__init__.py",
        # extractors
    f"{back_end}/src/extractors/extract.py",
    f"{back_end}/src/extractors/__init__.py",
    f"{back_end}/src/extractors/text_extractor.py",
    f"{back_end}/src/extractors/table_extractor.py",
    f"{back_end}/src/extractors/image_extractor.py",
        # storage
    f"{back_end}/src/storage/__init__.py",
    f"{back_end}/src/storage/pinecone_storage.py",
    f"{back_end}/src/storage/chroma_storage.py",
    f"{back_end}/src/storage/firebase_storage.py",
        # utils
    f"{back_end}/src/utils/__init__.py",
    f"{back_end}/src/utils/common.py",
        # config
    f"{back_end}/src/config/__init__.py",
    f"{back_end}/src/config/configuration.py",
        # constants
    f"{back_end}/src/constants/__init__.py",
        # entity
    f"{back_end}/src/entity/__init__.py",
    f"{back_end}/src/entity/report.py",
        # exceptions and logs
    f"{back_end}/logger/__init__.py",
    f"{back_end}/exception/__init__.py",
        # prompts
    f"{back_end}/src/prompts/__init__.py",
    f"{back_end}/src/prompts/image_prompt.json",
    f"{back_end}/src/prompts/table_prompt.json",
    f"{back_end}/src/prompts/text_prompt.json",
        # research
    f"{back_end}/notebooks/__init__.py",
    f"{back_end}/notebooks/trails.ipynb",
]

misc_structure = [
    "app.py",
    "README.md",
    "requirements.txt",
    ".gitignore",
    "Dockerfile",
    "setup.py",
    "Makefile",
    "LICENSE",
    "Readme.md",
    "config.yaml"
]

frontend_structure = ["frontend/src/"]

for structure in [backend_structure, misc_structure, frontend_structure]:
    for filepath in structure:
        if filepath.endswith("/"):
            os.makedirs(filepath, exist_ok=True)
        
        filepath = Path(filepath)
        filedir, filename = os.path.split(filepath)
        if filedir != "":
            os.makedirs(filedir, exist_ok=True)
        if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
            with open(filepath, "w") as f:
                pass
        else:
            print(f"file is already present at: {filepath}")