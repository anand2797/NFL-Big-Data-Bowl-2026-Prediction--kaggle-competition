
# NFL Game Competition Project Structure Templates
# Import necessary modules
import os
import sys
from pathlib import Path
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO)

# Define the project name
project_name = "nfl_game_competition"

# List of files and directories to create for the project structure
list_of_files = [
    # Root files
    f"src/{project_name}/__init__.py",  # Package initializer
    f"src/{project_name}/components/__init__.py",  # Components package initializer
    f"src/{project_name}/components/data_ingestion.py",  # Data ingestion module
    f"src/{project_name}/components/data_validation.py",  # Data validation module
    f"src/{project_name}/components/data_transformation.py",  # Data transformation module
    f"src/{project_name}/components/model_trainer.py",  # Model trainer module
    f"src/{project_name}/components/model_evaluation.py",  # Model evaluation module
    
    f"src/{project_name}/utils/__init__.py",  # Utils package initializer
    f"src/{project_name}/utils/common.py",  # Common utility functions
    f"src/{project_name}/utils/mlflow.py",  # MLflow utility functions
    
    f"src/{project_name}/logger.py",  # Logger module
    f"src/{project_name}/exception.py",  # Exception handling module
    
    f"src/{project_name}/config/__init__.py",  # Config package initializer
    f"src/{project_name}/config/configuration.py",  # Configuration management
    f"src/{project_name}/config/cloud_storage.py",  # Cloud storage configuration
    f"src/{project_name}/config/mlflow.py",  # MLflow configuration
    
    f"src/{project_name}/pipeline/__init__.py",  # Pipeline package initializer
    f"src/{project_name}/pipeline/predict_pipeline.py",  # Prediction pipeline
    f"src/{project_name}/pipeline/train_pipeline.py",  # Training pipeline
    f"src/{project_name}/pipeline/visuals.py",  # Visualization pipeline
    
    f"src/{project_name}/entity/__init__.py",  # Entity package initializer
    f"src/{project_name}/entity/config_entity.py",  # Config entity definitions
    f"src/{project_name}/entity/artifact_entity.py",  # Artifact entity definitions
    f"src/{project_name}/entity/model_factory.py",  # Model factory entity
    f"src/{project_name}/entity/mlflow_entity.py",  # MLflow entity definitions
    f"src/{project_name}/entity/predict_entity.py",  # Prediction entity definitions

    f"src/{project_name}/constants/__init__.py",  # Constants package initializer
    
    "config/config.yaml",  # Main configuration file
    "params.yaml",  # Parameters file
    "app.py",  # Application entry point
    "main.py",  # Main script
    #"Dockerfile",  # Docker configuration
    "requirements.txt",  # Python dependencies
    "setup.py",  # Setup script for packaging
    "notebooks/trials.ipynb",  # Research notebook
    "templates/index.html",  # Web app template
    "artifacts/data/"  # Data artifacts directory
]

# Create directories and files as specified in list_of_files
for file_path in list_of_files:
    file_path = Path(file_path)
    # If path ends with '/' or has no file extension, treat as directory
    if str(file_path).endswith("/") or file_path.suffix == "":
        os.makedirs(file_path, exist_ok=True)
        logging.info(f"Created directory: {file_path}")
    else:
        file_dir, file_name = os.path.split(file_path)
        # Create parent directory if it does not exist
        if file_dir != "":
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f"Created directory: {file_dir}")
        # Create empty file if it does not exist or is empty
        if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
            with open(file_path, "w") as f:
                pass
            logging.info(f"Created empty file: {file_path}")
        else:
            logging.info(f"File already exists and is not empty: {file_path}")
