import os
import sys
from src.nfl_game_competition.logger import get_logger
from src.nfl_game_competition.exception import NFLGameCompetitionException
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path 
from typing import Any
from box.exceptions import BoxValueError
import yaml

import pandas as pd

from zipfile import ZipFile

logger = get_logger(name="nfl_game_competition.utils.common")

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """REads yaml file and returns
    Args:
        path_to_yaml (str): path like input
    Raises:
        ValueError: if yaml file is empty
        e: empty file
    returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml}loaded Successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create list of Directories
    Args:
        path to directories (list): list of path of directories.
        ignore_log (bool, optional): ignore if multiple dirs are to be created. 
    """
    try:
        for path in path_to_directories:
            os.makedirs(path, exist_ok=True)
            if verbose:
                logger.info(f"created directory at: {path}")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)
    
@ensure_annotations
def save_json(path: Path, data: dict):
    """save json data
    Args:
        path (Path): path to save json file
        data (dict): data to be save in json file
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"json file saved at: {path}")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json data
    Args:
        path (Path): path to load json file
    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path) as f:
            content = json.load(f)
        logger.info(f"json file loaded successfully from : {path}")
        return ConfigBox(content)
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)
    
@ensure_annotations
def save_object(path: Path, obj: Any) -> None:
    """save object to file
    Args:
        path (Path): path to save the file
        obj (Any): object to be saved
    """
    try:
        dir_path = path.parent
        os.makedirs(dir_path, exist_ok=True)
        joblib.dump(value=obj, filename=path)
        logger.info(f"object saved successfully at : {path}")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)

@ensure_annotations
def load_object(path: Path) -> Any:
    """load object from file
    Args:
        path (Path): path to load the file
    Returns:
        Any: loaded object
    """
    try:
        return joblib.load(path)
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)

@ensure_annotations
def load_data(path: Path) -> pd.DataFrame:
    """load data from file
    Args:
        path (Path): path to load the file
    Returns:                                                                            
        pd.DataFrame: loaded dataframe
    """
    try:
        return pd.read_csv(path)
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)
    
@ensure_annotations
def save_data(path: Path, data: pd.DataFrame) -> None:
    """save data to file
    Args:
        path (Path): path to save the file
        data (pd.DataFrame): data to be saved
    """
    try:
        dir_path = path.parent
        os.makedirs(dir_path, exist_ok=True)
        data.to_csv(path, index=False)
        logger.info(f"data saved successfully at : {path}")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys)   



