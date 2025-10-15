from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
from src.nfl_game_competition.constants import training_pipeline_constants as training_pipeline
import os

# add comment for each line that tells what codeline does
# Training Pipeline Configuration
class TrainingPipelineConfig:
    def __init__(self, timestamp: str = datetime.now()): 
        self.timestamp: str = timestamp.strftime("%d_%m_%Y_%H_%M_%S")              # format timestamp,  set timestamp
        self.pipeline_name = training_pipeline.PIPELINE_NAME              # set pipeline name
        self.artifact_name = training_pipeline.ARTIFACT_DIR              # set artifact name
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)   # set artifact directory
        self.model_dir = os.path.join(self.artifact_dir, "final_model")  # set model directory


"""
Data Ingestion :
step 2: this step after step 1 ('src/nfl_game_competition/constants/training_pipeline_constants/__init__.py' file)
step 2.1:  'src/nfl_game_competition/entity/artifact_entity.py' file
next step 3 : 'src/nfl_game_competition/component/data_ingestion.py' 

"""
@dataclass
class DataIngestionConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir,
                                                    training_pipeline.DATA_INGESTION_DIR_NAME)  # data ingestion directory
        self.data_source_url: str = training_pipeline.DATA_INGESTION_SOURCE_URL  # data source url  
        self.data_collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME  # data collection
        # feature store file path as(artifacts/data_ingestion/feature_store/nfl_game_features.csv)
        self.feature_store_filepath: str = os.path.join(self.data_ingestion_dir, 
                                                        training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
                                                        training_pipeline.FILE_NAME)  # feature store file path
        # training file path as(artifacts/data_ingestion/ingested/train_test_split/train.csv)
        self.training_filepath: str = os.path.join(self.data_ingestion_dir, 
                                                   training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                   training_pipeline.DATA_INGESTION_SPLITTED_DIR,
                                                   training_pipeline.TRAIN_FILE_NAME) # training file path 
        self.testing_filepath: str = os.path.join(self.data_ingestion_dir, 
                                                  training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                  training_pipeline.DATA_INGESTION_SPLITTED_DIR,
                                                  training_pipeline.TEST_FILE_NAME)  # test filepath
        # downloaded data zip file path:  artifacts/data_ingestion/ingested/data.zip
        self.zipped_data_filepath: str = os.path.join(self.data_ingestion_dir,
                                                      training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                      training_pipeline.DATA_INGESTION_ZIPPED_FILE_DIR)  
        # unzipped data directory path: artifacts/data_ingestion/ingested/unzipped_data
        self.unzipped_data_dir: str = os.path.join(self.data_ingestion_dir,
                                                   training_pipeline.DATA_INGESTION_INGESTED_DIR,
                                                   training_pipeline.DATA_INGESTION_UNZIPPED_DIR_NAME)  # unzipped data directory
        
