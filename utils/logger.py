import os
import logging

#  Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

#  Create a single shared logger
logger = logging.getLogger("FinstreamAgents")
logger.setLevel(logging.INFO)

#  Define log format
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

#  File handler (all agents share one log file)
file_handler = logging.FileHandler(os.path.join("logs", "agents.log"),encoding="utf-8")
file_handler.setFormatter(formatter)

#  Console handler (for printing live logs)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

#  Avoid duplicate handlers when importing across agents
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
