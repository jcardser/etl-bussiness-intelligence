from datetime import datetime
import os
from loguru import logger

def setup_logging():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    app_log = os.path.join(LOG_DIR, f"app{timestamp}.log")

    logger.remove()

    logger.add(
        app_log,
        rotation="1 week",
        retention="4 weeks",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name} | {message}"
    )

    separator = "=" * 70
    logger.info(separator)
    logger.info("Logging configurado correctamente.")
    return logger
