import os
import logging
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"

log_path = os.path.join("artifacts", "logs", LOG_FILE)
os.makedirs(os.path.dirname(log_path), exist_ok=True)


os.makedirs(log_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.INFO,
    format= format,
    filename = LOG_FILE_PATH
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


if __name__ == "__main__":
    # quick sanity test when running module directly with -m
    logger = get_logger(name="nfl_game_competition.test")
    logger.info("Logger test: info message")
    logger.warning("Logger test: warning message")
    logger.error("Logger test: error message")
    # Print where the log file was written so you can check it
    try:
        print("Log file:", LOG_FILE_PATH)
    except NameError:
        print("LOG_FILE_PATH not available")