# main.py (project root)
"""from src.nfl_game_competition.logger import get_logger
# check if data_ingestion.py changes are correct

logger = get_logger(__name__)

from src.nfl_game_competition.components.data_ingestion import DataIngestion
from src.nfl_game_competition.entity.config_entity import TrainingPipelineConfig
from src.nfl_game_competition.entity.config_entity import DataIngestionConfig   
from src.nfl_game_competition.exception import NFLGameCompetitionException
import sys
if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise NFLGameCompetitionException(f"Error in Data Ingestion main: {e}", sys)"""

from src.nfl_game_competition.pipeline.train_pipeline import TrainingPipeline

if __name__ == "__main__":
    pipeline = TrainingPipeline()
    pipeline.run_pipeline()
