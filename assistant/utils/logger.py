# assistant/utils/logger.py

import logging
import os

LOG_DIR = "/home/ubuntu/assistant/logs"
LOG_FILE = os.path.join(LOG_DIR, "assistant.log")

def setup_logger(log_level=logging.INFO):
    """Configures the application logger."""
    # Create log directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("AssistantLogger")
    logger.setLevel(log_level)

    # Prevent adding multiple handlers if called again
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(LOG_FILE, encoding='utf-8')
    fh.setLevel(log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

# Initialize logger on import
log = setup_logger()

if __name__ == "__main__":
    log.debug("Este é um log de debug.")
    log.info("Este é um log de informação.")
    log.warning("Este é um log de aviso.")
    log.error("Este é um log de erro.")
    log.critical("Este é um log crítico.")
    print(f"Log configurado. Verifique o console e o arquivo: {LOG_FILE}")

