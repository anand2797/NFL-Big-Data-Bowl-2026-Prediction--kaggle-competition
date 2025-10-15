import os

"""
Defining common constant variable for training pipeline.
"""
ARTIFACT_DIR: str = 'artifacts'
PIPELINE_NAME: str = 'nfl_game_competition'

TRAIN_FILE_NAME: str= "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILEPATH: str = os.path.join('data_schema', 'schema.yaml')

SAVED_MODEL_DIR: str = os.path.join("models", "saved_models")
FILE_NAME: str = "merged_data.csv"
"""Data Ingestion Step 1: 
This is step 1: here 'src/nfl_game_competition/constants/training_pipeline_constants/__init__.py'
Next step 2 will be in 'src/nfl_game_competition/entity/config_entity.py' to create DataIngestionConfig class

Data Ingestion related constant start with DATA_INGESTION var name.
"""
DATA_INGESTION_COLLECTION_NAME: str = "NFLGameCompetitionData"
DATA_INGESTION_SOURCE_URL: str = "nfl-big-data-bowl-2026-prediction"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_ZIPPED_FILE_DIR: str = "zipped_data"
DATA_INGESTION_UNZIPPED_DIR_NAME: str = "unzipped_data"
DATA_INGESTION_SPLITTED_DIR: str = "train_test_split"

