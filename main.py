# main.py (project root)
from src.nfl_game_competition.exception import logger

# Use the logger from exception.py
logger.info("This is a test log from main.py")
logger.warning("Warning test from main.py")
logger.error("Error test from main.py")

print("Imported exception.py and logged messages successfully.")
