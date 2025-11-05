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
from src.nfl_game_competition.utils.common import create_directories, load_data, save_data, write_yaml
from kaggle.api.kaggle_api_extended import KaggleApi
import subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from zipfile import ZipFile
import glob
from sklearn.model_selection import train_test_split
from typing import Tuple

logger = get_logger(name="nfl_game_competition.components.data_ingestion")


# do changes based previos files changed

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        try:
            logger.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.__config = config
            self.__kaggle_api = KaggleApi()
            self.__kaggle_api.authenticate()
            logger.info(f"Data Ingestion config: {self.__config}")
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)
        
       # ---------------------------- PRIVATE INTERNAL STEPS ----------------------------
    def _download_nfl_data(self) -> str:
        """
        Downloads the data from kaggle competition.
        Returns:
            str: Path to the downloaded data file.
        """
        try:
            logger.info(f"Downloading data from kaggle competition: {self.__config.data_source_url}")
            create_directories([self.__config.zipped_data_filepath])
            # os.system(f"kaggle competitions download -c nfl-big-data-bowl-2026-prediction -p {self.__config.root_dir} --force")
            #self.__kaggle_api.competition_download_files(competition=self.__config.data_source_url,
            #                                           path=self.__config.zipped_data_filepath,
            #                                           force= True)
            # check already exist or not
            # expected final zip name
            zip_file_expected = os.path.join(
                                            self.__config.zipped_data_filepath,
                                            f"{self.__config.data_source_url}.zip"
                                            )

            # ---- SKIP LOGIC ----
            if os.path.exists(zip_file_expected):
                logger.info(f"ZIP already exists. Skipping download → {zip_file_expected}")
                return self.__config.zipped_data_filepath
            cmd = ["kaggle", "competitions", "download", "-c", self.__config.data_source_url,
                   "-p", self.__config.zipped_data_filepath,
                   "--force"]
            subprocess.run(cmd, check=True)
            logger.info(f"File downloaded successfully: {self.__config.zipped_data_filepath}")
            return self.__config.zipped_data_filepath
        except subprocess.CalledProcessError as e:
            raise NFLGameCompetitionException(f"Kaggle CLI download failed: {e}", sys)
        except Exception as e:
            raise NFLGameCompetitionException(e, sys)

    def _extract_zip_file(self, zip_file_path: str, extract_dir: str):
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
            # ---- CHECK IF extraction already done ----
            if len(os.listdir(extract_dir)) > 0:
                logger.info(f"Unzipped folder already contains files. Skipping extraction.")
                return Path(extract_dir)
            zip_file_name = f"{zip_file_path}/{self.__config.data_source_url}.zip"
            with ZipFile(zip_file_name, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                
            logger.info(f"File extracted successfully: {extract_dir}")
            return Path(extract_dir)
        except Exception as e:
            raise NFLGameCompetitionException(e, sys) from e

    # have to changes means we have to merge or concat all files so write one or more methods here
    def _merge_all_input_output(self, unzipped_dir: str) -> pd.DataFrame:
        """
    short merge logic – renames only target x,y columns
        """
        try:
            feature_store_path = Path(self.__config.feature_store_filepath)
            # ─── SKIP MERGE IF ALREADY MERGED ─────────────────────────────
            if feature_store_path.exists():
                logger.info(f"Feature store already exists: {feature_store_path} → loading it directly")
                return load_data(feature_store_path)
            # ─────────────────────────────────────────────────────────────
                # find train folder dynamically
            train_dir = glob.glob(os.path.join(unzipped_dir, "**", "*train*"), recursive=True)[0]
            logger.info(f"Train folder found: {train_dir}")

            # year independent pattern
            input_files  = sorted(glob.glob(os.path.join(train_dir, "input_*_w*.csv")))
            output_files = sorted(glob.glob(os.path.join(train_dir, "output_*_w*.csv")))

            if len(input_files) != len(output_files):
                raise NFLGameCompetitionException("input/output count mismatch", sys)

            all_merged = []
            for inp_file, out_file in zip(input_files, output_files):
                df_input  = load_data(Path(inp_file))
                df_output = load_data(Path(out_file))
                # rename ONLY target prediction columns
                df_output = df_output.rename(columns={'x': 'target_x', 'y': 'target_y'})
                merged_df = pd.merge(df_input, df_output,
                                      on=['game_id', 'play_id', 'nfl_id', 'frame_id'], how='inner')
                all_merged.append(merged_df)

            final_df = pd.concat(all_merged, ignore_index=True)
            logger.info(f"Merged all input/output files, final shape: {final_df.shape}")

            save_data(path=Path(self.__config.feature_store_filepath), data=final_df, index=False)
            logger.info(f"Saved merged feature store file at: {self.__config.feature_store_filepath}")

            # write YAML schema (before split)
            schema = [{"name":str(c),"dtype":str(t)} for c,t in final_df.dtypes.items()]
            yaml_content = {
                "metadata":{"rows":int(final_df.shape[0]),"columns":int(final_df.shape[1])},
                "schema":schema
            }
            logger.info(f"Saving merged feature store file at: {self.__config.schema_file_path}")
            write_yaml(yaml_content, self.__config.schema_file_path)

            return final_df

        except Exception as e:
            raise NFLGameCompetitionException(e, sys) from e
        
    # train test split
    def _train_test_split_and_save(self, df: pd.DataFrame) -> Tuple[str, str]:
        """
        90/10 split with shuffle and fixed random_state; save to config paths.
        """
        try:
            train_df, test_df = train_test_split(df, test_size=0.10, shuffle=True, random_state=42)
            logger.info(f"Split done: train={train_df.shape}, test={test_df.shape}")

            save_data(self.__config.training_filepath, train_df, index=False)
            save_data(self.__config.testing_filepath, test_df, index=False)

            return self.__config.training_filepath, self.__config.testing_filepath
        except Exception as e:
            raise NFLGameCompetitionException(e, sys) from e
        
    # ---------------------------- PUBLIC API ----------------------------
    def initiate_data_ingestion(self):
        try:
            logger.info(f"{'>>'*20} Data Ingestion Started:  {'<<'*20}")

            zip_file_path = self._download_nfl_data()
            logger.info(f"Data Ingestion - data downloded done: {zip_file_path}")
            unzip_dir = self._extract_zip_file(zip_file_path, self.__config.unzipped_data_dir)
            logger.info(f"Data Ingestion - data downloded done: {unzip_dir}")
            # remaining code written here with comment
            merged_df = self._merge_all_input_output(str(unzip_dir))
            logger.info(f"Data Ingestion - Merging input/output done. merged data shape: {merged_df.shape}")
            # train test split
            train_filepath, test_filepath = self._train_test_split_and_save(merged_df)
            logger.info(f"Data Ingestion - Train test split done. train: {train_filepath}, test: {test_filepath}")
            # prepare artifacts
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.__config.feature_store_filepath,
                train_file_path=train_filepath,
                test_file_path=test_filepath
            )
            logger.info(f"{'>>'*20} Data Ingestion Completed..  {'<<'*20}")
            return data_ingestion_artifact
        except Exception as e:
            raise NFLGameCompetitionException(e, sys) from e
        


if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig()
        data_ingestion = DataIngestion(config=data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logger.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise NFLGameCompetitionException(f"Error in Data Ingestion main: {e}", sys) from e