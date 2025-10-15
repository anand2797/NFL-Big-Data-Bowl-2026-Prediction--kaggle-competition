"""Data Ingestion 
step 3: This step is after , 
        step 1('src/nfl_game_competition/constants/__init__.py', 
              'src/nfl_game_competition/constants/training_pipeline_constants/__init__.py')
                                
        step 2 ('src/nfl_game_competition/entity/config_entity.py' files and 
                'src/nfl_game_competition/entity/artifact_entity.py' files.)

This module will download the data from kaggle using kaggle API, 
unzip the data and load the data from multiple files and combine them into single dataframe.
Next step 4 after this file is : src/nfl_game_competition/pipeline/train_pipeline.py
"""

import os, sys
from src.nfl_game_competition.logger import get_logger
from src.nfl_game_competition.exception import NFLGameCompetitionException
from src.nfl_game_competition.entity.config_entity import DataIngestionConfig
from src.nfl_game_competition.entity.artifact_entity import DataIngestionArtifact
from src.nfl_game_competition.utils.common import create_directories, load_data, save_data
from kaggle.api.kaggle_api_extended import KaggleApi
from pathlib import Path
import numpy as np
import pandas as pd
from zipfile import ZipFile
import glob

logger = get_logger(name="nfl_game_competition.components.data_ingestion")


# do changes based previos files changed

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            logger.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.config = config
            self.kaggle_api = KaggleApi()
            self.kaggle_api.authenticate()
            logger.info(f"Data Ingestion config: {self.config}")
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)
        
    def download_nfl_data(self) -> str:
        """
        Downloads the data from kaggle competition.
        Returns:
            str: Path to the downloaded data file.
        """
        try:
            logger.info(f"Downloading data from kaggle competition: {self.config.data_source_url}")
            create_directories([self.config.zipped_data_filepath])
            # os.system(f"kaggle competitions download -c nfl-big-data-bowl-2026-prediction -p {self.config.root_dir} --force")
            self.kaggle_api.competition_download_files(competition=self.config.data_source_url,
                                                       path=self.config.zipped_data_filepath,
                                                       force= True)
            logger.info(f"File downloaded successfully: {self.config.zipped_data_filepath}")
            return self.config.zipped_data_filepath
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)

    def extract_zip_file(self, zip_file_path: str, extract_dir: str):
        """
        Extracts a zip file to the specified directory.
        Args:
            zip_file_path (str): Path to the zip file.
            extract_dir (str): Directory where the contents will be extracted.
        returns:    
        """
        try:
            logger.info(f"Starting Unzip and Extracting zip file: {zip_file_path} to dir: {extract_dir}")
            # create directory if not exist
            create_directories([extract_dir])
            zip_file_name = f"{zip_file_path}/{self.config.data_source_url}.zip"
            with ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                
            logger.info(f"File extracted successfully: {extract_dir}")
            return Path(extract_dir)
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)

    # have to changes
    def load_data_multiple_files(self, unzip_dir: str) -> pd.DataFrame:
        try:
            logger.info(f"Loading data from unzipped dir: {unzip_dir}")
            all_files = glob.glob(os.path.join(unzip_dir, "*.csv"))
           
            train_input_files = [f for f in all_files if "train" in os.path.basename(f) and "input" in os.path.basename(f)]
            train_output_files = [f for f in all_files if "train" in os.path.basename(f) and "output" in os.path.basename(f)]
            
            df_list = []
            for input_file, output_file in zip(train_input_files, train_output_files):
                df_input = pd.read_csv(input_file)
                df_output = pd.read_csv(output_file)
                df_merged = pd.merge(df_input, df_output, on="gameId", how="inner")
                df_list.append(df_merged)
            
            full_df = pd.concat(df_list, ignore_index=True)
            logger.info(f"Data loaded successfully from multiple files. Shape: {full_df.shape}")
            return full_df
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)

    def initiate_data_ingestion(self):
        try:
            logger.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            zip_file_path = self.download_nfl_data()
            unzip_dir = self.extract_zip_file(zip_file_path, self.config.unzipped_data_dir)
            logger.info(f"Data Ingestion - data downloded done: {unzip_dir}")
            #full_df = self.load_data_multiple_files(unzip_dir)
            #train_set, test_set = self.train_test_splitting(full_df)
            #train_filepath = self.export_data_into_feature_store(train_set, "train")
            #test_filepath = self.export_data_into_feature_store(test_set, "test")
            #data_ingestion_aftifacts = DataIngestionArtifact(trained_filepath=train_filepath,
                                                             #test_filepath=test_filepath)
            #logger.info(f"Data Ingestion Completed. Artifacts: {data_ingestion_aftifacts}")
            return unzip_dir
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)
        


