from dataclasses import dataclass

"""
DAta Ingestion
  step 2.1: this step is after config_entity.py
  next step 3: after this step we goes to 'src/nfl_game_competition/component/data_ingestion.py' 
"""
@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str
    train_file_path: str
    test_file_path: str
