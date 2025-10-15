import os, sys
from src.nfl_game_competition.logger import get_logger
from src.nfl_game_competition.exception import NFLGameCompetitionException

from src.nfl_game_competition.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig)
from src.nfl_game_competition.entity.artifact_entity import DataIngestionArtifact

from src.nfl_game_competition.components.data_ingestion import DataIngestion
import sys

logger = get_logger(name="nfl_game_competition/pipelines/train_pipeline.py")
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    """data ingestion 
            step 4 after : components/data_ingestion.py
            next step 5: main.py

    """
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion = DataIngestion(config=self.data_ingestion_config)
            unzip_dir = data_ingestion.initiate_data_ingestion()
            #logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
            return unzip_dir
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)
        
    # run pipeline
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            # data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            # data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            # model_trainer_artifact = self.start_model_training(data_transformation_artifact=data_transformation_artifact)
            # model_evaluation_artifact = self.start_model_evaluation(data_validation_artifact=data_validation_artifact,
            #                                                        model_trainer_artifact=model_trainer_artifact)
            # model_pusher_artifact = self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
            # return model_pusher_artifact
            return data_ingestion_artifact
            
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)


# check if the pipeline is running
if __name__ == "__main__":
    train_pipeline = TrainingPipeline()
    train_pipeline.run_pipeline()