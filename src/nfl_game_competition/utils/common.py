import os
import sys
from src.nfl_game_competition.logger import get_logger
from src.nfl_game_competition.exception import NFLGameCompetitionException
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path 
from typing import Any, Dict
from box.exceptions import BoxValueError
import yaml

import pandas as pd

from zipfile import ZipFile

logger = get_logger(name="nfl_game_competition.utils.common")


    
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
def save_object(path: Path | str, obj: Any) -> None:
    """save object to file
    Args:
        path (Path): path to save the file
        obj (Any): object to be saved

    Enhancements:
    - auto convert path to Path type
    - auto create parent directories
    - better logging + descriptive exception
    """
    try:
        path = Path(path)
        dir_path = path.parent
        os.makedirs(dir_path, exist_ok=True)
        joblib.dump(value=obj, filename=path)
        logger.info(f"object saved successfully at : {path}")
    except Exception as e:
        raise NFLGameCompetitionException(f"Failed to save object at {path}. Reason: {e}", sys)

@ensure_annotations
def load_object(path: Path | str) -> Any:
    """load object from file
    Args:
        path (Path): path to load the file
    Returns:
        Any: loaded object

    Load python object using joblib.
    Enhancements:
    - auto convert to Path
    - check file existence before loading
    - descriptive exception
    
    """
    try:
        path = Path(path)
        if not path.exists():
            raise NFLGameCompetitionException(f"The file: {path} does not exist")
        return joblib.load(path)              
    except Exception as e: 
        raise NFLGameCompetitionException(f"Failed to load object from {path}. Reason: {e}", sys)

def _detect_dtypes(path: Path, sample_n: int = 5000) -> dict:
    """
    internal helper: detect best dtypes from small sample to reduce memory
    """
    sample_df = pd.read_csv(path, nrows=sample_n)

    dtype_map = {}
    for col in sample_df.columns:
        if pd.api.types.is_integer_dtype(sample_df[col]):
            dtype_map[col] = 'int32'
        elif pd.api.types.is_float_dtype(sample_df[col]):
            dtype_map[col] = 'float32'
        else:
            dtype_map[col] = 'object'
    return dtype_map

@ensure_annotations
def load_data(path: Path | str, **pd_kwargs) -> pd.DataFrame:
    """load data from file
    Args:
        path (Path): path to load the file
    Returns:                                                                            
        pd.DataFrame: loaded dataframe
    """
    try:
        path = Path(path)
        if not path.exists():
            raise NFLGameCompetitionException(f"The file: {path} does not exist", sys)
        # detect dtype from sample
        dtype_map = _detect_dtypes(path)

        # now read full file with optimized dtypes
        return pd.read_csv(path, dtype=dtype_map, **pd_kwargs)
    except Exception as e:
        raise NFLGameCompetitionException(e, sys) from e
    
# @ensure_annotations
def save_data(path: Path | str, data: pd.DataFrame, index: bool = False, **pd_kwargs: Any) -> None:
    """save data to file
    Args:
        path (Path): path to save the file
        data (pd.DataFrame): data to be saved
    """
    try:
        path = Path(path)
        dir_path = path.parent
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Writing CSV: {path} (rows={len(data)}, cols={len(data.columns)})")
        data.to_csv(path, index=index, **pd_kwargs)
        logger.debug(f"CSV written successfully: {path}")
    except Exception as e:
        raise NFLGameCompetitionException(e, sys) from e

# ---------------------------
# YAML helpers
# ---------------------------
    
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

# @ensure_annotations
def write_yaml(content: Dict[str, Any], file_path: str) -> None:
    """
    Write a Python dict to a YAML file.
    """
    try:
        dir_path = Path(file_path).parent
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Writing YAML: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(content, f, sort_keys=False, allow_unicode=True)
        logger.debug(f"YAML written successfully: {file_path}")
    except Exception as e:
        raise NFLGameCompetitionException(f"Failed to write YAML: {file_path}. Error: {e}")
