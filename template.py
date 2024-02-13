import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


project_name = "sensorqualityclassifier"


list_of_files = [
    ".github/workflows/.gitkeep",
    f"{project_name}/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/utils/common.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/pipeline/data_ingestion_pipeline.py",
	f"{project_name}/pipeline/data_validation_pipeline.py",
	f"{project_name}/pipeline/data_transformation_pipeline.py",
	f"{project_name}/pipeline/model_training_pipeline.py",
	f"{project_name}/pipeline/model_evaluation_pipeline.py",
	f"{project_name}/pipeline/inference_pipeline.py",
    f"{project_name}/constants/__init__.py",
    "config/config.yaml",
    "config/schema_training.json",
    "config/schema_prediction.json",
    "main.py",
    "app.py",
    "Dockerfile",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html",
    "test.py"


]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")