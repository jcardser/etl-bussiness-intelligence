import os
from loguru import logger

def setup_logging():
    """Configura los logs del proyecto ETL con Loguru."""

    # Ruta base del proyecto (nivel de main.py)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    os.makedirs(LOG_DIR, exist_ok=True)

    # Rutas de los logs
    app_log = os.path.join(LOG_DIR, "app.log")
    mongo_log = os.path.join(LOG_DIR, "client.log")
    repo_log = os.path.join(LOG_DIR, "repository.log")

    # Limpia handlers previos (útil si setup_logging() se llama más de una vez)
    logger.remove()

    # Log general de la aplicación
    logger.add(
        app_log,
        rotation="1 week",
        retention="4 weeks",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name} | {message}"
    )

    # Log específico de MongoDB
    logger.add(
        mongo_log,
        rotation="1 week",
        retention="4 weeks",
        compression="zip",
        level="INFO",
        filter=lambda record: record["extra"].get("context") == "Client",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {extra[context]} | {message}"
    )

    # Log específico del repositorio
    logger.add(
        repo_log,
        rotation="1 week",
        retention="4 weeks",
        compression="zip",
        level="INFO",
        filter=lambda record: record["extra"].get("context") == "Repository",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {name} | {message}"
    )

    logger.info("🪵 Logging configurado correctamente.")
    return logger
